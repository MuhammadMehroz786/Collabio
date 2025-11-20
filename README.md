# Collabio - AI-Powered Career Platform

<div align="center">

**Complete Full-Stack Application for Students, Employers & Mentors**

[![Flask](https://img.shields.io/badge/Flask-3.0-green)](https://flask.palletsprojects.com/)
[![React](https://img.shields.io/badge/React-18.3-blue)](https://react.dev/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14+-blue)](https://www.postgresql.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.8-blue)](https://www.typescriptlang.org/)
[![WebSockets](https://img.shields.io/badge/WebSockets-Enabled-green)](https://socket.io/)

</div>

---

## 🚀 Overview

Collabio is a comprehensive career platform designed to connect students with job opportunities, mentors, and learning resources. Built with modern technologies and AI-powered matching algorithms.

### ✨ Key Features

- 🎯 **AI-Powered Job Matching** - Smart recommendations based on skills and experience
- 🤝 **Mentorship Platform** - Connect with industry professionals
- 💬 **Real-Time Messaging** - WebSocket-powered instant messaging
- 📚 **Learning Hub** - Course management and progress tracking
- 🌐 **Social Feed** - Share updates, achievements, and opportunities
- 🤖 **AI Career Tools** - Resume builder, interview prep, skill gap analysis
- 📊 **Complete Profiles** - Education, experience, skills management
- 🔐 **Secure Authentication** - JWT-based auth with refresh tokens

---

## 🏗️ Architecture

### Tech Stack

**Backend (Flask)**
- Flask 3.0 - Web framework
- PostgreSQL - Primary database
- SQLAlchemy - ORM
- Flask-SocketIO - Real-time communication
- Flask-JWT-Extended - Authentication
- Redis - Caching & message queue
- Bcrypt - Password hashing

**Frontend (React)**
- React 18.3 - UI framework
- TypeScript - Type safety
- Vite - Build tool
- TailwindCSS - Styling
- shadcn/ui - Component library
- React Router - Navigation
- TanStack Query - Data fetching

---

## 📋 Prerequisites

- Python 3.10+
- Node.js 18+
- PostgreSQL 14+
- Redis 6+ (optional)
- Git

---

## 🚀 Quick Start

### 1. Clone Repository

```bash
git clone <your-repo-url>
cd Collabio
```

### 2. Setup Backend

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env
# Edit .env with your database credentials

# Create database
createdb collabio_db

# Run migrations
psql -d collabio_db -f migrations/001_initial_schema.sql

# Start server
python run.py
```

Backend runs on: **http://localhost:5000**

### 3. Setup Frontend

```bash
cd frontend

# Install dependencies
npm install

# Setup environment
cp .env.example .env

# Start development server
npm run dev
```

Frontend runs on: **http://localhost:5173**

---

## 📚 Documentation

- **[Complete Setup Guide](SETUP_GUIDE.md)** - Detailed installation instructions
- **[Backend Documentation](backend/README.md)** - API endpoints & database schema
- **[Frontend Documentation](frontend/README.md)** - Component structure & services

---

## 🗄️ Database Schema

The application uses a comprehensive PostgreSQL schema with:

- **15 Main Tables**: Users, Profiles, Jobs, Mentorship, Messaging, Courses, Social
- **Soft Deletes**: All tables support data recovery
- **Auto Triggers**: For updating counters and ratings
- **Optimized Indexes**: For fast queries
- **UUID Primary Keys**: For better distribution

**Key Tables:**
- `users` - Authentication and user types
- `student_profiles` - Student information
- `jobs` - Job listings
- `mentorship_requests` - Mentorship connections
- `messages` - Real-time messaging
- `courses` - Learning materials
- `posts` - Social feed

---

## 🔌 API Architecture

### Base URL
```
http://localhost:5000/api/v1
```

### Authentication Flow

1. **Register**: `POST /auth/register`
2. **Login**: `POST /auth/login` → Receives access & refresh tokens
3. **Protected Routes**: Include `Authorization: Bearer <token>` header
4. **Refresh Token**: `POST /auth/refresh` when access token expires

### Main Endpoints

| Category | Method | Endpoint | Description |
|----------|--------|----------|-------------|
| Auth | POST | `/auth/register` | Register user |
| Auth | POST | `/auth/login` | Login user |
| Jobs | GET | `/jobs` | List jobs |
| Jobs | POST | `/jobs/:id/apply` | Apply to job |
| Students | GET | `/students/me` | Get profile |
| Students | PUT | `/students/me` | Update profile |
| Mentors | GET | `/mentors` | List mentors |
| Mentors | POST | `/mentors/:id/request` | Request mentorship |
| Messages | GET | `/messages/conversations` | Get conversations |
| Courses | GET | `/courses` | List courses |
| AI Tools | POST | `/ai-tools/resume-builder` | Analyze resume |

**Full API Documentation**: See [backend/README.md](backend/README.md)

---

## 🎨 Frontend Services

The frontend uses a service layer pattern for API communication:

```typescript
import { authService, jobsService, studentsService } from '@/services';

// Login
await authService.login({ email, password });

// Get jobs
const jobs = await jobsService.getAll({ job_type: 'internship' });

// Update profile
await studentsService.updateMyProfile({ bio: 'Updated bio' });
```

**Available Services:**
- `authService` - Authentication
- `jobsService` - Job operations
- `studentsService` - Student profile management
- `mentorsService` - Mentorship operations
- `messagingService` - Real-time messaging
- `coursesService` - Course management
- `socialService` - Social feed
- `aiToolsService` - AI-powered tools

---

## 🤖 AI Matching Algorithm

### Job Matching (0-100 score)

- **Skills Match (40%)** - Compare student skills with job requirements
- **Education Relevance (20%)** - Field of study alignment
- **Experience Level (20%)** - Match experience with job type
- **Location Match (10%)** - Remote/location preferences
- **Profile Completeness (10%)** - Reward complete profiles

### Mentor Matching (0-100 score)

- **Skill Overlap (35%)** - Student skills vs mentor expertise
- **Career Alignment (25%)** - Career path similarity
- **Mentor Quality (25%)** - Rating and session count
- **Education Relevance (15%)** - Field alignment

**Implementation**: See `backend/app/services/ai_matching.py`

---

## 🔒 Security Features

- ✅ JWT Authentication with refresh tokens
- ✅ Password hashing with Bcrypt
- ✅ CORS protection
- ✅ Rate limiting
- ✅ Input validation
- ✅ SQL injection protection (SQLAlchemy ORM)
- ✅ XSS protection
- ✅ Soft deletes for data retention

---

## 📱 Real-Time Features (WebSockets)

### Messaging Events

**Client → Server:**
- `connect` - Authenticate connection
- `join_conversation` - Join conversation room
- `send_message` - Send message
- `typing` - Typing indicator
- `mark_read` - Mark messages as read

**Server → Client:**
- `connected` - Connection confirmed
- `new_message` - Receive message
- `user_typing` - User typing status

**WebSocket URL**: `ws://localhost:5000`

---

## 🧪 Testing

### Backend Tests

```bash
cd backend
pytest
pytest --cov=app tests/
```

### Frontend Tests

```bash
cd frontend
npm run test
```

---

## 📦 Project Structure

```
Collabio/
├── backend/                    # Flask API
│   ├── app/
│   │   ├── models/            # SQLAlchemy models
│   │   ├── routes/            # API blueprints
│   │   ├── services/          # Business logic
│   │   ├── websockets/        # Socket.IO handlers
│   │   └── utils/             # Helpers
│   ├── migrations/            # SQL migrations
│   ├── uploads/               # File storage
│   └── run.py                # Entry point
│
├── frontend/                  # React App
│   ├── src/
│   │   ├── pages/            # Route components
│   │   ├── components/       # UI components
│   │   ├── services/         # API layer
│   │   └── hooks/            # Custom hooks
│   └── package.json
│
├── SETUP_GUIDE.md            # Detailed setup
└── README.md                 # This file
```

---

## 🌟 Features Breakdown

### For Students
- ✅ Complete profile with education, experience, skills
- ✅ AI-powered job recommendations
- ✅ Apply to jobs and track applications
- ✅ Find and connect with mentors
- ✅ Enroll in courses and track progress
- ✅ Use AI tools (resume builder, interview prep, skill gap analysis)
- ✅ Real-time messaging with employers and mentors
- ✅ Social feed for networking

### For Employers
- ✅ Post job listings
- ✅ Review applications
- ✅ Update application status
- ✅ Message candidates
- ✅ Manage company profile

### For Mentors
- ✅ Create mentor profile
- ✅ Receive mentorship requests
- ✅ Schedule sessions
- ✅ Receive reviews and ratings
- ✅ Message students

---

## 🚀 Deployment

### Backend (Production)

```bash
# Using Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 "app:create_app()"

# With Docker
docker build -t collabio-backend .
docker run -p 5000:5000 collabio-backend
```

### Frontend (Production)

```bash
# Build
npm run build

# Deploy to Vercel/Netlify
# Or serve with nginx/apache
```

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/AmazingFeature`
3. Commit changes: `git commit -m 'Add AmazingFeature'`
4. Push to branch: `git push origin feature/AmazingFeature`
5. Open Pull Request

---

## 📝 License

This project is for educational purposes.

---

## 👥 Authors

Built for Database Course Project

---

## 🙏 Acknowledgments

- shadcn/ui for beautiful components
- Flask community for excellent documentation
- React team for the amazing framework

---

## 📞 Support & Issues

For detailed setup instructions, see **[SETUP_GUIDE.md](SETUP_GUIDE.md)**

For API documentation, see **[backend/README.md](backend/README.md)**

---

<div align="center">

**⭐ Star this repo if you find it helpful! ⭐**

Made with ❤️ using Flask, React, PostgreSQL, and Python

</div>
