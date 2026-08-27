# SmartServe

Smart Multi-Service Booking and Management System  
AI-powered full-stack service marketplace.

---

## 👥 Team
- **Pushkar Kanjani** — Provider ecosystem, integration, cloud and deployment
- **Aastha** — Customer ecosystem, backend and AI/ML

---

## 🚀 Tech Stack
- **Frontend:** React, TypeScript, Tailwind CSS, Vite, Lucide Icons
- **Backend:** FastAPI, Python, SQLAlchemy, Uvicorn, Pydantic
- **Database:** PostgreSQL (Primary), MongoDB (Media/Metadata)
- **Security:** JWT authentication, RBAC, encrypted credentials

---

## 🛠️ Local Setup Guide

### 1. Environment Configuration
Copy the example environment template and configure your local environment variables:
```bash
cp .env.example .env
```
Update `.env` with your local database URL, secrets, and API keys.

### 2. Backend Setup
```bash
cd backend
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

### 3. Frontend Setup
```bash
cd admin-frontend
npm install
npm run dev
```

The admin portal will be available at `http://localhost:5173`.
Backend API docs will be accessible at `http://127.0.0.1:8000/docs`.

---

## 🔒 Security Policy
- **Never commit `.env` or any production secrets/credentials to git.**
- Refer to `.env.example` for the required configuration keys.
