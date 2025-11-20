# Collabio - Complete Setup Guide

AI-Powered Career Platform for Students with Flask Backend + React Frontend

## 🎯 Project Overview

**Collabio** is a complete full-stack application with:
- **Backend**: Flask + PostgreSQL + WebSockets + AI Matching
- **Frontend**: React + TypeScript + TailwindCSS + shadcn/ui
- **Features**: Jobs, Mentorship, Messaging, Courses, Social Feed, AI Tools

---

## 📋 Prerequisites

Before starting, ensure you have:

- **Python 3.10+** ([Download](https://www.python.org/downloads/))
- **Node.js 18+** ([Download](https://nodejs.org/))
- **PostgreSQL 14+** ([Download](https://www.postgresql.org/download/))
- **Git** ([Download](https://git-scm.com/downloads))
- **Redis** (Optional, for caching) ([Download](https://redis.io/download))

---

## 🚀 Quick Start (5 Steps)

### Step 1: Setup PostgreSQL Database

```bash
# Login to PostgreSQL
psql -U postgres

# Create database and user
CREATE DATABASE collabio_db;
CREATE USER collabio_user WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE collabio_db TO collabio_user;
\q
```

### Step 2: Setup Backend

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Mac/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Edit .env with your database credentials
# Update: DATABASE_URL, SECRET_KEY, JWT_SECRET_KEY

# Run database migration
psql -U collabio_user -d collabio_db -f migrations/001_initial_schema.sql

# Start backend server
python run.py
```

Backend will run on: **http://localhost:5000**

### Step 3: Setup Frontend

```bash
# Open new terminal, navigate to frontend
cd frontend

# Install dependencies
npm install

# Create .env file
cp .env.example .env

# Start frontend development server
npm run dev
```

Frontend will run on: **http://localhost:5173**

### Step 4: Create Test Data (Optional)

```bash
# Use provided SQL or API endpoints to create test users
# See section "Creating Test Data" below
```

### Step 5: Test the Application

1. Open browser: **http://localhost:5173**
2. Click "Get Started" → "I'm a Student"
3. Register a new account
4. Start exploring!

---

## 📁 Project Structure

```
Collabio/
├── backend/                    # Flask Backend
│   ├── app/
│   │   ├── models/            # Database models
│   │   ├── routes/            # API endpoints
│   │   ├── services/          # Business logic (AI matching)
│   │   ├── websockets/        # WebSocket handlers
│   │   └── utils/             # Helpers & validators
│   ├── migrations/            # SQL migrations
│   ├── uploads/               # Local file storage
│   ├── .env.example          # Environment template
│   ├── requirements.txt       # Python dependencies
│   └── run.py                # Entry point
│
├── frontend/                  # React Frontend
│   ├── src/
│   │   ├── pages/            # Route components
│   │   ├── components/       # Reusable components
│   │   ├── services/         # API client layer
│   │   └── hooks/            # Custom React hooks
│   ├── .env.example          # Environment template
│   └── package.json          # Node dependencies
│
├── SETUP_GUIDE.md            # This file
└── README.md                 # Project documentation
```

---

## 🔧 Detailed Setup Instructions

### Backend Configuration

**1. Environment Variables (backend/.env)**

```env
# Flask
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your-super-secret-key-min-32-chars
DEBUG=True

# Database
DATABASE_URL=postgresql://collabio_user:your_password@localhost:5432/collabio_db

# JWT
JWT_SECRET_KEY=your-jwt-secret-key-min-32-chars
JWT_ACCESS_TOKEN_EXPIRES=3600
JWT_REFRESH_TOKEN_EXPIRES=2592000

# CORS (Frontend URL)
CORS_ORIGINS=http://localhost:5173

# File Upload
UPLOAD_FOLDER=./uploads
MAX_FILE_SIZE=10485760

# Redis (Optional)
REDIS_URL=redis://localhost:6379/0
SOCKETIO_MESSAGE_QUEUE=redis://localhost:6379/0
```

**2. Generate Secure Keys**

```bash
# Generate SECRET_KEY
python -c "import secrets; print(secrets.token_hex(32))"

# Generate JWT_SECRET_KEY
python -c "import secrets; print(secrets.token_hex(32))"
```

**3. Database Migration**

```bash
# Option 1: Direct SQL
psql -U collabio_user -d collabio_db -f migrations/001_initial_schema.sql

# Option 2: Flask-Migrate (if you prefer)
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

---

### Frontend Configuration

**1. Environment Variables (frontend/.env)**

```env
VITE_API_BASE_URL=http://localhost:5000/api/v1
VITE_WS_URL=ws://localhost:5000
VITE_APP_NAME=Collabio
```

**2. Install Dependencies**

```bash
cd frontend
npm install
```

**3. Start Development Server**

```bash
npm run dev
```

---

## 🧪 Creating Test Data

### Option 1: Using API Endpoints

```bash
# Register a student
curl -X POST http://localhost:5000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "student@test.com",
    "password": "Test123!@#",
    "user_type": "student",
    "full_name": "Test Student"
  }'

# Register an employer
curl -X POST http://localhost:5000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "employer@test.com",
    "password": "Test123!@#",
    "user_type": "employer",
    "company_name": "Test Company"
  }'

# Register a mentor
curl -X POST http://localhost:5000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "mentor@test.com",
    "password": "Test123!@#",
    "user_type": "mentor",
    "full_name": "Test Mentor",
    "current_role": "Senior Engineer",
    "current_company": "Tech Corp"
  }'
```

### Option 2: Direct SQL Inserts

```sql
-- Insert sample jobs
INSERT INTO jobs (title, company_name, description, job_type, location, salary_min, salary_max)
VALUES
  ('Software Engineer Intern', 'TechCorp', 'Great opportunity for students', 'internship', 'Remote', 25, 35),
  ('Full Stack Developer', 'StartupXYZ', 'Build amazing products', 'full-time', 'San Francisco', 80000, 120000);

-- Insert sample courses
INSERT INTO courses (title, description, category, difficulty_level, duration_weeks)
VALUES
  ('React Fundamentals', 'Learn React from scratch', 'Web Development', 'beginner', 4),
  ('System Design', 'Master system design interviews', 'Engineering', 'advanced', 8);
```

---

## 🔌 API Endpoints Reference

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login
- `GET /api/v1/auth/me` - Get current user
- `POST /api/v1/auth/change-password` - Change password

### Jobs
- `GET /api/v1/jobs` - List all jobs (with filters)
- `GET /api/v1/jobs/:id` - Get job details
- `POST /api/v1/jobs` - Create job (employer)
- `POST /api/v1/jobs/:id/apply` - Apply to job (student)
- `GET /api/v1/jobs/recommendations` - AI-matched jobs

### Students
- `GET /api/v1/students/me` - Get my profile
- `PUT /api/v1/students/me` - Update profile
- `POST /api/v1/students/me/education` - Add education
- `POST /api/v1/students/me/experience` - Add experience
- `POST /api/v1/students/me/skills` - Add skill

### Mentors
- `GET /api/v1/mentors` - List mentors
- `POST /api/v1/mentors/:id/request` - Request mentorship
- `GET /api/v1/mentors/recommendations` - AI-matched mentors

### Messaging
- `GET /api/v1/messages/conversations` - My conversations
- `POST /api/v1/messages/conversations` - Create conversation
- `POST /api/v1/messages/conversations/:id/messages` - Send message

### Courses
- `GET /api/v1/courses` - List courses
- `POST /api/v1/courses/:id/enroll` - Enroll in course
- `GET /api/v1/courses/my-enrollments` - My courses

### AI Tools
- `POST /api/v1/ai-tools/resume-builder` - Analyze resume
- `POST /api/v1/ai-tools/career-counselor` - Get career advice
- `POST /api/v1/ai-tools/interview-prep` - Practice interviews
- `POST /api/v1/ai-tools/skill-gap` - Analyze skill gaps

---

## 💡 Usage Examples (Frontend)

### Example: Login

```typescript
import { authService } from '@/services';

const handleLogin = async (email: string, password: string) => {
  try {
    const response = await authService.login({ email, password });
    console.log('Logged in:', response.data.user);
    // Redirect to dashboard
    navigate('/student');
  } catch (error) {
    console.error('Login failed:', error);
  }
};
```

### Example: Fetch Jobs

```typescript
import { jobsService } from '@/services';

const fetchJobs = async () => {
  try {
    const response = await jobsService.getAll({
      job_type: 'internship',
      location: 'Remote'
    });
    console.log('Jobs:', response.data);
  } catch (error) {
    console.error('Failed to fetch jobs:', error);
  }
};
```

### Example: Apply to Job

```typescript
import { jobsService } from '@/services';

const applyToJob = async (jobId: string) => {
  try {
    await jobsService.apply(jobId, {
      cover_letter: 'I am very interested...'
    });
    toast.success('Application submitted!');
  } catch (error) {
    toast.error('Application failed');
  }
};
```

---

## 🐛 Troubleshooting

### Backend Issues

**Issue: Database connection error**
```bash
# Check PostgreSQL is running
sudo systemctl status postgresql  # Linux
brew services list | grep postgresql  # Mac

# Test connection
psql -U collabio_user -d collabio_db -h localhost
```

**Issue: Module not found**
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

**Issue: Port 5000 already in use**
```bash
# Change port in run.py or kill process
lsof -ti:5000 | xargs kill -9
```

### Frontend Issues

**Issue: API connection error**
- Check `VITE_API_BASE_URL` in `.env`
- Ensure backend is running on correct port
- Check CORS settings in backend

**Issue: Build errors**
```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

---

## 🚀 Production Deployment

### Backend (Gunicorn + Nginx)

```bash
# Install gunicorn
pip install gunicorn

# Run with gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 "app:create_app()"
```

### Frontend (Build & Deploy)

```bash
# Build for production
npm run build

# Output will be in dist/ folder
# Deploy to Vercel, Netlify, or any static host
```

### Environment Variables for Production

**Backend:**
- Set `FLASK_ENV=production`
- Use strong `SECRET_KEY` and `JWT_SECRET_KEY`
- Use production database URL
- Set up SSL/HTTPS

**Frontend:**
- Update `VITE_API_BASE_URL` to production API URL
- Use HTTPS for WebSocket connections

---

## 📊 Database Schema Overview

- **15 Main Tables**: Users, Profiles, Jobs, Mentorship, Messaging, Courses, Social
- **Soft Deletes**: All tables support soft delete
- **Triggers**: Auto-update counters (likes, comments, ratings)
- **Indexes**: Optimized for performance
- **Full Schema**: See `backend/migrations/001_initial_schema.sql`

---

## 🤝 Contributing

1. Create feature branch: `git checkout -b feature/amazing-feature`
2. Commit changes: `git commit -m 'Add amazing feature'`
3. Push to branch: `git push origin feature/amazing-feature`
4. Open Pull Request

---

## 📝 Next Steps

1. ✅ Setup completed? Test all features
2. 📝 Add more test data for realistic experience
3. 🎨 Customize UI colors and branding
4. 🔒 Add email verification (integrate mail service)
5. 🤖 Enhance AI matching with ML models
6. 📱 Create mobile app (React Native)
7. 🚀 Deploy to production

---

## 📞 Support

- **Backend Issues**: Check `backend/README.md`
- **Frontend Issues**: Check `frontend/README.md`
- **Database Schema**: See `migrations/001_initial_schema.sql`
- **API Routes**: See `backend/app/routes/`

---

## 🎉 Congratulations!

Your Collabio platform is now fully set up and ready to use!

**Test URLs:**
- Frontend: http://localhost:5173
- Backend API: http://localhost:5000/api/v1
- API Health: http://localhost:5000/api/v1/auth/me (with token)

---

**Built with ❤️ for your Database Project**
