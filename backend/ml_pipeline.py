import pandas as pd
import numpy as np
import os
import joblib
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, mean_squared_error

def train_models():
    print("Loading data...")
    customers_df = pd.read_csv('../data/customers.csv')
    transactions_df = pd.read_csv('../data/transactions.csv')
    
    # Ensure models dir exists
    os.makedirs('models', exist_ok=True)
    
    # 1. RFM Analysis & Segmentation
    print("Training Customer Segmentation Model...")
    # Convert transaction date to datetime
    transactions_df['transaction_date'] = pd.to_datetime(transactions_df['transaction_date'])
    
    # Calculate R, F, M
    recent_date = transactions_df['transaction_date'].max()
    rfm = transactions_df.groupby('customer_id').agg({
        'transaction_date': lambda x: (recent_date - x.max()).days,
        'transaction_id': 'count',
        'amount': 'sum'
    }).reset_index()
    rfm.columns = ['customer_id', 'recency', 'frequency', 'monetary']
    
    # Merge with customers
    customer_features = pd.merge(customers_df, rfm, on='customer_id', how='left').fillna(0)
    
    # K-Means Clustering
    scaler = StandardScaler()
    rfm_scaled = scaler.fit_transform(customer_features[['recency', 'frequency', 'monetary']])
    kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
    customer_features['segment'] = kmeans.fit_predict(rfm_scaled)
    
    joblib.dump(kmeans, 'models/kmeans_segmentation.joblib')
    joblib.dump(scaler, 'models/rfm_scaler.joblib')
    print("Segmentation Model saved.")
    
    # 2. Churn Prediction (XGBoost)
    print("Training Churn Prediction Model...")
    # Features for churn: age, income, recency, frequency, monetary
    X_churn = customer_features[['age', 'annual_income', 'recency', 'frequency', 'monetary']]
    y_churn = customer_features['churned']
    
    X_train_c, X_test_c, y_train_c, y_test_c = train_test_split(X_churn, y_churn, test_size=0.2, random_state=42)
    
    xgb_model = XGBClassifier(use_label_encoder=False, eval_metric='logloss', random_state=42)
    xgb_model.fit(X_train_c, y_train_c)
    
    churn_preds = xgb_model.predict(X_test_c)
    print(f"Churn Accuracy: {accuracy_score(y_test_c, churn_preds):.4f}")
    
    joblib.dump(xgb_model, 'models/xgboost_churn.joblib')
    print("Churn Model saved.")
    
    # 3. Revenue Prediction / Customer Lifetime Value (Random Forest Regressor)
    print("Training CLV Prediction Model...")
    # We will predict next year's monetary value based on current features
    # Synthetic target: monetary + some random growth based on income
    customer_features['target_clv'] = customer_features['monetary'] * (1 + customer_features['annual_income']/500000) + np.random.normal(100, 50, len(customer_features))
    
    X_rev = customer_features[['age', 'annual_income', 'recency', 'frequency', 'monetary']]
    y_rev = customer_features['target_clv']
    
    X_train_r, X_test_r, y_train_r, y_test_r = train_test_split(X_rev, y_rev, test_size=0.2, random_state=42)
    
    rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
    rf_model.fit(X_train_r, y_train_r)
    
    rev_preds = rf_model.predict(X_test_r)
    print(f"CLV MSE: {mean_squared_error(y_test_r, rev_preds):.4f}")
    
    joblib.dump(rf_model, 'models/rf_clv.joblib')
    print("CLV Model saved.")
    print("All models trained and saved successfully.")

if __name__ == "__main__":
    train_models()
