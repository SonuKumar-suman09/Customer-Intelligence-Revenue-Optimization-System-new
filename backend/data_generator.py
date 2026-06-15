import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta

def generate_mock_data():
    np.random.seed(42)
    n_customers = 5000
    
    # 1. Customers Data
    customer_ids = np.arange(1, n_customers + 1)
    ages = np.random.normal(35, 10, n_customers).astype(int)
    ages = np.clip(ages, 18, 80)
    genders = np.random.choice(['Male', 'Female', 'Other'], n_customers, p=[0.48, 0.48, 0.04])
    locations = np.random.choice(['New York', 'Los Angeles', 'Chicago', 'Houston', 'Miami', 'Seattle', 'Austin'], n_customers)
    
    # Base spend capacity
    income = np.random.normal(70000, 25000, n_customers)
    income = np.clip(income, 30000, 200000)
    
    # Churn probability (synthetic logic)
    churn_prob = np.where(ages > 60, 0.2, 0.05)
    churn_prob = np.where(income < 40000, churn_prob + 0.1, churn_prob)
    churn = np.random.binomial(1, churn_prob)
    
    customers_df = pd.DataFrame({
        'customer_id': customer_ids,
        'age': ages,
        'gender': genders,
        'location': locations,
        'annual_income': income,
        'churned': churn
    })
    
    # 2. Transactions Data
    n_transactions = 50000
    t_customer_ids = np.random.choice(customer_ids, n_transactions)
    
    # Generate dates over the last 2 years
    end_date = datetime.now()
    start_date = end_date - timedelta(days=730)
    t_dates = [start_date + timedelta(days=np.random.randint(0, 730)) for _ in range(n_transactions)]
    
    # Products
    categories = ['Electronics', 'Clothing', 'Home', 'Beauty', 'Sports']
    t_categories = np.random.choice(categories, n_transactions)
    
    t_amounts = np.random.exponential(100, n_transactions)
    t_amounts = np.clip(t_amounts, 5, 2000)
    
    transactions_df = pd.DataFrame({
        'transaction_id': np.arange(1, n_transactions + 1),
        'customer_id': t_customer_ids,
        'transaction_date': t_dates,
        'category': t_categories,
        'amount': t_amounts
    })
    
    # Ensure data dir exists
    os.makedirs('../data', exist_ok=True)
    
    customers_df.to_csv('../data/customers.csv', index=False)
    transactions_df.to_csv('../data/transactions.csv', index=False)
    print("Mock data generated in ../data/")

if __name__ == "__main__":
    generate_mock_data()
