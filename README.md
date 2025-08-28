# GIS PLATFORM

# (PASE 1): Authentication System

## Overview
A modular Django-based authentication system that supports multiple login methods, user verification, and secure session management.  
It is designed to provide a production-ready, extensible foundation for authentication in modern web applications.

## Features
- User registration with email and username
- Login with **email or username**
- Email verification flow
- Mobile verification via **OTP (One-Time Password)**
- Two-Factor Authentication (2FA) after login
- Password reset via **email**
- User profile management with profile picture upload
- Activity log for tracking user actions
- **Swagger & ReDoc API documentation**

## Tech Stack
- **Backend:** Django, Django REST Framework (DRF)  
- **Database:** PostgreSQL  
- **Cache & Queues:** Redis  
- **Background Tasks:** Celery  
- **Authentication:** JWT / DRF Tokens  
- **External Services:** Email provider (SMTP)

## Problem Solved
Authentication is a critical part of any application. Instead of rewriting it for every project, this reusable system solves common challenges such as:  
- Secure login across multiple identifiers (username, email) 
- Enforcing account verification (email)  
- Providing strong security with **2FA**  
- Maintaining user activity logs for auditing  

This system can serve as the foundation for any web or mobile project requiring secure authentication.

## In Progress / Upcoming Features:
- SMS integration for 2FA (currently only console-based)  
- User profile management  
- Disable/enable 2FA  
- Email change process with verification  
- Password reset via email & mobile OTP  
- Advanced logging system (partially implemented)  


## Installation & Setup
```bash
# Clone repository
git clone https://github.com/mbnahmadi/gisplatform.git
cd gisplatform

# Create virtual environment & install dependencies
pip install -r requirements.txt

# Create a database in postgres
# Configure your PostgreSQL database settings in settings.py

# Apply migrations
python manage.py migrate

# Run server
python manage.py runserver
```
## API Documentation

Interactive API documentation is available via **Swagger UI**:
```bash
- Swagger UI: `http://localhost:8000/swagger/`
- ReDoc: `http://localhost:8000/redoc/`
```
The API schema is generated automatically using [drf-spectacular].