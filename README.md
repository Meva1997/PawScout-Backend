# 🐾 PawScout Backend API

A comprehensive FastAPI backend for an animal adoption platform with user authentication, admin management, and media handling.

## 📋 Table of Contents

- [Overview](#overview)
- [Tech Stack](#tech-stack)
- [Features](#features)
- [Project Structure](#project-structure)
- [Database Models](#database-models)
- [API Endpoints](#api-endpoints)
- [Authentication & Authorization](#authentication--authorization)
- [Environment Variables](#environment-variables)
- [Installation & Setup](#installation--setup)

---

## 🎯 Overview

PawScout is a full-featured REST API built with FastAPI that manages an animal adoption platform. The system includes user registration/authentication, animal listings with media support via Cloudinary, adoption applications, volunteer management, contact forms, and comprehensive admin controls.

## 🛠 Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL with SQLModel ORM
- **Authentication**: JWT (JSON Web Tokens)
- **Password Hashing**: Argon2 via pwdlib
- **Media Storage**: Cloudinary (images and videos)
- **Security**: OAuth2 with Bearer tokens
- **CORS**: Configured for Next.js frontend

## ✨ Features

### 🔐 Authentication & Authorization

- JWT-based authentication with 20,160 minute token expiration (14 days)
- Role-based access control (Admin/User)
- Secure password hashing with Argon2
- OAuth2 password bearer flow

### 🐶 Animal Management

- CRUD operations for animal listings
- Support for multiple media files (images/videos)
- Status tracking (available, pending, adopted)
- Detailed animal profiles with breed, age, temperament

### 📝 Application Processing

- Adoption applications linked to animals
- Volunteer registration and management
- Contact form message handling
- Status tracking for all applications

### 👨‍💼 Admin Dashboard

- User management (promote/demote admin rights)
- View all applications and volunteers
- Dashboard statistics
- Media management through Cloudinary

### 📸 Media Handling

- Upload single or multiple images/videos
- Automatic optimization and format conversion
- Cloudinary CDN delivery
- Public ID tracking for deletion

---

## 📁 Project Structure

```
backend/app/
├── main.py                      # FastAPI application & router registration
├── database.py                  # Database connection & session management
├── auth.py                      # JWT token & password utilities
├── dependencies.py              # Reusable FastAPI dependencies (Auth)
├── cloudinary_config.py         # Cloudinary upload/delete functions
├── routers/
│   ├── animals.py              # Animal CRUD endpoints
│   ├── adopt.py                # Adoption application endpoints
│   ├── volunteer.py            # Volunteer management endpoints
│   ├── contact.py              # Contact form endpoints
│   └── users.py                # User registration & authentication
├── internal/
│   └── admin.py                # Admin-only endpoints
└── cloudinary/
    └── routers/
        └── media.py            # Media upload/delete endpoints
```

---

## 🗃 Database Models

### PawUser

User accounts with authentication and role management

```python
{
  "id": int,
  "email": str (unique),
  "name": str,
  "lastName": str,
  "password": str (hashed),
  "isAdmin": bool
}
```

### Animal

Animal listings for adoption

```python
{
  "id": int,
  "name": str,
  "type": str,
  "age": int,
  "gender": str,
  "size": str,
  "breed": str,
  "shortDescription": str,
  "longDescription": str,
  "goodWithKids": bool,
  "goodWithDogs": bool,
  "homeTrained": bool,
  "availableForAdoption": "available" | "pending" | "adopted",
  "media": [{"url": str, "public_id": str, "resource_type": str}]
}
```

### AdoptionApplication

Applications to adopt animals

```python
{
  "id": int,
  "animalId": int (foreign key),
  "applicantName": str,
  "applicantLastName": str,
  "email": str,
  "phone": str,
  "address": str,
  "city": str,
  "state": str,
  "zipCode": str,
  "birthdate": str,
  "occupation": str,
  "reasonForAdoption": str,
  "experienceWithPets": str,
  "homeType": str,
  "whoLivesInHouse": str,
  "agreeToTerms": bool,
  "date": str
}
```

### Volunteer

Volunteer applications

```python
{
  "id": int,
  "name": str,
  "lastName": str,
  "email": str (unique),
  "phone": str,
  "availability": [str],  # Array: ["morning", "afternoon", "evening"]
  "availableDays": [str], # Array: ["monday", "tuesday", ...]
  "areasOfInterest": [str], # Array: ["animal_care", "events", ...]
  "whyVolunteer": str,
  "specialSkills": str,
  "emergencyContactName": str,
  "emergencyContactPhone": str,
  "status": "pending" | "accepted" | "rejected",
  "privacyAgreement": bool,
  "date": str
}
```

### ContactMessage

Messages from contact form

```python
{
  "id": int,
  "name": str,
  "lastName": str,
  "email": str,
  "subject": str,
  "message": str,
  "date": str
}
```

---

## 🌐 API Endpoints

### 🔓 Public Endpoints

#### Authentication

```
POST   /users/register          # Register new user
POST   /auth/token              # Login (get JWT token)
GET    /users/me                # Get current user info (requires auth)
```

#### Animals

```
GET    /animals/                # Get all animals
GET    /animals/{animal_id}    # Get animal by ID
```

#### Applications (Public Submit)

```
POST   /adopt/{animal_id}      # Submit adoption application
POST   /volunteer/             # Submit volunteer application
POST   /contact/               # Send contact message
```

### 🔒 Admin-Only Endpoints

#### Animal Management

```
POST   /animals/               # Create new animal (Admin)
PUT    /animals/{animal_id}   # Update animal (Admin)
DELETE /animals/{animal_id}   # Delete animal (Admin)
```

#### Application Management

```
GET    /adopt/                 # Get all adoption applications (Admin)
GET    /adopt/{app_id}         # Get adoption by ID (Admin)
DELETE /adopt/{app_id}         # Delete adoption application (Admin)

GET    /volunteer/             # Get all volunteers (Admin)
GET    /volunteer/{vol_id}     # Get volunteer by ID (Admin)
PUT    /volunteer/{vol_id}     # Update volunteer (Admin)
DELETE /volunteer/{vol_id}     # Delete volunteer (Admin)

GET    /contact/               # Get all messages (Admin)
GET    /contact/{msg_id}       # Get message by ID (Admin)
DELETE /contact/{msg_id}       # Delete message (Admin)
```

#### Media Management

```
POST   /media/upload           # Upload single image/video (Admin)
POST   /media/upload-multiple  # Upload multiple files (Admin)
DELETE /media/delete            # Delete media from Cloudinary (Admin)
```

#### Admin Dashboard

```
GET    /admin/dashboard        # Dashboard statistics (Admin)
GET    /admin/users            # Get all users (Admin)
GET    /admin/adoptions        # Get all adoptions (Admin)
GET    /admin/volunteers       # Get all volunteers (Admin)
PATCH  /admin/users/{id}/promote   # Promote user to admin (Admin)
PATCH  /admin/users/{id}/demote    # Remove admin privileges (Admin)
DELETE /admin/users/{id}       # Delete user (Admin)
```

---

## 🔐 Authentication & Authorization

### JWT Token Structure

```json
{
  "sub": "user@example.com",
  "user_id": 123,
  "exp": 1234567890
}
```

### Authorization Levels

1. **Public Access** - No authentication required
   - View animals
   - Submit applications (adopt, volunteer, contact)
   - Register/login

2. **Authenticated Users** - Valid JWT token
   - Access to `/users/me` endpoint

3. **Admin Access** - Valid JWT token + `isAdmin: true`
   - All CRUD operations
   - User management
   - Dashboard access
   - Media management

### Protected Endpoint Usage

Include JWT token in Authorization header:

```bash
Authorization: Bearer <your_jwt_token>
```

### Error Responses

- **401 Unauthorized** - Invalid or missing token
- **403 Forbidden** - Valid token but insufficient privileges (not admin)

---

## 🌍 Environment Variables

Create a `.env` file in the backend root:

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/pawscout

# JWT Authentication
AUTH_SECRET_KEY=your-super-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=20160

# Cloudinary
CLOUD_NAME=your-cloudinary-cloud-name
API_KEY=your-cloudinary-api-key
API_SECRET=your-cloudinary-api-secret
```

### Generating AUTH_SECRET_KEY

```bash
openssl rand -hex 32
```

---

## 🚀 Installation & Setup

### Prerequisites

- Python 3.11+
- PostgreSQL 14+
- Cloudinary account (free tier available)

### Installation Steps

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/pawscout.git
cd pawscout/backend
```

2. **Create virtual environment**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install fastapi sqlmodel psycopg2-binary python-multipart python-dotenv pyjwt pwdlib cloudinary uvicorn
```

4. **Set up environment variables**

```bash
cp .env.example .env
# Edit .env with your credentials
```

5. **Create PostgreSQL database**

```bash
createdb pawscout
```

6. **Run the application**

```bash
# Development mode with auto-reload
fastapi dev

# Production mode
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

7. **Access API documentation**

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## 📊 Database Schema

The application automatically creates all tables on startup via SQLModel. No manual migrations required for initial setup.

### Relationships

- `AdoptionApplication.animalId` → `Animal.id` (Foreign Key)
- Animal status changes to "pending" when adoption application is submitted

---

## 🧪 API Testing

### Register a User

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

### Login (Get Token)

```bash
curl -X POST http://localhost:8000/auth/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=user@example.com&password=securepassword123"
```

### Get Animals (Public)

```bash
curl http://localhost:8000/animals/
```

### Create Animal (Admin Only)

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
    "longDescription": "Max is a wonderful companion...",
    "goodWithKids": true,
    "goodWithDogs": true,
    "homeTrained": true,
    "media": [
      {
        "url": "https://res.cloudinary.com/...",
        "public_id": "pawscout/animals/abc123",
        "resource_type": "image"
      }
    ]
  }'
```

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

1. **Admin uploads media files** via `/media/upload-multiple`

   ```json
   Response: [
     {
       "url": "https://res.cloudinary.com/...",
       "public_id": "pawscout/animals/abc123",
       "resource_type": "image"
     }
   ]
   ```

2. **Admin creates/updates animal** with media array

   ```json
   {
     "name": "Buddy",
     "media": [
       /* array from step 1 */
     ]
   }
   ```

3. **Public users view animals** with optimized Cloudinary URLs

---

## 🌟 Key Features Showcase

### Adoption Flow

1. User browses animals (public)
2. User submits adoption application
3. Animal status automatically changes to "pending"
4. Admin reviews application in dashboard
5. Admin can approve/reject and manage status

### Volunteer Management

- Multi-select availability (morning, afternoon, evening)
- Days of week selection (PostgreSQL array)
- Areas of interest tracking
- Status workflow (pending → accepted/rejected)

### Contact System

- Subject categorization
- Message storage for admin review
- Email capture for follow-up

---

## 📈 Future Enhancements

- [ ] Email notifications (SendGrid/AWS SES)
- [ ] Payment processing for donations
- [ ] Animal search and filtering
- [ ] Adoption application status updates
- [ ] Volunteer scheduling system
- [ ] Real-time chat support
- [ ] Analytics dashboard

---

## 🤝 Contributing

This project demonstrates modern FastAPI development practices including:

- Clean architecture with separation of concerns
- Comprehensive API documentation
- Security best practices
- Database relationship management
- Third-party service integration (Cloudinary)
- Role-based authorization
- RESTful API design

---

## 📄 License

This project is part of a portfolio demonstration.

---

## 👨‍💻 Author

Built with ❤️ as part of a full-stack development portfolio

**Tech Highlights:**

- FastAPI for high-performance async API
- SQLModel for type-safe database operations
- JWT authentication with role-based access
- Cloudinary CDN integration
- PostgreSQL with complex data types (JSON, Arrays)
- RESTful API design principles

---

## 📞 API Support

- **Documentation**: http://localhost:8000/docs
- **OpenAPI Schema**: http://localhost:8000/openapi.json
- **Health Check**: http://localhost:8000/animals/ (public endpoint)
