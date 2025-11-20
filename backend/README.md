# Collabio Backend API

AI-Powered Career Platform Backend built with Flask, PostgreSQL, and WebSockets.

## Tech Stack

- **Framework**: Flask 3.0
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: JWT (Flask-JWT-Extended)
- **Real-time**: Flask-SocketIO with WebSockets
- **Caching**: Redis
- **File Storage**: Local (upgradeable to S3)

## Features

- User authentication (Students, Employers, Mentors)
- Job listings and applications
- Mentorship matching and sessions
- Real-time messaging with WebSockets
- AI-powered job/mentor matching
- Course management and enrollments
- Social feed (posts, likes, comments)
- File upload handling
- Soft delete architecture
- Rate limiting and security

## Project Structure

```
backend/
├── app/
│   ├── __init__.py              # Flask app factory
│   ├── config.py                # Configuration
│   ├── extensions.py            # Flask extensions
│   ├── models/                  # SQLAlchemy models
│   │   ├── base.py              # Base model with mixins
│   │   ├── user.py              # User authentication
│   │   ├── student.py           # Student profiles
│   │   ├── employer.py          # Employer profiles
│   │   ├── mentor.py            # Mentor profiles
│   │   ├── job.py               # Job listings
│   │   ├── messaging.py         # Messages & conversations
│   │   ├── course.py            # Courses & enrollments
│   │   └── all_models.py        # Consolidated models
│   ├── routes/                  # API endpoints (blueprints)
│   │   ├── auth.py              # Authentication routes
│   │   ├── students.py          # Student endpoints
│   │   ├── jobs.py              # Job endpoints
│   │   ├── mentors.py           # Mentor endpoints
│   │   ├── messaging.py         # Messaging endpoints
│   │   ├── courses.py           # Course endpoints
│   │   ├── social.py            # Social feed endpoints
│   │   └── ai_tools.py          # AI tools endpoints
│   ├── services/                # Business logic
│   │   └── ai_matching.py       # AI matching algorithms
│   ├── websockets/              # WebSocket event handlers
│   │   └── __init__.py          # Socket.IO events
│   └── utils/                   # Utility functions
│       ├── auth.py              # Auth decorators & helpers
│       ├── validators.py        # Input validation
│       ├── file_handler.py      # File upload/download
│       └── helpers.py           # General helpers
├── migrations/                  # Database migrations
│   └── 001_initial_schema.sql  # Initial database schema
├── uploads/                     # Local file storage
│   ├── profiles/                # Profile pictures
│   ├── resumes/                 # Resume files
│   ├── logos/                   # Company logos
│   ├── courses/                 # Course materials
│   └── attachments/             # Message attachments
├── logs/                        # Application logs
├── .env.example                 # Environment variables template
├── requirements.txt             # Python dependencies
├── run.py                       # Application entry point
└── README.md                    # This file
```

## Setup Instructions

### Prerequisites

- Python 3.10+
- PostgreSQL 14+
- Redis 6+ (optional, for caching and WebSocket queue)
- pip or virtualenv

### 1. Clone and Navigate

```bash
cd backend
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Setup PostgreSQL Database

```bash
# Create database
psql -U postgres
CREATE DATABASE collabio_db;
CREATE USER collabio_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE collabio_db TO collabio_user;
\q

# Run initial migration
psql -U collabio_user -d collabio_db -f migrations/001_initial_schema.sql
```

### 5. Configure Environment

```bash
cp .env.example .env
# Edit .env with your configuration
```

**Key environment variables:**
```env
DATABASE_URL=postgresql://collabio_user:your_password@localhost:5432/collabio_db
SECRET_KEY=your-super-secret-key-change-this
JWT_SECRET_KEY=your-jwt-secret-key-change-this
FLASK_ENV=development
```

### 6. Initialize Database (Alternative using Flask-Migrate)

```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### 7. Run Development Server

```bash
# Option 1: Using run.py
python run.py

# Option 2: Using Flask CLI
flask run

# Option 3: With SocketIO support
python run.py
```

Server will start on `http://localhost:5000`

## API Endpoints

### Authentication (`/api/v1/auth`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/register` | Register new user |
| POST | `/login` | Login user |
| POST | `/refresh` | Refresh access token |
| GET | `/me` | Get current user info |
| POST | `/change-password` | Change password |

### Students (`/api/v1/students`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | List all students (paginated) |
| GET | `/<id>` | Get student profile |
| GET | `/me` | Get my profile |
| PUT | `/me` | Update my profile |
| POST | `/me/education` | Add education |
| POST | `/me/experience` | Add experience |
| POST | `/me/skills` | Add skill |

### Jobs (`/api/v1/jobs`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | List all jobs (filterable) |
| GET | `/<id>` | Get job details |
| POST | `/` | Create job (employers only) |
| PUT | `/<id>` | Update job (employers only) |
| DELETE | `/<id>` | Delete job (employers only) |
| POST | `/<id>/apply` | Apply to job (students only) |
| POST | `/<id>/save` | Save job |
| GET | `/recommendations` | Get AI-matched jobs |

### Mentors (`/api/v1/mentors`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | List all mentors |
| GET | `/<id>` | Get mentor profile |
| POST | `/<id>/request` | Request mentorship |
| GET | `/recommendations` | Get AI-matched mentors |

### Messaging (`/api/v1/messages`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/conversations` | Get my conversations |
| GET | `/conversations/<id>` | Get conversation messages |
| POST | `/conversations` | Create conversation |
| POST | `/conversations/<id>/messages` | Send message |

### Courses (`/api/v1/courses`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | List all courses |
| GET | `/<id>` | Get course details |
| POST | `/<id>/enroll` | Enroll in course |
| GET | `/my-enrollments` | Get my courses |

## WebSocket Events

Connect to WebSocket: `ws://localhost:5000`

### Client → Server

| Event | Data | Description |
|-------|------|-------------|
| `connect` | `{token}` | Authenticate connection |
| `join_conversation` | `{conversation_id}` | Join conversation room |
| `send_message` | `{conversation_id, message_text}` | Send message |
| `typing` | `{conversation_id, is_typing}` | Typing indicator |
| `mark_read` | `{conversation_id}` | Mark messages as read |

### Server → Client

| Event | Data | Description |
|-------|------|-------------|
| `connected` | `{message}` | Connection confirmed |
| `new_message` | `{message object}` | New message received |
| `user_typing` | `{user_id, is_typing}` | User typing status |
| `error` | `{message}` | Error occurred |

## AI Matching Algorithm

The AI matching service calculates match scores (0-100) between:

### Job Matching
- **Skill Matching** (40%): Compare student skills with job requirements
- **Education Relevance** (20%): Match field of study with job domain
- **Experience Level** (20%): Align experience with job type
- **Location Match** (10%): Consider remote/location preferences
- **Profile Completeness** (10%): Reward complete profiles

### Mentor Matching
- **Skill Overlap** (35%): Match student skills with mentor expertise
- **Career Alignment** (25%): Align with mentor's career path
- **Mentor Quality** (25%): Consider rating and session count
- **Education Relevance** (15%): Match field of study with mentor's domain

## Database Schema Highlights

- **15 Main Tables**: Users, Profiles, Jobs, Mentorship, Messaging, Courses, Social, etc.
- **Soft Deletes**: All tables support soft delete (`deleted_at` column)
- **Triggers**: Auto-update counters (likes, comments, ratings)
- **Indexes**: Optimized for common queries
- **UUID Primary Keys**: For better distribution and security

## Security Features

- **JWT Authentication**: Secure token-based auth
- **Password Hashing**: Bcrypt encryption
- **Rate Limiting**: Prevent API abuse
- **CORS Configuration**: Controlled cross-origin requests
- **Input Validation**: Comprehensive validation layer
- **SQL Injection Protection**: SQLAlchemy ORM
- **Soft Deletes**: Data retention and recovery

## Development Tips

### Adding New Routes

1. Create blueprint in `app/routes/your_route.py`
2. Register in `app/__init__.py`
3. Follow existing patterns (see `ROUTES_TEMPLATE.py`)

### Adding New Models

1. Create model in `app/models/your_model.py`
2. Inherit from `BaseModel` and mixins
3. Import in `app/models/__init__.py`
4. Generate migration: `flask db migrate -m "Add your_model"`
5. Apply migration: `flask db upgrade`

### Running Tests

```bash
pytest
pytest --cov=app tests/
```

### Database Migrations

```bash
# Create migration
flask db migrate -m "Description"

# Apply migration
flask db upgrade

# Rollback
flask db downgrade
```

## Production Deployment

### Using Gunicorn

```bash
gunicorn -w 4 -b 0.0.0.0:5000 "app:create_app()"
```

### Using Docker

```dockerfile
# Create Dockerfile (example)
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:create_app()"]
```

### Environment Variables for Production

```env
FLASK_ENV=production
SECRET_KEY=<strong-secret-key>
JWT_SECRET_KEY=<strong-jwt-secret>
DATABASE_URL=postgresql://user:pass@host:5432/db
REDIS_URL=redis://host:6379/0
```

## Troubleshooting

### Database Connection Error
```bash
# Check PostgreSQL is running
sudo systemctl status postgresql

# Check connection
psql -U collabio_user -d collabio_db
```

### Redis Connection Error (Optional)
```bash
# Check Redis is running
redis-cli ping

# Should return: PONG
```

### Import Errors
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Migration Issues
```bash
# Reset migrations
flask db downgrade base
flask db upgrade
```

## Next Steps

1. **Complete Route Implementations**: Finish students.py, jobs.py, mentors.py, etc. using ROUTES_TEMPLATE.py
2. **Add Email Service**: Implement email verification and notifications
3. **Enhance AI Matching**: Integrate ML models for better matching
4. **Add Tests**: Write unit and integration tests
5. **API Documentation**: Generate Swagger/OpenAPI docs
6. **File Upload to S3**: Migrate from local to cloud storage
7. **Monitoring**: Add logging and monitoring (Sentry, DataDog)
8. **CI/CD**: Setup automated testing and deployment

## Contributing

1. Create feature branch
2. Follow existing code patterns
3. Write tests
4. Submit pull request

## License

Proprietary - Collabio Platform

## Support

For issues and questions, contact the development team.

---

**Built with ❤️ using Flask, PostgreSQL, and Python**
