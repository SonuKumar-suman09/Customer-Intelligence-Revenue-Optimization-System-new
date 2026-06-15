# Interview Preparation Q&A

This document contains expected questions from recruiters/technical panels regarding your Customer Intelligence system, along with answers you can use.

## 1. Tell me about this project and your role in it.
**Answer:** I built an end-to-end Customer Intelligence and Revenue Optimization platform. It acts as a full-stack SaaS product. I acted as a Full-Stack Developer and Data Scientist. I created the frontend using React, Vite, and Tailwind CSS with a modern Glassmorphism design. For the backend, I used FastAPI for high performance and built REST APIs to connect to a SQLite/MySQL database using SQLAlchemy. On the data science side, I engineered an ML pipeline that uses K-Means for customer segmentation (based on RFM analysis), XGBoost to predict churn probability, and a Random Forest Regressor to forecast Customer Lifetime Value (CLV).

## 2. Why did you choose FastAPI over Flask or Django?
**Answer:** I chose FastAPI because it is extremely fast and built on modern Python standards like type hints and Pydantic. This allowed me to automatically generate Swagger UI documentation and have built-in request validation. Since the backend frequently runs machine learning models for inference, the asynchronous capabilities and high throughput of FastAPI were critical for performance.

## 3. How does your Churn Prediction model work?
**Answer:** The churn model uses XGBoost. I engineered features like customer age, annual income, and behavioral RFM (Recency, Frequency, Monetary) data from their past transactions. The XGBoost classifier is trained on this data to output a churn probability between 0 and 1. Customers with a probability > 0.7 are flagged as "High Risk," allowing business users to target them with retention campaigns.

## 4. How did you structure your Database and why?
**Answer:** I used a relational model using SQLAlchemy as an ORM. The primary tables are `users` (for authentication), `customers` (storing demographic and ML predictions), and `transactions` (storing raw purchase history). A relational database was chosen because financial transaction data is highly structured, and ACID compliance is necessary for business data.

## 5. How is the application deployed?
**Answer:** The application is containerized using Docker. I wrote Dockerfiles for both the React frontend and FastAPI backend, and orchestrated them using `docker-compose`. This ensures the application can be easily spun up on any environment (like AWS EC2 or DigitalOcean) without environment discrepancies.
