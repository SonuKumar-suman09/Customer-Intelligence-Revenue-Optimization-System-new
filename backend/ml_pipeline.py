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
    customers_df = pd.read_csv('../data/Mall_Customers.csv')
    
    # Rename columns to match our schema
    customers_df.columns = ['customer_id', 'gender', 'age', 'annual_income', 'spending_score']
    
    os.makedirs('models', exist_ok=True)
    
    # 1. Customer Segmentation
    print("Training Customer Segmentation Model...")
    scaler = StandardScaler()
    features_scaled = scaler.fit_transform(customers_df[['age', 'annual_income', 'spending_score']])
    kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
    customers_df['segment'] = kmeans.fit_predict(features_scaled)
    
    joblib.dump(kmeans, 'models/kmeans_segmentation.joblib')
    joblib.dump(scaler, 'models/features_scaler.joblib')
    print("Segmentation Model saved.")
    
    # 2. Synthesize Churn Label for ML Training
    print("Synthesizing targets and Training Churn Prediction Model...")
    # Low spending score + older age = higher chance of churn (just for proxy demonstration)
    np.random.seed(42)
    base_prob = np.where(customers_df['spending_score'] < 40, 0.6, 0.1)
    base_prob = np.where(customers_df['age'] > 40, base_prob + 0.2, base_prob)
    base_prob = np.clip(base_prob, 0, 1)
    customers_df['churned'] = np.random.binomial(1, base_prob)
    
    X_churn = customers_df[['age', 'annual_income', 'spending_score']]
    y_churn = customers_df['churned']
    
    X_train_c, X_test_c, y_train_c, y_test_c = train_test_split(X_churn, y_churn, test_size=0.2, random_state=42)
    
    xgb_model = XGBClassifier(use_label_encoder=False, eval_metric='logloss', random_state=42)
    xgb_model.fit(X_train_c, y_train_c)
    
    churn_preds = xgb_model.predict(X_test_c)
    print(f"Churn Proxy Accuracy: {accuracy_score(y_test_c, churn_preds):.4f}")
    
    joblib.dump(xgb_model, 'models/xgboost_churn.joblib')
    print("Churn Model saved.")
    
    # 3. Synthesize CLV target and train Regressor
    print("Training CLV Prediction Model...")
    customers_df['target_clv'] = customers_df['annual_income'] * 1000 * (customers_df['spending_score'] / 100) * 5 + np.random.normal(5000, 2000, len(customers_df))
    customers_df['target_clv'] = np.clip(customers_df['target_clv'], 0, None) # Ensure positive
    
    X_rev = customers_df[['age', 'annual_income', 'spending_score']]
    y_rev = customers_df['target_clv']
    
    X_train_r, X_test_r, y_train_r, y_test_r = train_test_split(X_rev, y_rev, test_size=0.2, random_state=42)
    
    rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
    rf_model.fit(X_train_r, y_train_r)
    
    rev_preds = rf_model.predict(X_test_r)
    print(f"CLV Proxy MSE: {mean_squared_error(y_test_r, rev_preds):.4f}")
    
    joblib.dump(rf_model, 'models/rf_clv.joblib')
    print("CLV Model saved.")
    print("All models trained and saved successfully.")

if __name__ == "__main__":
    train_models()
