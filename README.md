# 🐾 PawScout Backend API

> **Modern, production-ready REST API for animal adoption platform built with FastAPI, PostgreSQL, and cloud-native technologies**

![Python](https://img.shields.io/badge/Python-3.11.9-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115.5-009688?logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-316192?logo=postgresql&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-Authentication-000000?logo=json-web-tokens&logoColor=white)
![Cloudinary](https://img.shields.io/badge/Cloudinary-Media_CDN-3448C5?logo=cloudinary&logoColor=white)

### 🚀 **[Live Demo](https://paw-scout.vercel.app/)** | **[View Full Project](https://paw-scout.vercel.app/)**

> **Full-Stack Deployment**: Frontend on Vercel + Backend API on Render

## 📋 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [Tech Stack & Architecture](#️-tech-stack--architecture)
- [Project Structure](#-project-structure)
- [Database Schema](#-database-schema)
- [API Endpoints](#-api-endpoints)
- [Security Implementation](#-security-implementation)
- [Deployment](#-deployment)
- [Installation & Setup](#-installation--setup)
- [Technical Highlights](#-technical-highlights)

---

## 🎯 Overview

**PawScout Backend** is a comprehensive, enterprise-grade REST API that powers an animal adoption platform. Built with modern Python async patterns and type safety, this API demonstrates production-ready development practices including role-based authentication, media management, database relationships, and deployment optimization.

### 🌐 **[View Live Application →](https://paw-scout.vercel.app/)**

**Deployed Production Stack:**

- 🎨 **Frontend**: Next.js 15 + TypeScript → Vercel
- ⚡ **Backend API**: FastAPI + PostgreSQL → Render
- ☁️ **Media CDN**: Cloudinary
- 🔒 **Authentication**: JWT with Argon2 hashing

### **Why This Project Stands Out:**

- ✅ **Type-Safe**: Full SQLModel integration with Pydantic validation
- ✅ **Secure**: JWT authentication with Argon2 password hashing
- ✅ **Scalable**: Async/await patterns, connection pooling, CDN integration
- ✅ **Production-Ready**: Deployed with Gunicorn + Uvicorn workers
- ✅ **Well-Documented**: OpenAPI/Swagger with detailed endpoint descriptions
- ✅ **Clean Architecture**: Modular router design with dependency injection

---

### 🔐 **Authentication & Security**

- **JWT-based authentication** with configurable token expiration (14-day default)
- **Role-Based Access Control (RBAC)** - Admin/User permissions with middleware
- **Argon2 password hashing** via `pwdlib` (industry-standard security)
- **OAuth2 password bearer flow** with FastAPI dependencies
- **Email validation** with `email-validator`
- **Input sanitization** and field-level validation

### 🐶 **Animal Management System**

- Full **CRUD operations** with comprehensive validation
- **Multi-media support** (images & videos via Cloudinary CDN)
- **Status workflow** tracking (available → pending → adopted)
- **Foreign key relationships** linking adoptions to animals
- **Detailed profiles** with breed, age, size, temperament, training status
- **Automatic status updates** when adoption applications submitted

### 📋 **Application Processing**

- **Adoption applications** with extensive form validation (14+ fields)
- **Volunteer registration** with availability scheduling and interests
- **Contact form** with subject categorization
- **Newsletter subscriptions** with email storage
- **Application status tracking** (pending, approved, rejected)
- **Date/time stamping** for all submissions

### 👨‍💼 **Admin Dashboard**

- **User management** (promote/demote admin, delete users)
- **Dashboard analytics** (total counts, overview stats)
- **Application review** interface for all form types
- **Settings management** for shelter configuration
- **Logo upload** and branding customization
- **Self-protection** (admins cannot demote/delete themselves)

### 📸 **Cloud Media Management**

- **Cloudinary integration** for image/video hosting
- **Automatic optimization** (quality: auto, format conversion)
- **Multi-file uploads** with async processing
- **CDN delivery** for optimal performance
- **Public ID tracking** for resource management and deletion
- **Metadata storage** (format, dimensions, file size)

---

## 🛠️ Tech Stack & Architecture

### **Core Technologies**

| Technology     | Purpose                           | Version |
| -------------- | --------------------------------- | ------- |
| **FastAPI**    | Modern async web framework        | 0.115.5 |
| **Python**     | Backend language                  | 3.11.9  |
| **SQLModel**   | SQL ORM with Pydantic integration | 0.0.22  |
| **PostgreSQL** | Relational database               | 14+     |
| **Pydantic**   | Data validation & settings        | 2.10.5  |
| **Uvicorn**    | ASGI server                       | 0.32.1  |
| **Gunicorn**   | Production WSGI server            | 23.0.0  |

### **Security & Authentication**

| Technology           | Purpose                      |
| -------------------- | ---------------------------- |
| **PyJWT**            | JSON Web Token handling      |
| **pwdlib[argon2]**   | Password hashing with Argon2 |
| **python-multipart** | Form data parsing            |
| **email-validator**  | Email validation             |

### **Cloud Services**

| Service            | Purpose                        |
| ------------------ | ------------------------------ |
| **Cloudinary**     | Image/video CDN storage        |
| **Render/Railway** | Production deployment platform |
| **PostgreSQL**     | Managed database service       |

### **Architecture Patterns**

- ✅ **Dependency Injection** - FastAPI's `Depends()` for session management and auth
- ✅ **Repository Pattern** - SQLModel sessions with context managers
- ✅ **Router-based Modularization** - Separate routers for each domain
- ✅ **Middleware Pipeline** - CORS, authentication, exception handling
- ✅ **OpenAPI Documentation** - Auto-generated Swagger UI
- ✅ **Environment-based Configuration** - `.env` with `pydantic-settings`

---

## 📁 Project Structure

```
backend/
├── 📄 main.py                      # Application entrypoint (compatibility)
├── 📄 requirements.txt             # Python dependencies
├── 📄 runtime.txt                  # Python version for deployment
├── 📄 start.sh                     # Production startup script (Gunicorn)
├── 📄 .env                         # Environment variables (not in git)
└── app/
    ├── 📄 main.py                  # FastAPI app initialization & routing
    ├── 📄 database.py              # PostgreSQL connection & SQLModel setup
    ├── 📄 auth.py                  # JWT token generation & password hashing
    ├── 📄 dependencies.py          # Reusable dependencies (auth middleware)
    ├── 📄 cloudinary_config.py     # Cloudinary upload/delete utilities
    │
    ├── 📁 routers/                 # Domain-specific API endpoints
    │   ├── animals.py              # Animal CRUD (GET, POST, PUT, DELETE)
    │   ├── adopt.py                # Adoption applications
    │   ├── volunteer.py            # Volunteer management
    │   ├── contact.py              # Contact form messages
    │   ├── users.py                # User registration & login
    │   └── subs.py                 # Newsletter subscriptions
    │
    ├── 📁 internal/                # Protected admin-only endpoints
    │   └── admin.py                # User management, dashboard, settings
    │
    ├── 📁 models/                  # Database models
    │   └── settings.py             # Shelter settings configuration
    │
    └── 📁 cloudinary/              # Media handling
        └── routers/
            └── media.py            # Media upload/delete endpoints
```

### **File Responsibilities**

| File                  | Purpose                                                              |
| --------------------- | -------------------------------------------------------------------- |
| `app/main.py`         | FastAPI instance, CORS setup, router registration, DB initialization |
| `app/database.py`     | Database engine, session management, table creation                  |
| `app/auth.py`         | Password hashing (Argon2), JWT token creation/validation             |
| `app/dependencies.py` | Authentication middleware, admin verification                        |
| `routers/*`           | Business logic for each domain (animals, users, etc.)                |
| `internal/admin.py`   | Admin-only operations with authorization checks                      |

---

## 🗃️ Database Schema

### **Entity Relationship Diagram**

```
┌─────────────────┐
│    PawUser      │
├─────────────────┤
│ id (PK)         │
│ email (unique)  │
│ name            │
│ lastName        │
│ password (hash) │
│ isAdmin         │
└─────────────────┘

┌─────────────────────────┐          ┌──────────────────────┐
│       Animal            │◄─────────│ AdoptionApplication  │
├─────────────────────────┤          ├──────────────────────┤
│ id (PK)                 │          │ id (PK)              │
│ name                    │          │ animalId (FK) ───────┤
│ type                    │          │ applicantName        │
│ age                     │          │ applicantLastName    │
│ gender                  │          │ email                │
│ size                    │          │ phone                │
│ breed                   │          │ address              │
│ shortDescription        │          │ city                 │
│ longDescription         │          │ state                │
│ goodWithKids            │          │ zipCode              │
│ goodWithDogs            │          │ birthdate            │
│ homeTrained             │          │ occupation           │
│ availableForAdoption    │          │ reasonForAdoption    │
│ media (JSON[])          │          │ experienceWithPets   │
└─────────────────────────┘          │ homeType             │
                                     │ whoLivesInHouse      │
┌─────────────────────────┐          │ agreeToTerms         │
│      Volunteer          │          │ status (enum)        │
├─────────────────────────┤          │ date                 │
│ id (PK)                 │          └──────────────────────┘
│ name                    │
│ lastName                │          ┌──────────────────────┐
│ email (unique)          │          │  ContactMessage      │
│ phone                   │          ├──────────────────────┤
│ availability (array)    │          │ id (PK)              │
│ availableDays (array)   │          │ name                 │
│ areasOfInterest (array) │          │ lastName             │
│ whyVolunteer            │          │ email                │
│ specialSkills           │          │ subject              │
│ emergencyContactName    │          │ message              │
│ emergencyContactPhone   │          │ date                 │
│ status (enum)           │          └──────────────────────┘
│ privacyAgreement        │
│ date                    │          ┌──────────────────────┐
└─────────────────────────┘          │   Subscription       │
                                     ├──────────────────────┤
┌─────────────────────────┐          │ id (PK)              │
│   ShelterSettings       │          │ email                │
├─────────────────────────┤          └──────────────────────┘
│ id (PK)                 │
│ logo_url                │
│ logo_public_id          │
│ shelter_name            │
│ shelter_email           │
│ shelter_phone           │
│ shelter_address         │
│ city                    │
│ state                   │
│ zip_code                │
│ updated_at              │
└─────────────────────────┘
```

### **Model Details**

#### **PawUser** (Authentication & Authorization)

```python
{
  "id": int,                    # Primary key
  "email": EmailStr,            # Unique, indexed
  "name": str,                  # Min 1, max 100 chars
  "lastName": str,              # Min 1, max 100 chars
  "password": str,              # Argon2 hashed, min 8 chars
  "isAdmin": bool               # Default: false
}
```

#### **Animal** (Adoption Listings)

```python
{
  "id": int,                           # Primary key
  "name": str,                         # Indexed, max 100 chars
  "type": str,                         # dog, cat, etc. (indexed)
  "age": int,                          # 0-30 years
  "gender": str,                       # Max 20 chars
  "size": str,                         # small/medium/large
  "breed": str,                        # Max 100 chars
  "shortDescription": str,             # Max 200 chars
  "longDescription": str,              # Max 2000 chars
  "goodWithKids": bool,
  "goodWithDogs": bool,
  "homeTrained": bool,
  "availableForAdoption": enum,        # available | pending | adopted
  "media": [                           # JSON array (PostgreSQL JSON type)
    {
      "url": str,                      # Cloudinary secure_url
      "public_id": str,                # For deletion
      "resource_type": str,            # image | video
      "format": str,                   # jpg, png, mp4, etc.
      "width": int,
      "height": int,
      "bytes": int
    }
  ]
}
```

#### **AdoptionApplication** (Adoption Requests)

```python
{
  "id": int,                           # Primary key, indexed
  "animalId": int,                     # Foreign key → Animal.id (indexed)
  "applicantName": str,                # Max 100 chars
  "applicantLastName": str,            # Max 100 chars
  "email": EmailStr,
  "phone": str,                        # 7-20 chars
  "address": str,                      # 5-200 chars
  "city": str,                         # 2-100 chars
  "state": str,                        # 2-100 chars
  "zipCode": str,                      # 3-20 chars
  "birthdate": str,
  "occupation": str,                   # 2-100 chars
  "reasonForAdoption": str,            # 10-1000 chars
  "experienceWithPets": str,           # 5-1000 chars
  "homeType": str,                     # 2-50 chars
  "whoLivesInHouse": str,              # 1-500 chars
  "agreeToTerms": bool,
  "status": enum,                      # pending | approved | rejected
  "date": str                          # ISO format
}
```

#### **Volunteer** (Volunteer Applications)

```python
{
  "id": int,                           # Primary key
  "name": str,                         # Max 100 chars
  "lastName": str,                     # Max 100 chars
  "email": EmailStr,                   # Unique
  "phone": str,                        # 7-20 chars
  "availability": [str],               # PostgreSQL ARRAY: ["morning", "afternoon", "evening"]
  "availableDays": [str],              # ARRAY: ["monday", "tuesday", ...]
  "areasOfInterest": [str],            # ARRAY: ["animal_care", "events", "fundraising"]
  "whyVolunteer": str,                 # 10-1000 chars
  "specialSkills": str,                # Optional, max 500 chars
  "emergencyContactName": str,         # Max 100 chars
  "emergencyContactPhone": str,        # 7-20 chars
  "status": enum,                      # pending | accepted | rejected
  "privacyAgreement": bool,
  "date": str                          # ISO format
}
```

#### **ContactMessage** (Contact Form)

```python
{
  "id": int,                           # Primary key
  "name": str,                         # Max 100 chars
  "lastName": str,                     # Max 100 chars
  "email": EmailStr,
  "subject": str,                      # Max 200 chars
  "message": str,                      # 10-2000 chars
  "date": str                          # ISO format
}
```

#### **Subscription** (Newsletter Subscribers)

```python
{
  "id": int,                           # Primary key
  "email": str                         # Max 100 chars
}
```

#### **ShelterSettings** (Configurable Shelter Info)

```python
{
  "id": int,                           # Primary key
  "logo_url": str | null,              # Cloudinary URL
  "logo_public_id": str | null,        # For logo management
  "shelter_name": str,                 # Default: "PawScout Shelter"
  "shelter_email": str | null,         # Max 200 chars
  "shelter_phone": str | null,         # Max 50 chars
  "shelter_address": str | null,       # Max 500 chars
  "city": str | null,                  # Max 100 chars
  "state": str | null,                 # Max 100 chars
  "zip_code": str | null,              # Max 20 chars
  "updated_at": datetime               # Auto-updated
}
```

### **Database Features**

- ✅ **Automatic table creation** via SQLModel metadata
- ✅ **Foreign key relationships** (AdoptionApplication → Animal)
- ✅ **Unique constraints** (email fields)
- ✅ **Indexes** for optimized queries (id, email, name, type, animalId)
- ✅ **Complex data types** (JSON, ARRAY) for PostgreSQL
- ✅ **Enumeration types** for status fields
- ✅ **Field-level validation** with Pydantic

---

## 🌐 API Endpoints

### **Authentication & User Management**

#### Public Endpoints

```http
POST   /users/register          # Register new user account
POST   /users/login             # Login and get JWT token
GET    /users/me                # Get current authenticated user info (requires token)
```

### **Animals (Public Read, Admin Write)**

```http
GET    /animals/                # Get all animals (public)
GET    /animals/{animal_id}     # Get specific animal by ID (public)

POST   /animals/                # Create new animal listing (admin only)
PUT    /animals/{animal_id}     # Update animal information (admin only)
DELETE /animals/{animal_id}     # Delete animal (admin only)
```

### **Applications (Public Submit, Admin Manage)**

#### Adoption Applications

```http
POST   /adopt/{animal_id}       # Submit adoption application (public)
GET    /adopt/{app_id}           # Get adoption application by ID (admin only)
GET    /admin/adoptions          # Get all adoption applications (admin only)
DELETE /adopt/{app_id}           # Delete adoption application (admin only)
```

#### Volunteer Applications

```http
POST   /volunteer/              # Submit volunteer application (public)
GET    /volunteer/              # Get all volunteers (admin only)
GET    /volunteer/{vol_id}      # Get volunteer by ID (admin only)
PUT    /volunteer/{vol_id}      # Update volunteer status (admin only)
DELETE /volunteer/{vol_id}      # Delete volunteer (admin only)
```

#### Contact Messages

```http
POST   /contact/                # Send contact message (public)
GET    /contact/                # Get all messages (admin only)
GET    /contact/{msg_id}        # Get message by ID (admin only)
DELETE /contact/{msg_id}        # Delete message (admin only)
```

#### Newsletter Subscriptions

```http
POST   /subs/                   # Subscribe to newsletter (public)
GET    /subs/                   # Get all subscriptions (admin only)
```

### **Media Management (Admin Only)**

```http
POST   /media/upload            # Upload single image/video
POST   /media/upload-multiple   # Upload multiple files
DELETE /media/delete            # Delete media from Cloudinary by public_id
```

### **Admin Dashboard**

```http
GET    /admin/dashboard         # Get dashboard statistics (users, animals, adoptions, volunteers)
GET    /admin/users             # Get all registered users
PATCH  /admin/users/{id}/promote   # Promote user to admin
PATCH  /admin/users/{id}/demote    # Revoke admin privileges
DELETE /admin/users/{id}        # Delete user account

GET    /admin/settings          # Get shelter settings
PUT    /admin/settings          # Update shelter settings
POST   /admin/settings/logo     # Upload shelter logo
```

### **Response Format Standards**

#### Success Response

```json
{
  "success": "Operation completed successfully",
  "data": {
    /* optional data object */
  }
}
```

#### Error Response

```json
{
  "detail": "Error message describing what went wrong"
}
```

#### List Response

```json
{
  "animals": [
    /* array of animals */
  ],
  "applications": [
    /* array of applications */
  ],
  "volunteers": [
    /* array of volunteers */
  ]
}
```

### **HTTP Status Codes**

| Code  | Description           | Usage                                               |
| ----- | --------------------- | --------------------------------------------------- |
| `200` | OK                    | Successful GET, PUT, DELETE operations              |
| `201` | Created               | Successful POST operations                          |
| `400` | Bad Request           | Validation errors, empty fields                     |
| `401` | Unauthorized          | Invalid or missing JWT token                        |
| `403` | Forbidden             | Valid token but insufficient permissions            |
| `404` | Not Found             | Resource doesn't exist                              |
| `409` | Conflict              | Duplicate email, animal already in adoption process |
| `500` | Internal Server Error | Server-side errors                                  |

---

## 🔐 Security Implementation

### **Authentication Flow**

```mermaid
sequenceDiagram
    participant Client
    participant API
    participant Database
    participant JWT

    Client->>API: POST /users/register (email, password, name)
    API->>API: Hash password with Argon2
    API->>Database: Store user with hashed password
    Database-->>API: User created
    API-->>Client: 201 Created

    Client->>API: POST /users/login (email, password)
    API->>Database: Find user by email
    Database-->>API: Return user with hashed password
    API->>API: Verify password with Argon2
    API->>JWT: Create token (sub, user_id, isAdmin, exp)
    JWT-->>API: Signed JWT token
    API-->>Client: 200 OK + JWT token

    Client->>API: GET /animals/ (with Authorization: Bearer <token>)
    API->>JWT: Verify token signature & expiration
    JWT-->>API: Token valid + decoded payload
    API->>Database: Execute query
    Database-->>API: Return data
    API-->>Client: 200 OK + data
```

### **JWT Token Structure**

```json
{
  "sub": "user@example.com", // Subject: user email
  "user_id": 123, // User ID for quick lookups
  "isAdmin": true, // Role-based access control
  "name": "John", // User's first name
  "lastName": "Doe", // User's last name
  "exp": 1234567890 // Expiration timestamp (14 days)
}
```

### **Security Features**

#### ✅ **Password Security**

- **Argon2** hashing algorithm (winner of Password Hashing Competition)
- **Memory-hard** and **CPU-intensive** to resist brute-force attacks
- **Salt** automatically generated and stored with hash
- **Minimum 8 characters** enforced at validation layer

#### ✅ **Authentication**

- **JWT tokens** with HS256 signing algorithm
- **Configurable expiration** (default: 14 days / 20,160 minutes)
- **Bearer token** scheme in HTTP Authorization header
- **Token payload** includes user identity and permissions

#### ✅ **Authorization**

**Three permission levels:**

1. **Public Access** - No authentication required
   - View animals
   - Submit applications (adoption, volunteer, contact)
   - Register/login
   - Subscribe to newsletter

2. **Authenticated Users** - Valid JWT token
   - Access to `/users/me` endpoint
   - View own profile information

3. **Admin Access** - Valid JWT token + `isAdmin: true`
   - All CRUD operations on animals
   - User management (promote, demote, delete)
   - View all applications and messages
   - Dashboard analytics
   - Media upload/delete
   - Settings management

#### ✅ **Middleware & Dependencies**

```python
# Dependency injection for protected routes
AdminUser = Annotated[PawUser, Depends(get_admin_user)]
CurrentUser = Annotated[PawUser, Depends(get_current_user)]
```

#### ✅ **Input Validation**

- **Pydantic models** for request validation
- **Field-level constraints** (min/max length, regex patterns)
- **Email validation** with `email-validator` library
- **Empty field detection** and rejection
- **Type safety** with SQLModel

#### ✅ **CORS Policy**

```python
origins = [
    "http://localhost:3000",       # Next.js dev
    "http://localhost:5173",       # Vite dev
    os.getenv("FRONTEND_URL")      # Production frontend
]
```

#### ✅ **Database Security**

- **SQL injection prevention** via SQLModel ORM (parameterized queries)
- **Unique constraints** on email fields
- **Foreign key constraints** for referential integrity
- **Index optimization** for performance

#### ✅ **Environment Variables**

All sensitive credentials stored in `.env` file (not in version control):

```env
DATABASE_URL=postgresql://...
AUTH_SECRET_KEY=<generated-secret>
CLOUD_NAME=<cloudinary-cloud>
API_KEY=<cloudinary-key>
API_SECRET=<cloudinary-secret>
```

### **Protected Endpoint Usage**

Include JWT token in Authorization header:

```bash
curl -X GET http://localhost:8000/admin/dashboard \
  -H "Authorization: Bearer <your_jwt_token>"
```

### **Error Responses**

| Status | Scenario      | Detail                           |
| ------ | ------------- | -------------------------------- |
| `401`  | Missing token | "Not authenticated"              |
| `401`  | Invalid token | "Could not validate credentials" |
| `401`  | Expired token | "Token has expired"              |
| `403`  | Not admin     | "Admin privileges required"      |
| `403`  | Self-demotion | "Cannot demote yourself"         |
| `403`  | Self-deletion | "Cannot delete your own account" |

---

## 🚢 Deployment

### 🌐 **Live Production Application**

**🔗 [https://paw-scout.vercel.app/](https://paw-scout.vercel.app/)**

**Deployment Details:**

- **Frontend**: Next.js 15 deployed on **Vercel**
- **Backend API**: FastAPI deployed on **Render** (this repository)
- **Database**: PostgreSQL managed by Render
- **CDN**: Cloudinary for image/video hosting
- **Status**: ✅ Live and fully functional

### **Production Architecture**

```
┌─────────────┐      ┌──────────────────┐      ┌──────────────┐
│   Client    │────►│  Gunicorn        │────►│  PostgreSQL  │
│ (Vercel)    │      │  (4 workers)     │      │  (Render)    │
│  Next.js    │      │  + Uvicorn       │      │   Database   │
└─────────────┘      │  ASGI Workers    │      └──────────────┘
                     │  (Render)        │
                     └──────────────────┘
                              │
                              ▼
                     ┌──────────────────┐
                     │   Cloudinary     │
                     │   CDN (Media)    │
                     └──────────────────┘
```

### **Deployment Configuration**

#### **start.sh** - Production Startup Script

```bash
#!/bin/bash
gunicorn app.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:${PORT:-8000}
```

**Configuration Rationale:**

- **Gunicorn**: Production-grade WSGI server with process management
- **4 Workers**: Multi-process for handling concurrent requests
- **UvicornWorker**: ASGI support for FastAPI async capabilities
- **Dynamic Port**: Uses `$PORT` environment variable (required by Render/Railway)
- **0.0.0.0 Bind**: Accepts connections from all network interfaces

#### **runtime.txt** - Python Version

```
python-3.11.9
```

### **Deployment Platforms**

#### **Render** (Currently Deployed ✅)

**Live API**: Backend currently running on Render infrastructure

```yaml
# Detected automatically from start.sh
build: pip install -r requirements.txt
start: bash start.sh
```

Environment variables configured:

- `DATABASE_URL` (auto-provided by Render PostgreSQL)
- `AUTH_SECRET_KEY`
- `FRONTEND_URL=https://paw-scout.vercel.app`
- `CLOUD_NAME`, `API_KEY`, `API_SECRET` (Cloudinary)

#### **Railway**

```yaml
# Detected automatically
buildCommand: pip install -r requirements.txt
startCommand: bash start.sh
```

#### **Docker** (future-ready)

```dockerfile
FROM python:3.11.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["bash", "start.sh"]
```

### **Database Migration**

- **Automatic table creation** on startup via `SQLModel.metadata.create_all()`
- No manual migration scripts needed for initial deployment
- Schema changes detected automatically

### **Environment Configuration**

#### Development

```bash
uvicorn app.main:app --reload --port 8000
```

#### Production

```bash
bash start.sh
```

### **Health Checks**

```bash
# Simple health check endpoint
curl http://your-api.com/animals/
```

### **Performance Optimizations**

- ✅ **Connection pooling** via SQLModel/SQLAlchemy
- ✅ **Async database operations** with SQLModel
- ✅ **CDN delivery** for all media (Cloudinary)
- ✅ **Automatic image optimization** (quality: auto, format: auto)
- ✅ **Database indexes** on frequently queried fields
- ✅ **Multi-worker deployment** for horizontal scaling

---

## 🌍 Environment Variables

Create a `.env` file in the backend root directory:

```env
# ========================================
# Database Configuration
# ========================================
DATABASE_URL=postgresql://user:password@localhost:5432/pawscout
# For Render: Auto-provided as POSTGRES_URL, rename to DATABASE_URL
# For Railway: Auto-provided

# ========================================
# JWT Authentication
# ========================================
AUTH_SECRET_KEY=your-super-secret-key-here-use-openssl-rand-hex-32
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=20160

# ========================================
# Cloudinary Configuration
# ========================================
CLOUD_NAME=your-cloudinary-cloud-name
API_KEY=your-cloudinary-api-key
API_SECRET=your-cloudinary-api-secret

# ========================================
# Frontend Configuration (Production)
# ========================================
FRONTEND_URL=https://your-production-frontend.vercel.app
# Used for CORS policy
```

### **Generating Secure Keys**

#### **AUTH_SECRET_KEY** (Required)

```bash
# Generate a secure random key (256-bit)
openssl rand -hex 32
```

Example output: `a1b2c3d4e5f6...` (use this value)

### **Environment Variable Details**

| Variable                      | Type   | Required | Default | Description                      |
| ----------------------------- | ------ | -------- | ------- | -------------------------------- |
| `DATABASE_URL`                | string | ✅       | -       | PostgreSQL connection string     |
| `AUTH_SECRET_KEY`             | string | ✅       | -       | JWT signing key (use openssl)    |
| `ALGORITHM`                   | string | ✅       | HS256   | JWT signing algorithm            |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | int    | ✅       | 20160   | Token expiration (14 days)       |
| `CLOUD_NAME`                  | string | ✅       | -       | Cloudinary cloud name            |
| `API_KEY`                     | string | ✅       | -       | Cloudinary API key               |
| `API_SECRET`                  | string | ✅       | -       | Cloudinary API secret            |
| `FRONTEND_URL`                | string | ❌       | -       | Production frontend URL for CORS |

### **Getting Cloudinary Credentials**

1. Sign up at [cloudinary.com](https://cloudinary.com) (free tier available)
2. Navigate to Dashboard
3. Copy **Cloud Name**, **API Key**, and **API Secret**

### **Database URL Formats**

#### Local PostgreSQL

```
postgresql://username:password@localhost:5432/database_name
```

#### Render

```
postgres://user:password@hostname:5432/database
# Automatically provided as POSTGRES_URL
# Set DATABASE_URL = ${POSTGRES_URL} in dashboard
```

#### Railway

```
postgres://user:password@hostname:port/database
# Automatically provided as DATABASE_URL
```

---

## 🚀 Installation & Setup

### **Prerequisites**

| Requirement            | Version   | Purpose            |
| ---------------------- | --------- | ------------------ |
| **Python**             | 3.11.9+   | Backend runtime    |
| **PostgreSQL**         | 14+       | Primary database   |
| **pip**                | Latest    | Package management |
| **Cloudinary Account** | Free tier | Media storage/CDN  |

### **Local Development Setup**

#### **1. Clone the Repository**

```bash
git clone https://github.com/yourusername/pawscout.git
cd pawscout/backend
```

#### **2. Create Virtual Environment**

```bash
# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate

# Windows
python -m venv .venv
.venv\Scripts\activate
```

#### **3. Install Dependencies**

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**requirements.txt includes:**

- fastapi==0.115.5
- uvicorn[standard]==0.32.1
- sqlmodel==0.0.22
- pydantic==2.10.5
- pydantic-settings==2.7.0
- python-dotenv==1.0.1
- python-multipart==0.0.18
- pyjwt==2.10.1
- pwdlib[argon2]==0.2.1
- cloudinary==1.41.0
- psycopg2-binary==2.9.10
- email-validator==2.2.0
- gunicorn==23.0.0

#### **4. Set Up PostgreSQL Database**

```bash
# Create database
createdb pawscout

# Verify connection
psql pawscout -c "\dt"
```

**Or using PostgreSQL client:**

```sql
CREATE DATABASE pawscout;
```

#### **5. Configure Environment Variables**

Create `.env` file in backend root:

```bash
# Copy example and edit
cp .env.example .env  # If example exists
# OR create manually
nano .env
```

Add the following (see [Environment Variables](#-environment-variables) section):

```env
DATABASE_URL=postgresql://user:password@localhost:5432/pawscout
AUTH_SECRET_KEY=<generate-with-openssl-rand-hex-32>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=20160
CLOUD_NAME=your-cloudinary-cloud-name
API_KEY=your-cloudinary-api-key
API_SECRET=your-cloudinary-api-secret
```

#### **6. Generate AUTH_SECRET_KEY**

```bash
openssl rand -hex 32
# Copy output to .env file
```

#### **7. Run the Application**

**Development mode with auto-reload:**

```bash
# Using FastAPI CLI (recommended)
fastapi dev app/main.py

# OR using Uvicorn directly
uvicorn app.main:app --reload --port 8000
```

**Production mode (locally):**

```bash
bash start.sh
```

#### **8. Verify Installation**

```bash
# Check if server is running
curl http://localhost:8000/animals/

# Expected response: {"animals": []}
```

#### **9. Access API Documentation**

- **Swagger UI (Interactive)**: http://localhost:8000/docs
- **ReDoc (Clean)**: http://localhost:8000/redoc
- **OpenAPI Schema (JSON)**: http://localhost:8000/openapi.json

### **Database Initialization**

Tables are **automatically created** on first startup via SQLModel:

```python
# In app/database.py
def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)
```

**Tables created:**

- `pawuser`
- `animal`
- `adoptionapplication`
- `volunteer`
- `contactmessage`
- `subscription`
- `shelter_settings`

### **Creating Your First Admin User**

1. Register a user via API:

```bash
curl -X POST http://localhost:8000/users/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@pawscout.com",
    "name": "Admin",
    "lastName": "User",
    "password": "securepassword123"
  }'
```

2. Manually promote to admin in PostgreSQL:

```sql
UPDATE pawuser SET "isAdmin" = true WHERE email = 'admin@pawscout.com';
```

3. Login to get JWT token:

```bash
curl -X POST http://localhost:8000/users/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@pawscout.com",
    "password": "securepassword123"
  }'
```

---

## 🧪 API Testing Examples

### **1. User Registration**

```bash
curl -X POST http://localhost:8000/users/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "name": "John",
    "lastName": "Doe",
    "password": "securepassword123"
  }'
```

**Response:**

```json
{
  "success": "User registered successfully"
}
```

### **2. User Login (Get JWT Token)**

```bash
curl -X POST http://localhost:8000/users/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword123"
  }'
```

**Response:**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "name": "John",
    "lastName": "Doe",
    "isAdmin": false
  }
}
```

### **3. Get All Animals (Public)**

```bash
curl http://localhost:8000/animals/
```

**Response:**

```json
{
  "animals": [
    {
      "id": 1,
      "name": "Max",
      "type": "dog",
      "age": 3,
      "gender": "Male",
      "size": "Medium",
      "breed": "Golden Retriever",
      "shortDescription": "Friendly and energetic",
      "longDescription": "Max is a wonderful companion...",
      "goodWithKids": true,
      "goodWithDogs": true,
      "homeTrained": true,
      "availableForAdoption": "available",
      "media": [
        {
          "url": "https://res.cloudinary.com/...",
          "public_id": "pawscout/animals/abc123",
          "resource_type": "image"
        }
      ]
    }
  ]
}
```

### **4. Upload Media (Admin Only)**

```bash
curl -X POST http://localhost:8000/media/upload \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -F "file=@/path/to/image.jpg" \
  -F "folder=pawscout/animals"
```

**Response:**

```json
{
  "url": "https://res.cloudinary.com/demo/image/upload/v1234567890/pawscout/animals/abc123.jpg",
  "public_id": "pawscout/animals/abc123",
  "resource_type": "image",
  "format": "jpg",
  "width": 1920,
  "height": 1080,
  "bytes": 245678
}
```

### **5. Create Animal (Admin Only)**

```bash
curl -X POST http://localhost:8000/animals/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Max",
    "type": "dog",
    "age": 3,
    "gender": "Male",
    "size": "Medium",
    "breed": "Golden Retriever",
    "shortDescription": "Friendly and energetic",
    "longDescription": "Max is a wonderful companion who loves to play fetch and go for long walks. He is well-trained and great with families.",
    "goodWithKids": true,
    "goodWithDogs": true,
    "homeTrained": true,
    "media": [
      {
        "url": "https://res.cloudinary.com/demo/image/upload/v1234567890/pawscout/animals/max.jpg",
        "public_id": "pawscout/animals/max",
        "resource_type": "image"
      }
    ]
  }'
```

**Response:**

```json
{
  "success": "Animal created successfully"
}
```

### **6. Submit Adoption Application (Public)**

```bash
curl -X POST http://localhost:8000/adopt/1 \
  -H "Content-Type: application/json" \
  -d '{
    "animalId": 1,
    "applicantName": "Jane",
    "applicantLastName": "Smith",
    "email": "jane@example.com",
    "phone": "555-0123",
    "address": "123 Main St",
    "city": "San Francisco",
    "state": "CA",
    "zipCode": "94102",
    "birthdate": "1990-01-15",
    "occupation": "Software Engineer",
    "reasonForAdoption": "I want to give Max a loving home...",
    "experienceWithPets": "I have owned dogs for 10 years...",
    "homeType": "House with yard",
    "whoLivesInHouse": "Just me and my partner",
    "agreeToTerms": true,
    "date": "2024-02-17"
  }'
```

**Response:**

```json
{
  "success": "Adoption application submitted successfully"
}
```

### **7. Get Dashboard Stats (Admin Only)**

```bash
curl http://localhost:8000/admin/dashboard \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**Response:**

```json
{
  "message": "Welcome to admin dashboard, Admin!",
  "stats": {
    "total_users": 15,
    "total_animals": 23,
    "total_adoptions": 8,
    "total_volunteers": 12
  }
}
```

### **Testing with Swagger UI**

1. Navigate to http://localhost:8000/docs
2. Click **"Authorize"** button (🔒 icon)
3. Enter: `Bearer YOUR_JWT_TOKEN`
4. Click **"Authorize"**
5. Test endpoints interactively with auto-generated forms

---

## 🔒 Security Features

- ✅ Argon2 password hashing
- ✅ JWT token-based authentication
- ✅ Role-based access control (RBAC)
- ✅ CORS configuration for trusted origins
- ✅ Input validation with Pydantic models
- ✅ SQL injection prevention via SQLModel ORM
- ✅ Secure password requirements (min 8 characters)
- ✅ Email uniqueness validation
- ✅ Self-modification protection (can't demote/delete yourself)

---

## 📝 API Response Format

### Success Response

```json
{
  "success": "Operation completed successfully",
  "data": {...}
}
```

### Error Response

```json
{
  "detail": "Error message describing what went wrong"
}
```

### List Response

```json
{
  "animals": [...],
  "applications": [...],
  "volunteers": [...]
}
```

---

## 🎨 Media Upload Workflow

### **Complete Flow**

```mermaid
sequenceDiagram
    participant Admin
    participant API
    participant Cloudinary
    participant Database

    Admin->>API: POST /media/upload-multiple (files)
    API->>Cloudinary: Upload images/videos
    Cloudinary-->>API: Return URLs + public_ids
    API-->>Admin: Media metadata array

    Admin->>API: POST /animals/ (with media array)
    API->>Database: Store animal + media references
    Database-->>API: Animal created
    API-->>Admin: Success response

    Note over Cloudinary: Images optimized, CDN cached

    Admin->>API: DELETE /media/delete (public_id)
    API->>Cloudinary: Remove media
    Cloudinary-->>API: Deletion confirmed
    API-->>Admin: Success
```

### **Step-by-Step**

1. **Upload Media**

   ```bash
   POST /media/upload-multiple
   # Returns: [{ url, public_id, resource_type, ... }]
   ```

2. **Create/Update Animal**

   ```bash
   POST /animals/
   # Include media array from step 1 in request body
   ```

3. **Public Access**
   - URLs automatically optimized via Cloudinary
   - Format: `https://res.cloudinary.com/<cloud>/image/upload/q_auto,f_auto/...`
   - **q_auto**: Automatic quality
   - **f_auto**: Automatic format conversion (WebP for Chrome, etc.)

4. **Media Deletion**
   ```bash
   DELETE /media/delete
   # Body: { "public_id": "pawscout/animals/abc123" }
   ```

---

## 💡 Technical Highlights

### **Backend Engineering Skills Demonstrated**

#### ✅ **API Design & Development**

- **RESTful architecture** with proper HTTP verbs and status codes
- **CRUD operations** across 7 database models
- **Comprehensive validation** with Pydantic (50+ validated fields)
- **OpenAPI documentation** auto-generated from code annotations
- **Error handling** with custom exception classes

#### ✅ **Database Engineering**

- **SQLModel ORM** for type-safe database operations
- **Foreign key relationships** and referential integrity
- **Complex data types**: JSON arrays, PostgreSQL ARRAY types
- **Optimized queries** with indexes on frequently accessed fields
- **Automatic migrations** via metadata.create_all()

#### ✅ **Authentication & Security**

- **JWT token-based authentication** with 14-day expiration
- **Argon2 password hashing** (OWASP recommended)
- **Role-based access control** (RBAC) with dependency injection
- **CORS configuration** for secure cross-origin requests
- **SQL injection prevention** via ORM parameterization
- **Input sanitization** and field-level validation

#### ✅ **Cloud Integration**

- **Cloudinary SDK** for media management
- **Async file uploads** with multipart form data
- **Automatic optimization** (quality, format, dimensions)
- **CDN delivery** for global performance
- **Resource lifecycle management** (upload, serve, delete)

#### ✅ **Production Deployment**

- **Gunicorn + Uvicorn** multi-worker configuration
- **Environment-based configuration** with dotenv
- **Database connection pooling** for efficiency
- **Production-ready startup scripts**
- **Platform-agnostic deployment** (Render, Railway, Docker)

#### ✅ **Code Quality**

- **Type hints** throughout (Python 3.11+ syntax)
- **Modular architecture** with router-based organization
- **Dependency injection** for testability and reusability
- **Separation of concerns** (models, routes, business logic)
- **Consistent naming conventions** and code structure

### **Performance Optimizations**

- ⚡ **Async/await patterns** for non-blocking I/O
- ⚡ **Database indexing** on email, id, animalId, name, type
- ⚡ **CDN caching** for all media assets
- ⚡ **Connection pooling** via SQLAlchemy engine
- ⚡ **Multi-worker deployment** for horizontal scaling

### **Full-Stack Integration**

This backend integrates with a **Next.js 15** frontend featuring:

- Server and Client Components
- Server Actions for form submissions
- TanStack Query (React Query) for data fetching
- TypeScript throughout
- Tailwind CSS for styling

**Live Application**: **[https://paw-scout.vercel.app/](https://paw-scout.vercel.app/)**

**API consumed by:**

- Public-facing adoption website
- Admin dashboard for management
- Mobile-friendly responsive interfaces

---

## 🎯 Use Cases & Business Logic

### **Animal Adoption System**

- Browse available animals with filters
- View detailed profiles with media galleries
- Submit adoption applications with 14+ validated fields
- Automatic status updates (available → pending → adopted)
- Foreign key relationships ensure data integrity

### **Volunteer Management**

- Multi-select availability (time slots + days of week)
- Areas of interest tracking (animal care, events, fundraising)
- Application status workflow (pending, accepted, rejected)
- Emergency contact information storage

### **Admin Operations**

- User role management (promote/demote)
- Dashboard analytics and statistics
- Review all applications and messages
- Media library management
- Shelter settings configuration

### **Security & Data Protection**

- Self-protection (admins can't delete themselves)
- Email uniqueness validation
- Comprehensive input validation
- Secure credential storage
- Token expiration and refresh patterns

---

## 📈 Future Enhancements

### **Planned Features**

- [ ] **Email notifications** - SendGrid/AWS SES integration for application updates
- [ ] **Payment processing** - Stripe integration for donations
- [ ] **Advanced search** - Full-text search with PostgreSQL or Elasticsearch
- [ ] **Pagination** - Cursor-based pagination for large datasets
- [ ] **Rate limiting** - slowapi integration to prevent abuse
- [ ] **Websockets** - Real-time updates for admin dashboard
- [ ] **File validation** - Virus scanning for uploaded images
- [ ] **Metrics & monitoring** - Prometheus/Grafana integration
- [ ] **Automated testing** - pytest suite with 80%+ coverage
- [ ] **CI/CD pipeline** - GitHub Actions for automated deployment

### **Scalability Considerations**

- Redis caching for frequently accessed data
- Message queue (Celery) for async tasks
- Microservices architecture for domain separation
- Database read replicas for query optimization
- GraphQL layer for flexible client queries

---

## 🤝 Contributing & Development

### **Code Standards**

- **PEP 8** compliance for Python code style
- **Type hints** for all function signatures
- **Docstrings** for all public functions
- **Async/await** for I/O operations
- **Dependency injection** for testability

### **Development Workflow**

```bash
# Create feature branch
git checkout -b feature/new-endpoint

# Make changes with hot reload
fastapi dev app/main.py

# Test endpoints via Swagger UI
open http://localhost:8000/docs

# Commit and push
git add .
git commit -m "feat: add new endpoint"
git push origin feature/new-endpoint
```

---

## 📄 License

This project is part of a **full-stack development portfolio** demonstrating production-ready backend engineering skills.

### **Project Purpose**

Built to showcase:

- Modern Python API development with FastAPI
- Database design and ORM implementation
- Authentication and authorization patterns
- Cloud service integration
- Production deployment practices
- Clean code and architecture principles

---

## 👨‍💻 Author

**Full-Stack Developer | Backend Engineer**

### 🌐 **Live Project**

**[https://paw-scout.vercel.app/](https://paw-scout.vercel.app/)**

**Technologies Featured:**

- 🐍 Python 3.11 with type safety
- ⚡ FastAPI for high-performance async APIs
- 🗄️ PostgreSQL with SQLModel ORM
- 🔐 JWT authentication with Argon2 hashing
- ☁️ Cloudinary CDN integration
- 🚀 Production deployment (Gunicorn + Uvicorn)
- 📚 Comprehensive API documentation

**Full Stack:**

- **Backend**: Python, FastAPI, PostgreSQL (Render)
- **Frontend**: Next.js 15, TypeScript, React, Tailwind CSS (Vercel)
- **DevOps**: Render, Vercel, Git
- **Tools**: Postman, pgAdmin, VS Code

---

## 📞 API Documentation

### **Local Development**

- **Interactive Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc
- **OpenAPI Schema**: http://localhost:8000/openapi.json

### **Quick Health Check**

```bash
# Simple test to verify API is running
curl http://localhost:8000/animals/
```

### **Support & Questions**

For questions about the architecture, implementation details, or technical decisions:

- Review the comprehensive code comments
- Explore the Swagger documentation
- Examine the database schema and relationships

---

## 🎓 Learning Outcomes

This project demonstrates:

- ✅ Building **production-grade REST APIs** with FastAPI
- ✅ Implementing **secure authentication** with JWT and Argon2
- ✅ Designing **normalized database schemas** with foreign keys
- ✅ Integrating **third-party cloud services** (Cloudinary)
- ✅ Writing **comprehensive API documentation**
- ✅ Deploying to **production environments** with proper configuration
- ✅ Following **best practices** for code organization and security
- ✅ Creating **full-stack applications** with modern frameworks

**Total Lines of Code**: ~2,000+ across backend and frontend
**API Endpoints**: 35+ routes
**Database Tables**: 7 models with relationships
**Authentication**: JWT with role-based access control
**Cloud Integration**: Cloudinary CDN for media management

---

**Built with ❤️ and attention to detail | Production-ready backend engineering**
