# HRM Agriculture - Fullstack Starter Project
This project is a starter full-stack HRM system for an agriculture company.
It includes:
- Backend: Flask REST API with JWT auth, RBAC, SQLAlchemy models (SQLite by default)
- Frontend: React single-page app (sources only) that consumes the API
- Database: SQLite file `hrm.db` (initialized on first run) and an optional seed script

## Quick start (backend)
- Create a Python 3.9+ virtual environment
  ```bash
  python -m venv venv
  source venv/bin/activate   # or venv\Scripts\activate on Windows
  pip install -r backend/requirements.txt
  ```
- Run the backend API:
  ```bash
  cd backend
  export FLASK_APP=run.py
  export FLASK_ENV=development
  flask run --host=0.0.0.0 --port=5000
  ```
- The API will be at http://127.0.0.1:5000

## Quick start (frontend)
- Install Node.js (16+)
- From `frontend` folder run:
  ```bash
  cd frontend
  npm install
  npm start
  ```
- The React app (development) will run at http://localhost:3000 and proxy API requests to port 5000.

## Notes
- This is a starter implementation and not production hardened.
- Extend with biometric integrations, mobile sync, advanced payroll rules, and secure production deployment.
