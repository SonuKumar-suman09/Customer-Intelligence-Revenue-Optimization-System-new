import pandas as pd
import numpy as np
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models
import joblib

def ingest():
    print("Creating tables...")
    models.Base.metadata.create_all(bind=engine)
    
    print("Loading data from CSVs...")
    try:
        customers_df = pd.read_csv('../data/customers.csv')
        transactions_df = pd.read_csv('../data/transactions.csv')
    except FileNotFoundError:
        print("CSV files not found. Run data_generator.py first.")
        return

    db = SessionLocal()
    
    # Check if data already exists
    if db.query(models.Customer).first():
        print("Data already ingested.")
        db.close()
        return

    # To calculate features, we can do some pandas operations or just use what we have
    # The ml_pipeline calculates rfm, we'll do a quick rfm here to save into DB
    transactions_df['transaction_date'] = pd.to_datetime(transactions_df['transaction_date'])
    recent_date = transactions_df['transaction_date'].max()
    rfm = transactions_df.groupby('customer_id').agg({
        'transaction_date': lambda x: (recent_date - x.max()).days,
        'transaction_id': 'count',
        'amount': 'sum'
    }).reset_index()
    rfm.columns = ['customer_id', 'recency', 'frequency', 'monetary']
    
    customer_features = pd.merge(customers_df, rfm, on='customer_id', how='left').fillna(0)
    
    print("Loading ML models for predictions...")
    try:
        kmeans = joblib.load('models/kmeans_segmentation.joblib')
        scaler = joblib.load('models/rfm_scaler.joblib')
        xgb_model = joblib.load('models/xgboost_churn.joblib')
        rf_model = joblib.load('models/rf_clv.joblib')
        
        # Predictions
        rfm_scaled = scaler.transform(customer_features[['recency', 'frequency', 'monetary']])
        customer_features['segment'] = kmeans.predict(rfm_scaled)
        
        X_churn = customer_features[['age', 'annual_income', 'recency', 'frequency', 'monetary']]
        churn_probs = xgb_model.predict_proba(X_churn)[:, 1]
        customer_features['churn_probability'] = churn_probs
        
        X_rev = customer_features[['age', 'annual_income', 'recency', 'frequency', 'monetary']]
        predicted_clv = rf_model.predict(X_rev)
        customer_features['predicted_clv'] = predicted_clv
    except Exception as e:
        print(f"Error loading models or predicting: {e}")
        # Default values if models fail
        customer_features['segment'] = -1
        customer_features['churn_probability'] = 0.0
        customer_features['predicted_clv'] = 0.0

    print("Inserting customers into DB...")
    customers_to_insert = []
    for _, row in customer_features.iterrows():
        customer = models.Customer(
            customer_id=int(row['customer_id']),
            age=int(row['age']),
            gender=row['gender'],
            location=row['location'],
            annual_income=float(row['annual_income']),
            churned=int(row['churned']),
            recency=float(row['recency']),
            frequency=float(row['frequency']),
            monetary=float(row['monetary']),
            segment=int(row['segment']),
            predicted_clv=float(row['predicted_clv']),
            churn_probability=float(row['churn_probability'])
        )
        customers_to_insert.append(customer)
    
    # Bulk insert for speed
    db.bulk_save_objects(customers_to_insert)
    db.commit()
    
    print("Inserting transactions into DB...")
    transactions_to_insert = []
    for _, row in transactions_df.iterrows():
        transaction = models.Transaction(
            transaction_id=int(row['transaction_id']),
            customer_id=int(row['customer_id']),
            transaction_date=row['transaction_date'].to_pydatetime(),
            category=row['category'],
            amount=float(row['amount'])
        )
        transactions_to_insert.append(transaction)
    
    # Insert in chunks
    chunk_size = 10000
    for i in range(0, len(transactions_to_insert), chunk_size):
        db.bulk_save_objects(transactions_to_insert[i:i+chunk_size])
        db.commit()
    
    db.close()
    print("Ingestion complete!")

if __name__ == '__main__':
    ingest()
