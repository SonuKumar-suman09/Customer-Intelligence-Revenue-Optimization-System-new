# Customer Intelligence & Revenue Optimization System

This project is a production-grade Data Science and Full Stack Web Application that predicts customer churn, performs customer segmentation, and forecasts Customer Lifetime Value (CLV).

## Features
- **Machine Learning**: 
  - K-Means Clustering for RFM Customer Segmentation
  - XGBoost for Customer Churn Prediction
  - Random Forest Regressor for CLV Prediction
- **Backend**: FastAPI, SQLAlchemy (SQLite/MySQL)
- **Frontend**: React, Vite, Tailwind CSS, Recharts, Framer Motion
- **Deployment**: Docker, Docker Compose

## Quick Start

### 1. Generate Data & Train Models
Navigate to the `backend` directory and generate synthetic data, train the models, and ingest data into SQLite.
```bash
cd backend
python -m venv venv
source venv/Scripts/activate  # On Windows
pip install -r requirements.txt

# Generate Data (CSVs)
python data_generator.py

# Train Models
python ml_pipeline.py

# Ingest data into SQLite Database
python ingest_data.py
```

### 2. Run Locally (without Docker)
Start the backend:
```bash
cd backend
uvicorn main:app --reload
```

Start the frontend:
```bash
cd frontend
npm install
npm run dev
```

### 3. Run with Docker Compose
```bash
docker-compose up --build
```
Frontend runs on `http://localhost:4173`, Backend API runs on `http://localhost:8000`.
