from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import timedelta
import models, schemas, auth, database
import pandas as pd
import joblib
import os

# Initialize DB
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Customer Intelligence API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Auth Endpoints
@app.post("/token", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Users endpoint
@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Dashboard Endpoints
@app.get("/api/dashboard/summary")
def get_dashboard_summary(db: Session = Depends(get_db)):
    total_customers = db.query(models.Customer).count()
    
    # Calculate total revenue from transactions
    total_revenue = db.query(models.Transaction.amount).scalar() or 0.0
    
    # In a real scenario, active_users might be based on recent transactions
    active_users = db.query(models.Customer).filter(models.Customer.churned == 0).count()
    
    churn_rate = 0
    if total_customers > 0:
        churn_rate = round((total_customers - active_users) / total_customers, 4)
        
    avg_ltv = 0
    if total_customers > 0:
        # Average predicted clv
        from sqlalchemy.sql import func
        avg_ltv_result = db.query(func.avg(models.Customer.predicted_clv)).scalar()
        avg_ltv = round(avg_ltv_result, 2) if avg_ltv_result else 0

    return {
        "total_customers": total_customers,
        "total_revenue": round(total_revenue, 2),
        "active_users": active_users,
        "churn_rate": churn_rate,
        "avg_ltv": avg_ltv
    }

@app.get("/api/customers")
def get_customers(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    customers = db.query(models.Customer).offset(skip).limit(limit).all()
    # Map to schema required by frontend
    result = []
    for c in customers:
        
        # Determine risk
        risk = "Low"
        if c.churn_probability > 0.7:
            risk = "High"
        elif c.churn_probability > 0.4:
            risk = "Medium"
            
        # Determine Segment
        segment_map = {0: "New", 1: "At Risk", 2: "Loyal", 3: "High Value", -1: "Unknown"}
        
        result.append({
            "id": c.customer_id,
            "name": f"Customer {c.customer_id}",
            "email": f"customer{c.customer_id}@example.com",
            "segment": segment_map.get(c.segment, "Unknown"),
            "clv": f"${c.predicted_clv:,.2f}",
            "churnRisk": risk,
            "status": "Inactive" if c.churned else "Active"
        })
    return result

# Include ML prediction endpoints or more CRUD here
@app.get("/api/customers/predict-churn/{customer_id}")
def predict_churn(customer_id: int, db: Session = Depends(get_db)):
    try:
        model = joblib.load('models/xgboost_churn.joblib')
        # In a real scenario, fetch customer features from DB and predict
        # For now, return mock
        return {"customer_id": customer_id, "churn_probability": 0.15, "risk_level": "Low"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
