# Collabio Demo Mode Guide

## Overview

Collabio now includes a **Demo Mode** that allows you to showcase the entire platform with full UI functionality using mock data - **no backend required!** This is perfect for presentations, demos, and testing the user interface.

## Quick Start

### Running the Demo

1. **Start the Frontend**:
   ```bash
   cd frontend
   npm run dev
   ```

2. **Open in Browser**:
   Navigate to `http://localhost:8080`

3. **Login**:
   - Use ANY email and password to login
   - For Student view: Use email with "student" in it (e.g., `student@demo.com`)
   - For Employer view: Use email with "employer" in it (e.g., `employer@demo.com`)

That's it! The entire platform is now functional with realistic mock data.

---

## Demo Mode Features

### ✅ Fully Functional Features

All UI features work perfectly in demo mode:

#### 🎓 Student Features
- **Dashboard**: View personalized feed, job recommendations, and activity
- **Job Board**: Browse 5+ realistic job listings with filters
- **Job Applications**: Apply to jobs and track application status
- **Profile Management**: Edit profile, add education, experience, and skills
- **Courses**: Browse and enroll in courses with progress tracking
- **Mentorship**: Find mentors by expertise and request sessions
- **AI Tools**:
  - Resume Builder with AI suggestions
  - Career Counselor for personalized advice
  - Interview Prep with practice questions
  - Skill Gap Analysis
- **Social Feed**: View posts, like, comment, and create new posts
- **Messages**: Real-time messaging interface with conversations

#### 💼 Employer Features
- **Dashboard**: Overview of job postings and applications
- **Job Management**: Create, edit, and manage job postings
- **Application Review**: Review and manage student applications
- **Messages**: Communicate with applicants
- **Analytics**: View job statistics and applicant data

---

## Mock Data Overview

The demo includes comprehensive, realistic mock data:

### Users
- **Student**: Alex Johnson (Computer Science student)
- **Employer**: Sarah Williams (TechCorp Solutions recruiter)

### Content
- **5 Job Listings**: Various positions from different companies
  - Full Stack Developer Intern (TechCorp Solutions)
  - Frontend Developer (InnovateLabs)
  - Data Science Intern (DataMinds AI)
  - Backend Engineer (TechCorp Solutions)
  - UI/UX Designer (Creative Studio)

- **3 Mentors**: Industry professionals ready to help
  - Dr. Emily Chen (Software Engineering)
  - Michael Rodriguez (Data Science)
  - Jessica Park (Product Management)

- **4 Courses**: Free professional development courses
  - Advanced React Development
  - Machine Learning Fundamentals
  - Full Stack Web Development Bootcamp
  - Data Structures & Algorithms

- **5+ Social Posts**: Realistic student interactions
- **Multiple Conversations**: Sample messaging threads
- **Student Profile**: Complete with education, experience, and skills

---

## Configuration

### Enabling/Disabling Demo Mode

Demo mode is controlled by the environment variable in `frontend/.env`:

```env
# Set to 'true' for demo mode (mock data)
VITE_DEMO_MODE=true

# Set to 'false' to use real backend
VITE_DEMO_MODE=false
```

### Features of Demo Mode

When `VITE_DEMO_MODE=true`:
- ✅ All API calls are intercepted and return mock data
- ✅ No backend server required
- ✅ Realistic network delays simulated (300-1500ms)
- ✅ File uploads are simulated
- ✅ Authentication works with ANY credentials
- ✅ Visual banner indicates demo mode is active
- ✅ All CRUD operations work (changes persist in memory during session)

---

## Demo Walkthrough

### Student Journey Demo Script

Here's a suggested flow for demonstrating the platform:

1. **Start at Landing Page** (`/`)
   - Show the modern, professional landing page
   - Click "Get Started"

2. **Login** (`/login`)
   - Email: `demo.student@collabio.com`
   - Password: `anything`
   - Notice the demo banner at the top

3. **Student Dashboard** (`/student`)
   - Overview of personalized feed
   - Quick stats and recommendations
   - Recent activity

4. **Explore Jobs** (`/student/jobs`)
   - Browse job listings
   - Use filters (remote, location, type)
   - Click on a job to view details
   - Apply to a job with cover letter

5. **Check Applications**
   - View application status
   - See previously applied jobs

6. **View Profile** (`/student/profile`)
   - Complete student profile with:
     - Education history
     - Work experience
     - Skills with proficiency levels
     - Social links (GitHub, LinkedIn, Portfolio)

7. **Edit Profile** (`/student/profile/edit`)
   - Update profile information
   - Add new skills
   - Upload resume (simulated)

8. **Browse Courses** (`/student/courses`)
   - View available courses
   - Enroll in a course
   - Track progress

9. **Find Mentors** (`/student/mentorship`)
   - Browse mentor profiles
   - Filter by expertise
   - Request mentorship session

10. **AI Tools** (`/student/ai-tools`)
    - Try Resume Builder
    - Get career counseling advice
    - Practice interview questions
    - Analyze skill gaps

11. **Social Feed** (Dashboard)
    - View posts from other students
    - Like and comment on posts
    - Create a new post

12. **Messages** (`/student/messages`)
    - View conversations
    - Send messages
    - Real-time chat interface

### Employer Journey Demo Script

1. **Login as Employer**
   - Email: `demo.employer@techcorp.com`
   - Password: `anything`

2. **Employer Dashboard** (`/employer`)
   - View job postings overview
   - See application statistics
   - Review recent applications

3. **Manage Jobs**
   - Create new job posting
   - Edit existing jobs
   - View job analytics

4. **Review Applications**
   - See applicant details
   - Review resumes
   - Update application status

5. **Messages** (`/employer/messages`)
   - Communicate with applicants
   - Schedule interviews

---

## Benefits of Demo Mode

### For Presentations
- ✅ No backend setup required
- ✅ No database needed
- ✅ Works offline (after initial load)
- ✅ Consistent, reliable data
- ✅ Fast and responsive

### For Development
- ✅ Frontend development without backend
- ✅ UI/UX testing
- ✅ Quick prototyping
- ✅ Demo for stakeholders

### For Testing
- ✅ User flow testing
- ✅ UI component testing
- ✅ Visual regression testing
- ✅ Mobile responsiveness testing

---

## Switching Between Demo and Production

### Demo Mode (No Backend)
```env
VITE_DEMO_MODE=true
```
```bash
cd frontend
npm run dev
# Open http://localhost:8080
```

### Production Mode (With Backend)
```env
VITE_DEMO_MODE=false
VITE_API_BASE_URL=http://localhost:5001/api/v1
```
```bash
# Terminal 1 - Start Backend
cd backend
python run.py

# Terminal 2 - Start Frontend
cd frontend
npm run dev
```

---

## Customizing Mock Data

To customize the demo data, edit the file:
```
frontend/src/mocks/mockData.ts
```

You can modify:
- User profiles
- Job listings
- Courses
- Mentors
- Social posts
- Messages
- And more!

The mock API handler (`frontend/src/mocks/mockApi.ts`) controls how the mock data is served.

---

## Tips for a Great Demo

1. **Prepare Your Browser**
   - Open in incognito/private mode for a clean session
   - Use a large screen or presentation mode
   - Zoom to 110-125% for better visibility

2. **Highlight Key Features**
   - Show the comprehensive job board
   - Demonstrate the AI tools
   - Explore the social networking features
   - Show the mentorship platform

3. **Emphasize the Value**
   - All-in-one platform for students
   - AI-powered career guidance
   - Real-world job opportunities
   - Professional development courses
   - Networking and mentorship

4. **Interactive Elements**
   - Try applying to a job
   - Create a social post
   - Use an AI tool
   - Browse and enroll in a course

---

## Troubleshooting

### Demo Mode Not Working
1. Check `frontend/.env` has `VITE_DEMO_MODE=true`
2. Restart the dev server after changing .env
3. Clear browser cache and reload

### Data Not Appearing
1. Check browser console for errors
2. Verify mock files are imported correctly
3. Check network tab - requests should resolve instantly

### Visual Issues
1. Ensure all dependencies are installed: `npm install`
2. Clear Vite cache: `rm -rf frontend/node_modules/.vite`
3. Rebuild: `npm run dev`

---

## Support

For issues or questions:
- Check the browser console for detailed logs
- Review the mock API handler logs (look for `[MOCK API]` in console)
- Verify the demo mode banner is visible at the top

---

## Next Steps

After the demo, you can:
1. **Deploy Frontend Only**: Deploy to Vercel/Netlify with demo mode enabled
2. **Set Up Backend**: Follow SETUP_GUIDE.md for full production setup
3. **Customize**: Modify mock data and styling to match your needs
4. **Extend**: Add more mock endpoints or features

---

Happy Demoing! 🚀
