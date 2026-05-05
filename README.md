# 🌐 Language

- [English](README.md) (you are here)
- [**Español / Spanish**](README_ES.md)

---

# <center>🏨 Reservation System API </center>

Backend API for a hotel reservation and management platform built with **Django REST Framework**.  
Designed with a real-world architecture mindset, including **public vs admin separation**, **JWT authentication**, **role-based access control**, **rate limiting**, and strong **business rules validation** for reservations, room availability, and payments.

---

## 🌍 Live Demo (Deployed on Render)

### 📌 Swagger API Docs
https://sistema-de-reservas-4827.onrender.com/api/docs/

### 📌 Redoc Documentation
https://sistema-de-reservas-4827.onrender.com/api/schema/redoc/

---

## 🚀 Tech Stack

- **Python**
- **Django**
- **Django REST Framework**
- **PostgreSQL**
- **JWT Authentication (SimpleJWT)**
- **drf-spectacular** (Swagger/OpenAPI Documentation)
- **django-filter** (Advanced Filtering)
- **DRF Throttling / Rate Limiting**
- **Render Deployment**

---

## 🎯 Key Features

### 🛏️ Room Management
- Full room and room-type management for admins (CRUD).
- Room availability endpoint using real booking overlap logic.
- Room state management (active / inactive / maintenance).

### 📅 Reservation System
- Reservation creation with automatic total calculation.
- Prevents double booking with date overlap validation.
- Reservation lifecycle management:
  - confirmed
  - checked_in
  - cancelled
  - no_show
  - finished

### 💳 Payment System
- Payments linked to reservations.
- Prevents invalid payments using business logic rules.
- Tracks reservation balance and paid amounts.

---

# 🧠 Architecture & Code Quality

This project was structured using clean architecture principles inspired by **SOLID** and real backend scalability patterns.

### Clean separation of responsibilities:
- **Serializers** handle input validation + serialization.
- **ViewSets** expose endpoints and control API flow.
- **Services layer** handles business rules (ex: payments).
- **Mixins** share reusable logic across multiple endpoints.
- **Filters** isolate query filtering logic cleanly.

This avoids "fat views" and improves testability and maintainability.

---

# 🔐 Security & Best Practices

This API is designed with production-like security practices.

---

## ✅ Authentication (JWT)

Authentication is handled with **JWT tokens** using SimpleJWT.

Admins must authenticate using JWT to access protected endpoints.

---

## ✅ Role-Based Access Control (RBAC)

Custom permission classes enforce user roles:

- `BaseUserPermission` (active + authenticated)
- `IsSuperUser`
- `IsReceptionist`

Receptionist role is managed using Django Groups.

---

## ✅ Receptionist Role Migration

A migration automatically creates the `Receptionist` group, ensuring consistent environments in production.

---

## ✅ Public vs Admin Endpoint Separation

A key security design decision: **public endpoints do not expose full CRUD access**.

### Public endpoints:
- Room availability
- Reservation creation
- Reservation cancellation (token-based access)

### Admin endpoints:
- CRUD rooms
- CRUD room types
- Reservation management
- Payment management
- Controlled status transitions

This prevents exposing sensitive operations to unauthenticated users.

---

## ✅ Safe Reservation Status Transitions

Reservation status updates are controlled through a dedicated endpoint that enforces valid transitions:

- `confirmed → checked_in | cancelled | no_show`
- `checked_in → finished`

Invalid transitions are rejected.

This prevents inconsistent reservation states and improves system integrity.

---

## ✅ Anti-Spam Protection (Rate Limiting)

Public reservation endpoints include **throttling / rate limiting** to prevent abuse (spam reservation creation attempts).

This adds real-world API protection and demonstrates security-focused backend design.

---

# 🧠 Business Logic Integrity

## ✅ Prevent Double Booking (Overlap Validation)

Room availability is calculated using overlap logic:

```
python
check_in__lt = requested_check_out
check_out__gt = requested_check_in
```
This prevents multiple reservations from occupying the same room during overlapping dates.

---
## ✅ Financial Tracking (Computed Properties)

Reservations support computed billing logic:

- total_real = total_amount + extra_charges
- total_paid = sum of all payments
- balance = remaining amount

This allows real-world scenarios like minibar charges, damages, or additional services.

---

## ✅ Service Layer (Payments)

Payments use a dedicated service layer to enforce business rules:

- Prevent payments for finished reservations
- Prevent invalid payment amounts
- Prevent overpayment beyond reservation balance

This demonstrates scalable backend design.

---

## 🔍 Filtering System (Admin)

Admin reservation listing supports advanced filtering using django-filter:

- status
- room_id
- guest_document
- date range overlap

Example:
`GET /api/admin/reservations/?status=confirmed&room_id=10`

---
## 📍 Main Endpoints
### Public API
Room availability  
`GET /api/public/rooms/available/?room_type=3&check_in=2026-03-28&check_out=2026-03-30`  
Create reservation  
`POST /api/public/reservations/`  
Cancel reservation (token-based)  
`PATCH /api/public/reservations/{token}/cancel/`

### Admin API (JWT Protected)
Rooms CRUD  
`/api/admin/rooms/`  
RoomTypes CRUD  
`/api/admin/roomtypes/`  
Reservations management  
`/api/admin/reservations/`  
Change reservation status  
`PATCH /api/admin/reservations/{id}/change_status/`  
Payments  
`/api/admin/payments/`

---
## 🔑 Authentication Usage (JWT)
Login  
`POST /api/auth/login/`

Body:
```
{
    "email": "admin@mail.com",
    "password": "password"
}
```

Response:
```
{
    "access": "...",
    "refresh": "..."
}
```

---
# 🛠️ Local Setup
### Clone project
```
git clone <repo-url>
cd Sistema_de_Reservas
```
### Create virtual environment
```
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```
### Install dependencies
`pip install -r requirements.txt`

### Configure environment variables
Create .env file:
```
DEBUG=True
SECRET_KEY=your_secret_key
DATABASE_URL=postgres://user:password@localhost:5432/dbname
```
### Run migrations
`python manage.py migrate`
### Run server
`python manage.py runserver`

---
# 📌 Why this project stands out
This is not a basic CRUD API.

It demonstrates real backend engineering practices:

✅ JWT authentication and RBAC permissions  
✅ public/admin endpoint separation  
✅ throttling (rate limiting) to prevent abuse  
✅ validated reservation state transitions  
✅ double-booking prevention using overlap queries  
✅ payment service layer with business rules validation  
✅ clean architecture inspired by SOLID principles  
✅ production-ready documentation (Swagger + Redoc)  
✅ deployed and accessible live on Render

---
## 📬 Author

Developed by Verónica Sierra
Backend Developer | Django & REST API