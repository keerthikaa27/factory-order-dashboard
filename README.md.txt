# Factory Order Management System

A lightweight, practical web application built to simplify how factories manage sales orders, pending dispatches, and delivery analytics using structured CSV data.

This system replaces manual Excel tracking with a clean dashboard that allows real-time searching, filtering, and financial analysis — all while maintaining a scalable and secure backend architecture.

---

## 📌 What this project does

The application allows factory staff to:

* Upload Sales Order and Delivery CSV reports
* View and search all orders from a single dashboard
* Track pending/open orders separately
* Analyse sales based on Financial Year
* Filter orders by customer, product, serial number, or status
* Control access with role-based authentication

All data processing happens server-side with a modular API and is visualised through a React-based interface.

---

## 🧱 Core Features

### 1. CSV Data Ingestion

* Supports two factory report types:

  * Sales Order Outstanding CSV
  * Delivery Report CSV
* Uploaded files are stored in dedicated folders
* Data is parsed and normalised into a unified orders structure
* Admin-only access for ingestion endpoints

---

### 2. Authentication & Roles

* Secure login system with JWT tokens
* Role-based access control:

  * Admin → Can upload and manage CSVs
  * User → View-only access to dashboard and analytics
* Session persistence via local storage

---

### 3. Search & Filter Dashboard

Users can search orders using:

* PO Number
* Serial Number
* Part Number
* Customer Name
* Dispatch Status (Pending / Dispatched)

Includes:

* Global search with debounce
* Advanced filter controls
* Clean results table with status indicators

---

### 4. Open Orders View

* Displays only pending orders
* Highlights:

  * Today’s open orders
  * Orders grouped by customer / product
* Helps operations teams prioritise dispatch planning

---

### 5. Sales & Delivery Analytics

* Financial Year selector
* Automatically recalculates based on FY
* Displays:

  * Total Sales Amount
  * Total Quantity Sold
  * Product-wise sales chart
  * Customer-wise sales chart

Figures dynamically update when the financial year changes.

---

## 🏗️ System Architecture

Frontend (React + TypeScript)
→ API Layer (FastAPI)
→ Data Processing Engine
→ Structured Order Models
→ CSV File Storage

The backend follows a modular structure with:

* Separate routers for ingestion, analytics, and authentication
* Data abstraction layer for future DB or external integrations

---

## 🔧 Tech Stack

### Frontend

* React + TypeScript
* Tailwind CSS
* Framer Motion
* Axios

### Backend

* FastAPI
* Python
* Pandas for data processing
* JWT for authentication

### Storage

* CSV-based structured storage
* Folder-based ingestion pipeline

---

## Folder Structure (Simplified)

```
backend/
 ├── app/
 │   ├── api/
 │   │   ├── v1/
 │   │   │   ├── ingestion.py
 │   │   │   ├── analytics.py
 │   │   │   └── auth.py
 │   ├── core/
 │   ├── models/
 │   └── main.py
 └── data/
     ├── sales_orders/
     └── delivery_reports/

frontend/
 ├── src/
 │   ├── pages/
 │   ├── components/
 │   └── api/
```

---

## Installation & Setup

### Prerequisites

* Node.js
* Python 3.9+
* npm / pip

### Backend Setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Access:

* Frontend: [http://localhost:5173](http://localhost:5173)
* Backend API: [http://localhost:8000](http://localhost:8000)

---

## Environment Variables

Create a `.env` file in backend:

```
SECRET_KEY=your_secret_key
ACCESS_TOKEN_EXPIRE_MINUTES=60
UPLOAD_DIR=data/
```

---

## Implementation Status

✅ CSV Upload & Parsing
✅ Unified Order Data Model
✅ Authentication & JWT
✅ Role-based access
✅ Dashboard Search
✅ Open Orders View
✅ Sales Analytics by Financial Year
✅ Responsive UI
✅ Environment-based config

Planned future enhancement:

* IMAP-based automatic CSV import from factory email inbox

---

## Future Enhancements

* Automatic email ingestion using IMAP
* Scheduled background data sync
* Export reports to Excel/PDF
* Role hierarchy expansion
* Notification system for delayed orders

---

## Author Notes

This project was designed with real factory workflows in mind and focuses on practicality over complexity. The goal was not just to build a tool, but to create a system that genuinely reduces operational friction and improves clarity in daily order handling.

Every feature has been implemented gradually with scalability and maintainability as priorities.

---

## Support

For any improvements or feature suggestions, feel free to fork or extend the system. This platform is intentionally structured to allow smooth future expansion.

---

**Factory Order Management System**
*A clean solution for complex factory operations.*
