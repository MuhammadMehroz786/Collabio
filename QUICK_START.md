# 🚀 Quick Start - Get Collabio Running in 2 Minutes

## ✅ Configuration Complete

Your Collabio platform is fully configured with:
- ✅ Backend .env file (with secure keys)
- ✅ Frontend .env file
- ✅ Startup scripts created
- ✅ All code files in place

## 🎯 Start the Application

### Option 1: Automatic Start (Recommended)

Run this single command to start both backend and frontend:

```bash
cd /Users/apple/Desktop/Collabio
./start-all.sh
```

This will:
- Create virtual environment (if needed)
- Install Python dependencies (if needed)
- Create database (if needed)
- Run migrations (if needed)
- Install Node modules (if needed)
- Start backend on http://localhost:5000
- Start frontend on http://localhost:5173

### Option 2: Manual Start (Two Terminals)

**Terminal 1 - Backend:**
```bash
cd /Users/apple/Desktop/Collabio
./start-backend.sh
```

**Terminal 2 - Frontend:**
```bash
cd /Users/apple/Desktop/Collabio
./start-frontend.sh
```

## 📝 First Time Setup

The startup scripts will automatically handle:

1. **Virtual Environment**: Creates `backend/venv/` if not exists
2. **Dependencies**: Installs from `requirements.txt` and `package.json`
3. **Database**: Creates `collabio_db` if not exists
4. **Migrations**: Runs initial schema SQL
5. **Upload Folders**: Creates required directories

## 🎉 Access the Application

Once both servers are running:

1. **Open Browser**: http://localhost:5173
2. **Click**: "Get Started" → "I'm a Student"
3. **Register** with:
   - Email: your@email.com
   - Password: Must include uppercase, lowercase, number, special char (min 8 chars)
   - Full Name: Your Name
4. **Start Exploring!**

## 🔧 Troubleshooting

### Backend Issues

**Database Connection Error:**
```bash
# Make sure PostgreSQL is running
brew services list | grep postgresql  # Mac
sudo systemctl status postgresql      # Linux

# If not running, start it:
brew services start postgresql        # Mac
sudo systemctl start postgresql       # Linux
```

**Port 5000 Already in Use:**
```bash
# Find and kill the process
lsof -ti:5000 | xargs kill -9
```

### Frontend Issues

**Port 5173 Already in Use:**
```bash
# Find and kill the process
lsof -ti:5173 | xargs kill -9
```

**Connection Refused:**
- Make sure backend is running on port 5000
- Check backend terminal for errors

## 📱 What You Can Do

### As a Student:
- ✅ Complete your profile with education, experience, skills
- ✅ Browse and apply to jobs
- ✅ Get AI-powered job recommendations
- ✅ Find mentors and request mentorship
- ✅ Enroll in courses
- ✅ Use AI tools (resume builder, career counselor, interview prep)
- ✅ Post on social feed
- ✅ Message employers and mentors

### Test Accounts

Create test accounts for different user types:

**Student:**
```
Email: student@test.com
Password: Test123!@#
```

**Employer:**
```
Email: employer@test.com
Password: Test123!@#
```

**Mentor:**
```
Email: mentor@test.com
Password: Test123!@#
```

## 📊 Database Access

To view database directly:

```bash
psql -U postgres -d collabio_db

# Useful queries:
\dt                           # List all tables
SELECT * FROM users;          # View users
SELECT * FROM jobs;           # View jobs
SELECT * FROM student_profiles; # View student profiles
```

## 🛑 Stop the Servers

Press `Ctrl + C` in each terminal window to stop the servers.

## 📚 Next Steps

1. **Explore Features**: Try all the features mentioned above
2. **Add Test Data**: Create multiple test accounts and jobs
3. **Read Documentation**:
   - `SETUP_GUIDE.md` - Detailed setup instructions
   - `backend/README.md` - API documentation
   - `frontend/src/services/README.md` - Frontend API usage
4. **Customize**: Modify colors, branding, add features

## 🔗 Important URLs

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:5000/api/v1
- **WebSocket**: ws://localhost:5000

## 💡 Development Tips

### Backend Development:
```bash
# Activate virtual environment
cd backend
source venv/bin/activate

# Run Flask shell
python
>>> from app import create_app, db
>>> app = create_app()
>>> with app.app_context():
...     # Database operations here
```

### Frontend Development:
```bash
# Install new package
cd frontend
npm install package-name

# Build for production
npm run build
```

### Database Operations:
```bash
# Backup database
pg_dump -U postgres collabio_db > backup.sql

# Restore database
psql -U postgres collabio_db < backup.sql

# Reset database
dropdb -U postgres collabio_db
createdb -U postgres collabio_db
psql -U postgres -d collabio_db -f backend/migrations/001_initial_schema.sql
```

## 🎊 You're All Set!

Your Collabio platform is ready to use. Enjoy building your Database Project! 🚀

---

**Need Help?**
- Check `SETUP_GUIDE.md` for detailed information
- Check `README.md` for project overview
- Check terminal logs for error messages
