
# Backend README – Factory Order Management

## Overview

The backend powers the core logic of the Factory Order Management System. It handles CSV ingestion, authentication, data processing, filtering, and analytics generation through a modular FastAPI-based architecture.

It is designed with scalability and future IMAP integration in mind.

---

## Tech Stack

* FastAPI
* Python 3.10+
* Pandas (CSV processing)
* JWT Authentication
* PostgreSQL / SQLite (configurable)
* Uvicorn

---

## Core Responsibilities

* User authentication & role management
* CSV ingestion pipeline
* Order searching & filtering
* Sales analytics generation
* Financial year calculations
* Data abstraction layer for future IMAP integration

---

## Folder Structure

```
backend/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── ingestion.py
│   │       ├── orders.py
│   │       └── analytics.py
│   ├── core/
│   │   ├── config.py
│   │   └── security.py
│   ├── models/
│   ├── services/
│   └── main.py
├── csv_data/
└── .env
```

---

## Authentication Flow

* JWT-based login
* Role system: admin / user
* Secured endpoints using dependency injection
* Token validation on each API call

---

## CSV Processing Pipeline

```
CSV File → Parser → Validator → Normalizer → Database
```

Supports:

* Delivery Report (Dispatched orders)
* Sales Order Outstanding (Pending orders)

Daily data ingestion logic ensures updated snapshots without data corruption.

---

## Important Environment Variables (.env)

```
SECRET_KEY=your_secret_key
DATABASE_URL=postgresql://user:password@localhost/dbname
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

---

## Running the Backend

```
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Backend runs at:
[http://localhost:8000], [https://factory-order-dashboard.onrender.com/docs]

---

## API Highlights

* GET /orders/search
* GET /orders/open
* GET /analytics/summary
* POST /auth/login
* POST /ingest/csv

---

## Future-Ready Design

* Abstracted data source layer
* IMAP-ready structure
* Modular services for easy extension
* Config-driven environment handling

---

## Notes

* .env must NOT be committed
* Use .env.example for setup reference
* Logging enabled for debugging and monitoring

## Screenshots

![alt text](image.png)
![alt text](image-1.png)
![alt text](image-2.png)
