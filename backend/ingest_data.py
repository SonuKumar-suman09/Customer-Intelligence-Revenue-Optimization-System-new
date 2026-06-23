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
        customers_df = pd.read_csv('../data/Mall_Customers.csv')
        customers_df.columns = ['customer_id', 'gender', 'age', 'annual_income', 'spending_score']
    except FileNotFoundError:
        print("CSV file not found.")
        return

    db = SessionLocal()
    
    # Check if data already exists
    if db.query(models.Customer).first():
        print("Data already ingested. Please delete sql_app.db to re-ingest.")
        db.close()
        return

    print("Loading ML models for predictions...")
    try:
        kmeans = joblib.load('models/kmeans_segmentation.joblib')
        scaler = joblib.load('models/features_scaler.joblib')
        xgb_model = joblib.load('models/xgboost_churn.joblib')
        rf_model = joblib.load('models/rf_clv.joblib')
        
        # Predictions
        features_scaled = scaler.transform(customers_df[['age', 'annual_income', 'spending_score']])
        customers_df['segment'] = kmeans.predict(features_scaled)
        
        X_ml = customers_df[['age', 'annual_income', 'spending_score']]
        churn_probs = xgb_model.predict_proba(X_ml)[:, 1]
        customers_df['churn_probability'] = churn_probs
        
        predicted_clv = rf_model.predict(X_ml)
        customers_df['predicted_clv'] = predicted_clv
    except Exception as e:
        print(f"Error loading models or predicting: {e}")
        customers_df['segment'] = -1
        customers_df['churn_probability'] = 0.0
        customers_df['predicted_clv'] = 0.0

    print("Inserting customers into DB...")
    customers_to_insert = []
    for _, row in customers_df.iterrows():
        # Re-synthesize churn label for database so it looks realistic in UI if churn_prob > 0.5
        churned = 1 if row['churn_probability'] > 0.6 else 0
        
        customer = models.Customer(
            customer_id=int(row['customer_id']),
            age=int(row['age']),
            gender=row['gender'],
            annual_income=float(row['annual_income']),
            spending_score=float(row['spending_score']),
            churned=churned,
            segment=int(row['segment']),
            predicted_clv=float(row['predicted_clv']),
            churn_probability=float(row['churn_probability'])
        )
        customers_to_insert.append(customer)
    
    # Bulk insert for speed
    db.bulk_save_objects(customers_to_insert)
    db.commit()
    db.close()
    print("Ingestion complete!")

if __name__ == '__main__':
    ingest()
