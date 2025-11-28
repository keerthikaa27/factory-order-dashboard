# Frontend README – Factory Order Management

## Overview

The frontend of the Factory Order Management Dashboard provides a clean, minimal, and operationally-focused user interface for interacting with factory order data. It allows users to search, filter, view open orders, and analyze sales reports in real-time using data sourced from uploaded CSV files.

The UI is designed to be lightweight, responsive, and aligned with a calm beige & brown professional theme for ease of long operational use.

---

## Tech Stack

* React + TypeScript
* Vite
* Tailwind CSS
* Framer Motion (for subtle UI animations)
* Axios (API communication)
* React Router DOM

---

## Key Features

* Landing Page with feature overview and navigation
* Search Interface with:

  * Global search (PO / Serial / Part / Customer)
  * Individual filters
  * Dispatch status filter
* Open Orders View (pending only)
* Sales Analytics Dashboard

  * Financial year selector
  * Product-wise and Customer-wise charts
* Mobile responsive layout
* Visual status indicators (Pending / Dispatched)

---

## Folder Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── SearchOrders.tsx
│   │   ├── OpenOrders.tsx
│   │   ├── SalesAnalytics.tsx
│   │   └── ...
│   ├── pages/
│   │   ├── LandingPage.tsx
│   │   ├── Dashboard.tsx
│   │   └── Login.tsx
│   ├── api/
│   │   └── client.ts
│   └── styles/
│       └── global.css
```

---

## Environment Variables

Create a `.env` file in frontend root:

```
VITE_API_BASE_URL=http://localhost:8000
```

---

## Running the Frontend

```
cd frontend
npm install
npm run dev
```

The app will run at:
[http://localhost:5173](http://localhost:5173)

---

## Styling System

* Beige base background: #f6efe6
* Brown primary: #6f4e37
* Cards and inputs use soft rounded edges for visual clarity
* Typography optimized for readability

---

## Notes

* Ensure backend is running before testing search or analytics
* Mobile testing recommended using Chrome DevTools responsive mode

---
