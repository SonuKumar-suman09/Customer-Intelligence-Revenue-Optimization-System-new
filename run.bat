@echo off
echo Starting Backend Server on http://localhost:8000
start cmd /k "cd backend && uvicorn main:app --reload"

echo Starting Frontend Server on http://localhost:5173
start cmd /k "cd frontend && npm run dev"

echo Done! The Customer Intelligence System is now running.
