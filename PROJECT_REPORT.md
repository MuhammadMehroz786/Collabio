# COLLABIO - AI-POWERED CAREER PLATFORM
## Database Systems Project Report

---

<div align="center">

**Course:** Database Systems
**Semester:** Fall 2025
**Submitted Date:** November 26, 2025

</div>

---

## GROUP MEMBERS

| Name | Roll Number | Contribution |
|------|-------------|--------------|
| Mehroz Muneer | 23k0748 | Backend Development, Database Design, Integration |
| Dua Shafiq | 23k0825 | Testing, Frontend Development, UI/UX Design, Documentation |

---

## TABLE OF CONTENTS

1. [Introduction](#1-introduction)
2. [Targeted Audience](#2-targeted-audience)
3. [Project Scope](#3-project-scope)
4. [Functional Requirements](#4-functional-requirements)
5. [Non-Functional Requirements](#5-non-functional-requirements)
6. [Entity-Relationship (ER) Diagram](#6-entity-relationship-er-diagram)
7. [Normalized Schema](#7-normalized-schema)
8. [Conclusion](#8-conclusion)
9. [References](#9-references)

---

## 1. INTRODUCTION

### 1.1 Project Overview

**Collabio** is a comprehensive AI-powered career platform designed to bridge the gap between students, employers, and mentors. The platform leverages modern web technologies and artificial intelligence to create a seamless ecosystem for career development, job hunting, mentorship, and skill enhancement.

### 1.2 Problem Statement

Traditional job search platforms often fail to:
- Provide personalized job recommendations based on individual skills and aspirations
- Connect students with experienced mentors in their field of interest
- Offer integrated learning and skill development opportunities
- Enable real-time communication between stakeholders
- Track and analyze career progression effectively

### 1.3 Solution

Collabio addresses these challenges by providing:
- **AI-Powered Matching**: Intelligent algorithms that match students with relevant jobs and mentors
- **Integrated Mentorship**: Direct connection between students and industry professionals
- **Learning Hub**: Curated courses for skill development
- **Real-Time Communication**: WebSocket-based instant messaging
- **Career Tools**: AI-driven resume analysis, interview preparation, and skill gap analysis
- **Social Networking**: Professional networking through a social feed

### 1.4 Technology Stack

**Backend:**
- Flask 3.0 (Python Web Framework)
- PostgreSQL 14+ (Relational Database)
- SQLAlchemy (ORM)
- Flask-SocketIO (WebSocket Support)
- Flask-JWT-Extended (Authentication)
- Redis (Caching & Message Queue)

**Frontend:**
- React 18.3 with TypeScript
- Vite (Build Tool)
- TailwindCSS & shadcn/ui (Styling)
- React Router (Navigation)
- TanStack Query (State Management)

---

## 2. TARGETED AUDIENCE

### 2.1 Primary Users

#### **Students**
- **Demographics**: University/college students aged 18-25
- **Needs**:
  - Finding internships and entry-level positions
  - Connecting with mentors for career guidance
  - Building professional skills through courses
  - Networking with peers and professionals
  - Tracking job applications and progress

#### **Employers**
- **Demographics**: HR professionals and recruiters from companies of all sizes
- **Needs**:
  - Posting job opportunities and internships
  - Finding qualified candidates efficiently
  - Managing applications and candidate pipeline
  - Communicating with potential hires
  - Reviewing candidate profiles and portfolios

#### **Mentors**
- **Demographics**: Experienced professionals (3+ years experience) willing to guide students
- **Needs**:
  - Sharing expertise and giving back to the community
  - Managing mentorship requests and sessions
  - Building personal brand and reputation
  - Tracking mentee progress
  - Receiving feedback and reviews

### 2.2 Secondary Users

- **Educational Institutions**: For tracking student placements and career outcomes
- **Course Creators**: For hosting educational content
- **System Administrators**: For platform management and analytics

---

## 3. PROJECT SCOPE

### 3.1 In-Scope Features

#### **Core Features**
1. **User Management**
   - Multi-role authentication (Student, Employer, Mentor)
   - Profile management with detailed information
   - Education, experience, and skills tracking
   - File upload for resumes, profile pictures, and documents

2. **Job Management**
   - Job posting and listing
   - Advanced filtering and search
   - AI-powered job recommendations
   - Application tracking and status management
   - Saved jobs functionality

3. **Mentorship System**
   - Mentor discovery and profiles
   - AI-based mentor matching
   - Mentorship request workflow
   - Session scheduling and tracking
   - Review and rating system

4. **Real-Time Messaging**
   - One-on-one conversations
   - WebSocket-based instant messaging
   - Typing indicators
   - Read receipts
   - Message notifications

5. **Learning Platform**
   - Course catalog
   - Course enrollment and tracking
   - Progress monitoring
   - Lesson completion tracking

6. **Social Features**
   - Professional feed/timeline
   - Post creation and sharing
   - Likes and comments
   - Achievement showcase

7. **AI Career Tools**
   - Resume builder and analyzer
   - Career counseling chatbot
   - Interview preparation
   - Skill gap analysis

### 3.2 Out-of-Scope Features

- Video calling integration
- Payment gateway for premium features
- Mobile native applications
- Automated background verification
- Integration with third-party job boards
- Advanced analytics and reporting dashboard
- Multi-language support

### 3.3 System Boundaries

- **Platform**: Web-based application (no native mobile apps)
- **Geography**: Initially targeting single region (can be expanded)
- **Scale**: Designed for thousands of concurrent users
- **Data Storage**: On-premise or cloud-based PostgreSQL
- **File Storage**: Local storage (upgradeable to cloud storage)

---

## 4. FUNCTIONAL REQUIREMENTS

### 4.1 Authentication & Authorization (F-AUTH)

| ID | Requirement | Priority |
|----|-------------|----------|
| F-AUTH-01 | System shall allow users to register with email and password | High |
| F-AUTH-02 | System shall support three user types: Student, Employer, Mentor | High |
| F-AUTH-03 | System shall authenticate users using JWT tokens | High |
| F-AUTH-04 | System shall provide token refresh mechanism | Medium |
| F-AUTH-05 | System shall enforce password complexity requirements | High |
| F-AUTH-06 | System shall allow users to change their password | Medium |
| F-AUTH-07 | System shall maintain user sessions securely | High |

### 4.2 Student Management (F-STU)

| ID | Requirement | Priority |
|----|-------------|----------|
| F-STU-01 | Students shall create and update their profiles | High |
| F-STU-02 | Students shall add multiple education entries | High |
| F-STU-03 | Students shall add multiple work experiences | High |
| F-STU-04 | Students shall manage their skills list | High |
| F-STU-05 | Students shall upload profile pictures and resumes | Medium |
| F-STU-06 | Students shall view their application history | High |
| F-STU-07 | Students shall track course enrollments | Medium |

### 4.3 Job Management (F-JOB)

| ID | Requirement | Priority |
|----|-------------|----------|
| F-JOB-01 | Employers shall post job listings | High |
| F-JOB-02 | Employers shall edit and delete their job posts | High |
| F-JOB-03 | System shall display jobs with filtering options | High |
| F-JOB-04 | Students shall apply to jobs with cover letters | High |
| F-JOB-05 | Students shall save jobs for later | Medium |
| F-JOB-06 | Employers shall view applications for their jobs | High |
| F-JOB-07 | Employers shall update application status | High |
| F-JOB-08 | System shall provide AI-powered job recommendations | Medium |
| F-JOB-09 | System shall calculate match scores for job-student pairs | Medium |

### 4.4 Mentorship System (F-MEN)

| ID | Requirement | Priority |
|----|-------------|----------|
| F-MEN-01 | Mentors shall create detailed mentor profiles | High |
| F-MEN-02 | Mentors shall specify expertise areas | High |
| F-MEN-03 | Students shall search and filter mentors | High |
| F-MEN-04 | Students shall send mentorship requests | High |
| F-MEN-05 | Mentors shall accept or decline requests | High |
| F-MEN-06 | System shall track mentorship sessions | Medium |
| F-MEN-07 | Students shall review and rate mentors | Medium |
| F-MEN-08 | System shall provide AI-powered mentor recommendations | Medium |

### 4.5 Messaging System (F-MSG)

| ID | Requirement | Priority |
|----|-------------|----------|
| F-MSG-01 | Users shall send real-time messages | High |
| F-MSG-02 | System shall support one-on-one conversations | High |
| F-MSG-03 | System shall show typing indicators | Low |
| F-MSG-04 | System shall mark messages as read/unread | Medium |
| F-MSG-05 | Users shall receive message notifications | Medium |
| F-MSG-06 | System shall maintain message history | High |

### 4.6 Course Management (F-CRS)

| ID | Requirement | Priority |
|----|-------------|----------|
| F-CRS-01 | System shall display available courses | High |
| F-CRS-02 | Students shall enroll in courses | High |
| F-CRS-03 | System shall track course progress | Medium |
| F-CRS-04 | Students shall mark lessons as complete | Medium |
| F-CRS-05 | System shall show completion percentage | Low |

### 4.7 Social Features (F-SOC)

| ID | Requirement | Priority |
|----|-------------|----------|
| F-SOC-01 | Users shall create posts on feed | Medium |
| F-SOC-02 | Users shall like and comment on posts | Medium |
| F-SOC-03 | System shall display personalized feed | Medium |
| F-SOC-04 | Users shall track connections | Low |
| F-SOC-05 | System shall display trending topics | Low |

### 4.8 AI Tools (F-AI)

| ID | Requirement | Priority |
|----|-------------|----------|
| F-AI-01 | System shall analyze resumes and provide feedback | Medium |
| F-AI-02 | System shall provide career counseling responses | Medium |
| F-AI-03 | System shall generate interview preparation questions | Medium |
| F-AI-04 | System shall identify skill gaps for target roles | Medium |
| F-AI-05 | System shall maintain AI tool usage history | Low |

---

## 5. NON-FUNCTIONAL REQUIREMENTS

### 5.1 Performance (NF-PERF)

| ID | Requirement | Metric |
|----|-------------|--------|
| NF-PERF-01 | Page load time shall be under 3 seconds | < 3s |
| NF-PERF-02 | API response time shall be under 500ms | < 500ms |
| NF-PERF-03 | System shall support 1000+ concurrent users | 1000+ |
| NF-PERF-04 | Database queries shall be optimized with indexes | N/A |
| NF-PERF-05 | Real-time messages shall be delivered within 1 second | < 1s |

### 5.2 Security (NF-SEC)

| ID | Requirement | Implementation |
|----|-------------|----------------|
| NF-SEC-01 | Passwords shall be hashed using Bcrypt | Bcrypt algorithm |
| NF-SEC-02 | JWT tokens shall expire after 1 hour | 3600 seconds |
| NF-SEC-03 | Refresh tokens shall expire after 30 days | 2592000 seconds |
| NF-SEC-04 | All API endpoints shall use HTTPS in production | SSL/TLS |
| NF-SEC-05 | Input validation shall prevent SQL injection | SQLAlchemy ORM |
| NF-SEC-06 | CORS shall be configured to allow specific origins | Flask-CORS |
| NF-SEC-07 | File uploads shall be validated and sanitized | File validators |
| NF-SEC-08 | Sensitive data shall not be logged | Log filtering |

### 5.3 Scalability (NF-SCAL)

| ID | Requirement | Approach |
|----|-------------|----------|
| NF-SCAL-01 | System shall handle growing user base | Horizontal scaling |
| NF-SCAL-02 | Database shall support sharding | PostgreSQL partitioning |
| NF-SCAL-03 | Static files shall be cached | Redis caching |
| NF-SCAL-04 | Load balancing shall distribute traffic | Reverse proxy |

### 5.4 Reliability (NF-REL)

| ID | Requirement | Target |
|----|-------------|--------|
| NF-REL-01 | System uptime shall be 99.5% or higher | 99.5% |
| NF-REL-02 | Data backups shall occur daily | Daily |
| NF-REL-03 | System shall support soft deletes | Implemented |
| NF-REL-04 | Failed transactions shall be rolled back | Database transactions |

### 5.5 Usability (NF-USE)

| ID | Requirement | Description |
|----|-------------|-------------|
| NF-USE-01 | UI shall be responsive across devices | Mobile-first design |
| NF-USE-02 | Interface shall be intuitive and user-friendly | Modern UI/UX |
| NF-USE-03 | Error messages shall be clear and actionable | User-friendly errors |
| NF-USE-04 | Loading states shall be indicated | Spinners/skeletons |

### 5.6 Maintainability (NF-MAIN)

| ID | Requirement | Implementation |
|----|-------------|----------------|
| NF-MAIN-01 | Code shall follow consistent style guidelines | ESLint, Prettier |
| NF-MAIN-02 | Code shall be modular and reusable | Service layer pattern |
| NF-MAIN-03 | Documentation shall be comprehensive | README files |
| NF-MAIN-04 | Database migrations shall be versioned | Flask-Migrate |

### 5.7 Compatibility (NF-COMP)

| ID | Requirement | Support |
|----|-------------|---------|
| NF-COMP-01 | System shall support modern browsers | Chrome, Firefox, Safari, Edge |
| NF-COMP-02 | API shall follow RESTful conventions | REST API |
| NF-COMP-03 | WebSockets shall fallback to polling | Socket.IO |

---

## 6. ENTITY-RELATIONSHIP (ER) DIAGRAM

### 6.1 Main Entities

The Collabio database consists of **30+ tables** organized into the following entity groups:

#### **Core Entities**
1. **User** - Base authentication entity
2. **StudentProfile** - Student-specific information
3. **EmployerProfile** - Employer/company information
4. **MentorProfile** - Mentor professional details

#### **Profile Extension Entities**
5. **StudentEducation** - Educational history
6. **StudentExperience** - Work experience
7. **StudentSkill** - Skills and proficiencies
8. **MentorExpertise** - Mentor areas of expertise

#### **Job-Related Entities**
9. **Job** - Job listings
10. **JobSkillRequired** - Skills required for jobs
11. **JobApplication** - Application submissions
12. **SavedJob** - Bookmarked jobs

#### **Mentorship Entities**
13. **MentorshipRequest** - Mentorship connection requests
14. **MentorshipSession** - Scheduled mentorship sessions
15. **MentorshipReview** - Feedback and ratings

#### **Messaging Entities**
16. **Conversation** - Chat containers
17. **ConversationParticipant** - Conversation members
18. **Message** - Individual messages
19. **WebSocketSession** - Active connections

#### **Learning Entities**
20. **Course** - Course catalog
21. **CourseLesson** - Individual lessons
22. **CourseEnrollment** - Student enrollments

#### **Social Entities**
23. **Post** - Social feed posts
24. **PostLike** - Post reactions
25. **PostComment** - Post discussions
26. **Connection** - User connections

#### **Supporting Entities**
27. **Notification** - System notifications
28. **FileUpload** - File metadata
29. **Achievement** - User achievements
30. **UserAchievement** - Achievement assignments
31. **AIToolUsage** - AI tool interaction history

### 6.2 ER Diagram Representation

```
┌─────────────────┐         ┌──────────────────┐         ┌─────────────────┐
│     USER        │         │ STUDENT_PROFILE  │         │ EMPLOYER_PROFILE│
├─────────────────┤         ├──────────────────┤         ├─────────────────┤
│ user_id (PK)    │────────<│ student_id (PK)  │         │ employer_id (PK)│
│ email           │         │ user_id (FK)     │         │ user_id (FK)    │
│ password_hash   │         │ full_name        │         │ company_name    │
│ user_type       │         │ bio              │         │ industry        │
│ created_at      │         │ location         │         │ description     │
└─────────────────┘         └──────────────────┘         └─────────────────┘
        │                            │                             │
        │                            │                             │
        └────────────────┬───────────┘                             │
                         │                                         │
                         ▼                                         │
              ┌──────────────────┐                                │
              │  MENTOR_PROFILE  │                                │
              ├──────────────────┤                                │
              │ mentor_id (PK)   │                                │
              │ user_id (FK)     │                                │
              │ current_role     │                                │
              │ years_experience │                                │
              │ rating           │                                │
              │ total_sessions   │                                │
              └──────────────────┘                                │
                       │                                           │
                       │ 1:N                                       │
                       ▼                                           │
            ┌──────────────────┐                                  │
            │ MENTOR_EXPERTISE │                                  │
            ├──────────────────┤                                  │
            │ expertise_id(PK) │                                  │
            │ mentor_id (FK)   │                                  │
            │ skill_name       │                                  │
            └──────────────────┘                                  │
                                                                   │
┌──────────────────┐      ┌──────────────────┐                   │
│STUDENT_EDUCATION │      │STUDENT_EXPERIENCE│                   │
├──────────────────┤      ├──────────────────┤                   │
│ education_id(PK) │      │ experience_id(PK)│                   │
│ student_id (FK)  │      │ student_id (FK)  │                   │
│ institution      │      │ company_name     │                   │
│ degree           │      │ job_title        │                   │
│ field_of_study   │      │ start_date       │                   │
│ start_date       │      │ end_date         │                   │
│ end_date         │      │ description      │                   │
└──────────────────┘      └──────────────────┘                   │
                                                                   │
                                                                   ▼
                          ┌──────────────────┐         ┌──────────────────┐
                          │       JOB        │         │  JOB_APPLICATION │
                          ├──────────────────┤         ├──────────────────┤
                          │ job_id (PK)      │────────<│ application_id   │
                          │ employer_id (FK) │────┐    │ job_id (FK)      │
                          │ title            │    │    │ student_id (FK)  │
                          │ description      │    │    │ status           │
                          │ job_type         │    │    │ applied_at       │
                          │ location         │    │    │ cover_letter     │
                          │ salary_range     │    │    └──────────────────┘
                          │ status           │    │
                          └──────────────────┘    │
                                   │              │
                                   │ 1:N          └──────┐
                                   ▼                     │
                          ┌──────────────────┐           │
                          │JOB_SKILL_REQUIRED│           │
                          ├──────────────────┤           │
                          │ skill_req_id(PK) │           │
                          │ job_id (FK)      │           │
                          │ skill_name       │           │
                          │ proficiency_level│           │
                          └──────────────────┘           │
                                                          │
┌──────────────────┐                                     │
│ CONVERSATION     │      ┌──────────────────┐          │
├──────────────────┤      │ CONV_PARTICIPANT │          │
│conversation_id PK│─────<│ participant_id PK│          │
│ created_at       │      │ conversation_id  │          │
│ updated_at       │      │ user_id (FK)     │          │
└──────────────────┘      └──────────────────┘          │
         │                                               │
         │ 1:N                                           │
         ▼                                               │
┌──────────────────┐                                     │
│    MESSAGE       │                                     │
├──────────────────┤                                     │
│ message_id (PK)  │                                     │
│ conversation_id  │                                     │
│ sender_id (FK)   │                                     │
│ message_text     │                                     │
│ sent_at          │                                     │
│ is_read          │                                     │
└──────────────────┘                                     │
                                                          │
┌──────────────────┐      ┌──────────────────┐          │
│    COURSE        │      │COURSE_ENROLLMENT │          │
├──────────────────┤      ├──────────────────┤          │
│ course_id (PK)   │─────<│ enrollment_id PK │          │
│ title            │      │ course_id (FK)   │          │
│ description      │      │ student_id (FK)  │          │
│ instructor_id    │      │ enrolled_at      │          │
│ category         │      │ progress         │          │
│ duration         │      │ completed_at     │          │
└──────────────────┘      └──────────────────┘          │
         │                                               │
         │ 1:N                                           │
         ▼                                               │
┌──────────────────┐                                     │
│  COURSE_LESSON   │                                     │
├──────────────────┤                                     │
│ lesson_id (PK)   │                                     │
│ course_id (FK)   │                                     │
│ title            │                                     │
│ content_url      │                                     │
│ order_num        │                                     │
└──────────────────┘                                     │
                                                          │
┌──────────────────┐      ┌──────────────────┐          │
│MENTORSHIP_REQUEST│      │MENTORSHIP_SESSION│          │
├──────────────────┤      ├──────────────────┤          │
│ request_id (PK)  │      │ session_id (PK)  │          │
│ student_id (FK)  │      │ request_id (FK)  │          │
│ mentor_id (FK)   │      │ scheduled_at     │          │
│ status           │      │ duration         │          │
│ message          │      │ meeting_link     │          │
│ requested_at     │      │ status           │          │
└──────────────────┘      └──────────────────┘          │
                                   │                     │
                                   │ 1:1                 │
                                   ▼                     │
                          ┌──────────────────┐           │
                          │MENTORSHIP_REVIEW │           │
                          ├──────────────────┤           │
                          │ review_id (PK)   │           │
                          │ session_id (FK)  │           │
                          │ rating           │           │
                          │ review_text      │           │
                          │ created_at       │           │
                          └──────────────────┘           │
                                                          │
┌──────────────────┐      ┌──────────────────┐          │
│      POST        │      │   POST_LIKE      │          │
├──────────────────┤      ├──────────────────┤          │
│ post_id (PK)     │─────<│ like_id (PK)     │          │
│ author_id (FK)   │      │ post_id (FK)     │          │
│ content          │      │ user_id (FK)     │          │
│ created_at       │      │ created_at       │          │
│ likes_count      │      └──────────────────┘          │
│ comments_count   │                                     │
└──────────────────┘      ┌──────────────────┐          │
         │                │  POST_COMMENT    │          │
         │                ├──────────────────┤          │
         └───────────────<│ comment_id (PK)  │          │
                          │ post_id (FK)     │          │
                          │ user_id (FK)     │          │
                          │ comment_text     │          │
                          │ created_at       │          │
                          └──────────────────┘          │
```

### 6.3 Key Relationships

| Relationship | Cardinality | Description |
|--------------|-------------|-------------|
| User → StudentProfile | 1:1 | One user can have one student profile |
| User → EmployerProfile | 1:1 | One user can have one employer profile |
| User → MentorProfile | 1:1 | One user can have one mentor profile |
| StudentProfile → Education | 1:N | Student can have multiple education entries |
| StudentProfile → Experience | 1:N | Student can have multiple experiences |
| StudentProfile → Skills | 1:N | Student can have multiple skills |
| EmployerProfile → Jobs | 1:N | Employer can post multiple jobs |
| Job → Applications | 1:N | Job can have multiple applications |
| Job → SkillsRequired | 1:N | Job can require multiple skills |
| MentorProfile → MentorshipRequests | 1:N | Mentor can receive multiple requests |
| StudentProfile → MentorshipRequests | 1:N | Student can send multiple requests |
| MentorshipRequest → Sessions | 1:N | Request can have multiple sessions |
| Session → Review | 1:1 | Each session can have one review |
| Conversation → Participants | 1:N | Conversation has multiple participants |
| Conversation → Messages | 1:N | Conversation contains multiple messages |
| Course → Lessons | 1:N | Course contains multiple lessons |
| Course → Enrollments | 1:N | Course can have multiple enrollments |
| Post → Likes | 1:N | Post can have multiple likes |
| Post → Comments | 1:N | Post can have multiple comments |

---

## 7. NORMALIZED SCHEMA

### 7.1 Normalization Level

The Collabio database schema is normalized to **Third Normal Form (3NF)**, ensuring:
- **1NF**: All attributes contain atomic values
- **2NF**: No partial dependencies on composite keys
- **3NF**: No transitive dependencies

### 7.2 Database Tables (Normalized)

#### **7.2.1 User Authentication**

```sql
-- USERS Table (Primary authentication table)
CREATE TABLE users (
    user_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    user_type VARCHAR(20) NOT NULL CHECK (user_type IN ('student', 'employer', 'mentor')),
    is_active BOOLEAN DEFAULT TRUE,
    is_verified BOOLEAN DEFAULT FALSE,
    last_login TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP
);

-- Indexes for performance
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_type ON users(user_type);
CREATE INDEX idx_users_active ON users(is_active) WHERE deleted_at IS NULL;
```

#### **7.2.2 Student Profile Tables**

```sql
-- STUDENT_PROFILES Table
CREATE TABLE student_profiles (
    student_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID UNIQUE NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    full_name VARCHAR(255) NOT NULL,
    bio TEXT,
    phone VARCHAR(20),
    location VARCHAR(255),
    date_of_birth DATE,
    profile_picture VARCHAR(500),
    resume_url VARCHAR(500),
    linkedin_url VARCHAR(500),
    github_url VARCHAR(500),
    portfolio_url VARCHAR(500),
    connections_count INTEGER DEFAULT 0,
    applications_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP
);

-- STUDENT_EDUCATION Table (1:N with student_profiles)
CREATE TABLE student_education (
    education_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id UUID NOT NULL REFERENCES student_profiles(student_id) ON DELETE CASCADE,
    institution_name VARCHAR(255) NOT NULL,
    degree VARCHAR(100),
    field_of_study VARCHAR(100),
    start_date DATE,
    end_date DATE,
    grade VARCHAR(50),
    description TEXT,
    is_current BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP
);

-- STUDENT_EXPERIENCE Table (1:N with student_profiles)
CREATE TABLE student_experience (
    experience_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id UUID NOT NULL REFERENCES student_profiles(student_id) ON DELETE CASCADE,
    company_name VARCHAR(255) NOT NULL,
    job_title VARCHAR(255) NOT NULL,
    employment_type VARCHAR(50),
    location VARCHAR(255),
    start_date DATE NOT NULL,
    end_date DATE,
    is_current BOOLEAN DEFAULT FALSE,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP
);

-- STUDENT_SKILLS Table (1:N with student_profiles)
CREATE TABLE student_skills (
    skill_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id UUID NOT NULL REFERENCES student_profiles(student_id) ON DELETE CASCADE,
    skill_name VARCHAR(100) NOT NULL,
    proficiency_level VARCHAR(50) CHECK (proficiency_level IN ('Beginner', 'Intermediate', 'Advanced', 'Expert')),
    years_of_experience INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP,
    UNIQUE(student_id, skill_name)
);

CREATE INDEX idx_student_education_student ON student_education(student_id);
CREATE INDEX idx_student_experience_student ON student_experience(student_id);
CREATE INDEX idx_student_skills_student ON student_skills(student_id);
CREATE INDEX idx_student_skills_name ON student_skills(skill_name);
```

#### **7.2.3 Employer Profile Tables**

```sql
-- EMPLOYER_PROFILES Table
CREATE TABLE employer_profiles (
    employer_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID UNIQUE NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    company_name VARCHAR(255) NOT NULL,
    industry VARCHAR(100),
    company_size VARCHAR(50),
    website VARCHAR(500),
    description TEXT,
    logo_url VARCHAR(500),
    location VARCHAR(255),
    founded_year INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP
);

CREATE INDEX idx_employer_company ON employer_profiles(company_name);
CREATE INDEX idx_employer_industry ON employer_profiles(industry);
```

#### **7.2.4 Mentor Profile Tables**

```sql
-- MENTOR_PROFILES Table
CREATE TABLE mentor_profiles (
    mentor_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID UNIQUE NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    full_name VARCHAR(255) NOT NULL,
    current_role VARCHAR(255),
    current_company VARCHAR(255),
    bio TEXT,
    profile_picture VARCHAR(500),
    linkedin_url VARCHAR(500),
    years_of_experience INTEGER,
    rating DECIMAL(3,2) DEFAULT 0.0,
    total_sessions INTEGER DEFAULT 0,
    total_reviews INTEGER DEFAULT 0,
    hourly_rate DECIMAL(10,2),
    is_available BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP
);

-- MENTOR_EXPERTISE Table (1:N with mentor_profiles)
CREATE TABLE mentor_expertise (
    expertise_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    mentor_id UUID NOT NULL REFERENCES mentor_profiles(mentor_id) ON DELETE CASCADE,
    skill_name VARCHAR(100) NOT NULL,
    years_of_experience INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP,
    UNIQUE(mentor_id, skill_name)
);

CREATE INDEX idx_mentor_expertise_mentor ON mentor_expertise(mentor_id);
CREATE INDEX idx_mentor_expertise_skill ON mentor_expertise(skill_name);
CREATE INDEX idx_mentor_rating ON mentor_profiles(rating);
```

#### **7.2.5 Job Tables**

```sql
-- JOBS Table
CREATE TABLE jobs (
    job_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    employer_id UUID NOT NULL REFERENCES employer_profiles(employer_id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    requirements TEXT,
    responsibilities TEXT,
    job_type VARCHAR(50) CHECK (job_type IN ('Full-time', 'Part-time', 'Internship', 'Contract', 'Freelance')),
    experience_level VARCHAR(50) CHECK (experience_level IN ('Entry', 'Mid', 'Senior', 'Lead')),
    location VARCHAR(255),
    is_remote BOOLEAN DEFAULT FALSE,
    salary_min DECIMAL(10,2),
    salary_max DECIMAL(10,2),
    salary_currency VARCHAR(10) DEFAULT 'USD',
    application_deadline DATE,
    status VARCHAR(50) DEFAULT 'active' CHECK (status IN ('draft', 'active', 'closed', 'filled')),
    views_count INTEGER DEFAULT 0,
    applications_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP
);

-- JOB_SKILLS_REQUIRED Table (1:N with jobs)
CREATE TABLE job_skills_required (
    skill_requirement_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    job_id UUID NOT NULL REFERENCES jobs(job_id) ON DELETE CASCADE,
    skill_name VARCHAR(100) NOT NULL,
    proficiency_level VARCHAR(50),
    is_required BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP
);

-- JOB_APPLICATIONS Table (M:N between jobs and students)
CREATE TABLE job_applications (
    application_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    job_id UUID NOT NULL REFERENCES jobs(job_id) ON DELETE CASCADE,
    student_id UUID NOT NULL REFERENCES student_profiles(student_id) ON DELETE CASCADE,
    status VARCHAR(50) DEFAULT 'pending' CHECK (status IN ('pending', 'reviewing', 'shortlisted', 'rejected', 'accepted')),
    cover_letter TEXT,
    resume_url VARCHAR(500),
    match_score DECIMAL(5,2),
    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP,
    UNIQUE(job_id, student_id)
);

-- SAVED_JOBS Table (M:N between jobs and students)
CREATE TABLE saved_jobs (
    saved_job_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id UUID NOT NULL REFERENCES student_profiles(student_id) ON DELETE CASCADE,
    job_id UUID NOT NULL REFERENCES jobs(job_id) ON DELETE CASCADE,
    saved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP,
    UNIQUE(student_id, job_id)
);

CREATE INDEX idx_jobs_employer ON jobs(employer_id);
CREATE INDEX idx_jobs_status ON jobs(status) WHERE deleted_at IS NULL;
CREATE INDEX idx_jobs_type ON jobs(job_type);
CREATE INDEX idx_job_skills_job ON job_skills_required(job_id);
CREATE INDEX idx_applications_job ON job_applications(job_id);
CREATE INDEX idx_applications_student ON job_applications(student_id);
CREATE INDEX idx_applications_status ON job_applications(status);
```

#### **7.2.6 Mentorship Tables**

```sql
-- MENTORSHIP_REQUESTS Table
CREATE TABLE mentorship_requests (
    request_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id UUID NOT NULL REFERENCES student_profiles(student_id) ON DELETE CASCADE,
    mentor_id UUID NOT NULL REFERENCES mentor_profiles(mentor_id) ON DELETE CASCADE,
    status VARCHAR(50) DEFAULT 'pending' CHECK (status IN ('pending', 'accepted', 'declined', 'cancelled')),
    message TEXT,
    match_score DECIMAL(5,2),
    requested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    responded_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP
);

-- MENTORSHIP_SESSIONS Table (1:N with mentorship_requests)
CREATE TABLE mentorship_sessions (
    session_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    request_id UUID NOT NULL REFERENCES mentorship_requests(request_id) ON DELETE CASCADE,
    scheduled_at TIMESTAMP NOT NULL,
    duration_minutes INTEGER DEFAULT 60,
    meeting_link VARCHAR(500),
    agenda TEXT,
    notes TEXT,
    status VARCHAR(50) DEFAULT 'scheduled' CHECK (status IN ('scheduled', 'completed', 'cancelled', 'no-show')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP
);

-- MENTORSHIP_REVIEWS Table (1:1 with mentorship_sessions)
CREATE TABLE mentorship_reviews (
    review_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID UNIQUE NOT NULL REFERENCES mentorship_sessions(session_id) ON DELETE CASCADE,
    mentor_id UUID NOT NULL REFERENCES mentor_profiles(mentor_id) ON DELETE CASCADE,
    student_id UUID NOT NULL REFERENCES student_profiles(student_id) ON DELETE CASCADE,
    rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
    review_text TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP
);

CREATE INDEX idx_mentorship_requests_student ON mentorship_requests(student_id);
CREATE INDEX idx_mentorship_requests_mentor ON mentorship_requests(mentor_id);
CREATE INDEX idx_mentorship_sessions_request ON mentorship_sessions(request_id);
CREATE INDEX idx_mentorship_reviews_session ON mentorship_reviews(session_id);
```

#### **7.2.7 Messaging Tables**

```sql
-- CONVERSATIONS Table
CREATE TABLE conversations (
    conversation_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP
);

-- CONVERSATION_PARTICIPANTS Table (M:N between users and conversations)
CREATE TABLE conversation_participants (
    participant_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID NOT NULL REFERENCES conversations(conversation_id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_read_at TIMESTAMP,
    deleted_at TIMESTAMP,
    UNIQUE(conversation_id, user_id)
);

-- MESSAGES Table (1:N with conversations)
CREATE TABLE messages (
    message_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID NOT NULL REFERENCES conversations(conversation_id) ON DELETE CASCADE,
    sender_id UUID NOT NULL REFERENCES users(user_id) ON DELETE SET NULL,
    message_text TEXT NOT NULL,
    attachment_url VARCHAR(500),
    is_read BOOLEAN DEFAULT FALSE,
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP
);

-- WEBSOCKET_SESSIONS Table (Active connections)
CREATE TABLE websocket_sessions (
    session_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    socket_id VARCHAR(255) NOT NULL,
    connected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_ping TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    disconnected_at TIMESTAMP
);

CREATE INDEX idx_conversation_participants_conv ON conversation_participants(conversation_id);
CREATE INDEX idx_conversation_participants_user ON conversation_participants(user_id);
CREATE INDEX idx_messages_conversation ON messages(conversation_id);
CREATE INDEX idx_messages_sender ON messages(sender_id);
CREATE INDEX idx_messages_sent_at ON messages(sent_at);
```

#### **7.2.8 Course Tables**

```sql
-- COURSES Table
CREATE TABLE courses (
    course_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    instructor_id UUID REFERENCES users(user_id) ON DELETE SET NULL,
    category VARCHAR(100),
    difficulty_level VARCHAR(50) CHECK (difficulty_level IN ('Beginner', 'Intermediate', 'Advanced')),
    duration_hours INTEGER,
    thumbnail_url VARCHAR(500),
    price DECIMAL(10,2) DEFAULT 0.00,
    is_published BOOLEAN DEFAULT FALSE,
    enrollments_count INTEGER DEFAULT 0,
    average_rating DECIMAL(3,2) DEFAULT 0.0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP
);

-- COURSE_LESSONS Table (1:N with courses)
CREATE TABLE course_lessons (
    lesson_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    course_id UUID NOT NULL REFERENCES courses(course_id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    content_type VARCHAR(50) CHECK (content_type IN ('video', 'article', 'quiz', 'assignment')),
    content_url VARCHAR(500),
    duration_minutes INTEGER,
    order_number INTEGER NOT NULL,
    is_preview BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP
);

-- COURSE_ENROLLMENTS Table (M:N between courses and students)
CREATE TABLE course_enrollments (
    enrollment_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    course_id UUID NOT NULL REFERENCES courses(course_id) ON DELETE CASCADE,
    student_id UUID NOT NULL REFERENCES student_profiles(student_id) ON DELETE CASCADE,
    progress_percentage DECIMAL(5,2) DEFAULT 0.0,
    completed_lessons INTEGER DEFAULT 0,
    total_lessons INTEGER,
    enrolled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    last_accessed_at TIMESTAMP,
    deleted_at TIMESTAMP,
    UNIQUE(course_id, student_id)
);

CREATE INDEX idx_courses_category ON courses(category);
CREATE INDEX idx_courses_published ON courses(is_published) WHERE deleted_at IS NULL;
CREATE INDEX idx_course_lessons_course ON course_lessons(course_id);
CREATE INDEX idx_course_enrollments_course ON course_enrollments(course_id);
CREATE INDEX idx_course_enrollments_student ON course_enrollments(student_id);
```

#### **7.2.9 Social Feed Tables**

```sql
-- POSTS Table
CREATE TABLE posts (
    post_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    author_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    media_url VARCHAR(500),
    media_type VARCHAR(50),
    visibility VARCHAR(50) DEFAULT 'public' CHECK (visibility IN ('public', 'connections', 'private')),
    likes_count INTEGER DEFAULT 0,
    comments_count INTEGER DEFAULT 0,
    shares_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP
);

-- POST_LIKES Table (M:N between posts and users)
CREATE TABLE post_likes (
    like_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    post_id UUID NOT NULL REFERENCES posts(post_id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP,
    UNIQUE(post_id, user_id)
);

-- POST_COMMENTS Table (1:N with posts)
CREATE TABLE post_comments (
    comment_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    post_id UUID NOT NULL REFERENCES posts(post_id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    comment_text TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP
);

-- CONNECTIONS Table (M:N self-referencing users)
CREATE TABLE connections (
    connection_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    connected_user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    status VARCHAR(50) DEFAULT 'pending' CHECK (status IN ('pending', 'accepted', 'declined', 'blocked')),
    requested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    responded_at TIMESTAMP,
    deleted_at TIMESTAMP,
    UNIQUE(user_id, connected_user_id)
);

CREATE INDEX idx_posts_author ON posts(author_id);
CREATE INDEX idx_posts_created ON posts(created_at);
CREATE INDEX idx_post_likes_post ON post_likes(post_id);
CREATE INDEX idx_post_likes_user ON post_likes(user_id);
CREATE INDEX idx_post_comments_post ON post_comments(post_id);
CREATE INDEX idx_connections_user ON connections(user_id);
```

#### **7.2.10 Supporting Tables**

```sql
-- NOTIFICATIONS Table
CREATE TABLE notifications (
    notification_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    type VARCHAR(50) NOT NULL,
    title VARCHAR(255) NOT NULL,
    message TEXT,
    related_entity_type VARCHAR(50),
    related_entity_id UUID,
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    read_at TIMESTAMP,
    deleted_at TIMESTAMP
);

-- FILE_UPLOADS Table
CREATE TABLE file_uploads (
    file_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    uploader_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    file_name VARCHAR(255) NOT NULL,
    file_type VARCHAR(100),
    file_size BIGINT,
    file_url VARCHAR(500) NOT NULL,
    storage_path VARCHAR(500),
    entity_type VARCHAR(50),
    entity_id UUID,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP
);

-- ACHIEVEMENTS Table
CREATE TABLE achievements (
    achievement_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    icon_url VARCHAR(500),
    points INTEGER DEFAULT 0,
    category VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- USER_ACHIEVEMENTS Table (M:N between users and achievements)
CREATE TABLE user_achievements (
    user_achievement_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    achievement_id UUID NOT NULL REFERENCES achievements(achievement_id) ON DELETE CASCADE,
    earned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, achievement_id)
);

-- AI_TOOL_USAGE Table
CREATE TABLE ai_tool_usage (
    usage_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    tool_name VARCHAR(100) NOT NULL,
    input_data JSONB,
    output_data JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_notifications_user ON notifications(user_id);
CREATE INDEX idx_notifications_read ON notifications(is_read);
CREATE INDEX idx_file_uploads_uploader ON file_uploads(uploader_id);
CREATE INDEX idx_user_achievements_user ON user_achievements(user_id);
CREATE INDEX idx_ai_tool_usage_user ON ai_tool_usage(user_id);
```

### 7.3 Triggers and Functions

```sql
-- Auto-update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply to all tables with updated_at
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_student_profiles_updated_at BEFORE UPDATE ON student_profiles
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Add similar triggers for all tables with updated_at

-- Auto-update post likes count
CREATE OR REPLACE FUNCTION update_post_likes_count()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        UPDATE posts SET likes_count = likes_count + 1 WHERE post_id = NEW.post_id;
    ELSIF TG_OP = 'DELETE' THEN
        UPDATE posts SET likes_count = likes_count - 1 WHERE post_id = OLD.post_id;
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER post_likes_count_trigger
AFTER INSERT OR DELETE ON post_likes
FOR EACH ROW EXECUTE FUNCTION update_post_likes_count();

-- Auto-update post comments count
CREATE OR REPLACE FUNCTION update_post_comments_count()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        UPDATE posts SET comments_count = comments_count + 1 WHERE post_id = NEW.post_id;
    ELSIF TG_OP = 'DELETE' THEN
        UPDATE posts SET comments_count = comments_count - 1 WHERE post_id = OLD.post_id;
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER post_comments_count_trigger
AFTER INSERT OR DELETE ON post_comments
FOR EACH ROW EXECUTE FUNCTION update_post_comments_count();

-- Auto-update mentor rating
CREATE OR REPLACE FUNCTION update_mentor_rating()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE mentor_profiles mp
    SET rating = (
        SELECT AVG(rating)::DECIMAL(3,2)
        FROM mentorship_reviews
        WHERE mentor_id = NEW.mentor_id AND deleted_at IS NULL
    ),
    total_reviews = (
        SELECT COUNT(*)
        FROM mentorship_reviews
        WHERE mentor_id = NEW.mentor_id AND deleted_at IS NULL
    )
    WHERE mp.mentor_id = NEW.mentor_id;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER mentor_rating_trigger
AFTER INSERT OR UPDATE ON mentorship_reviews
FOR EACH ROW EXECUTE FUNCTION update_mentor_rating();
```

### 7.4 Normalization Analysis

#### **First Normal Form (1NF)**
- ✅ All tables have atomic (indivisible) columns
- ✅ Each column contains values of a single type
- ✅ Each column has a unique name
- ✅ Primary keys are defined for all tables

#### **Second Normal Form (2NF)**
- ✅ All tables are in 1NF
- ✅ All non-key attributes are fully functionally dependent on the primary key
- ✅ No partial dependencies exist (all tables use single-column primary keys or proper composite keys)

**Example**: In `student_education`, all attributes (institution_name, degree, field_of_study) depend fully on `education_id`, not on any subset of a composite key.

#### **Third Normal Form (3NF)**
- ✅ All tables are in 2NF
- ✅ No transitive dependencies exist
- ✅ All non-key attributes depend only on the primary key

**Example**: User-specific data (email, password) is in the `users` table, while role-specific data (student details, employer details) is in separate tables (`student_profiles`, `employer_profiles`), eliminating transitive dependencies.

### 7.5 Denormalization Decisions

Some controlled denormalization was applied for performance optimization:

| Table | Denormalized Column | Reason | Trade-off |
|-------|---------------------|--------|-----------|
| posts | likes_count, comments_count | Avoid expensive COUNT queries | Updated via triggers |
| mentor_profiles | rating, total_sessions, total_reviews | Fast mentor listing | Updated via triggers |
| student_profiles | connections_count, applications_count | Dashboard performance | Updated via application logic |
| jobs | applications_count, views_count | Quick job statistics | Updated via application logic |
| course_enrollments | total_lessons | Progress calculation | Cached from course |

**Justification**: These denormalizations significantly improve read performance (critical for user-facing dashboards) while maintaining data consistency through database triggers and application-level updates.

---

## 8. CONCLUSION

### 8.1 Project Achievements

The Collabio project successfully demonstrates the application of database concepts learned throughout the course:

1. **Comprehensive Database Design**
   - Designed and implemented 30+ normalized tables
   - Applied normalization principles (3NF) effectively
   - Created complex relationships (1:1, 1:N, M:N)
   - Implemented soft-delete architecture for data retention

2. **Advanced SQL Features**
   - Utilized PostgreSQL-specific features (UUID, JSONB)
   - Implemented database triggers for automated updates
   - Created indexes for query optimization
   - Used foreign keys with appropriate cascade rules

3. **Full-Stack Integration**
   - Seamlessly integrated PostgreSQL with Flask backend
   - Used SQLAlchemy ORM for database operations
   - Implemented real-time features with WebSockets
   - Applied security best practices (JWT, password hashing)

4. **Scalable Architecture**
   - Designed for horizontal scalability
   - Implemented caching layer with Redis
   - Optimized queries with strategic indexing
   - Prepared for future enhancements

### 8.2 Learning Outcomes

Through this project, we gained practical experience in:

- **Database Design**: ER modeling, normalization, relationship mapping
- **SQL Proficiency**: Complex queries, joins, aggregations, subqueries
- **Performance Optimization**: Indexing strategies, query optimization
- **Data Integrity**: Constraints, triggers, cascading deletes
- **Application Integration**: ORM usage, transaction management
- **Real-World Problem Solving**: Addressing practical challenges in career platforms

### 8.3 Challenges Faced

1. **Complex Relationship Modeling**
   - Managing multiple user types (students, employers, mentors) with shared and distinct attributes
   - Solution: Used inheritance pattern with base `users` table and role-specific profile tables

2. **Performance Considerations**
   - Balancing normalization with query performance
   - Solution: Strategic denormalization with automated triggers for consistency

3. **Real-Time Features**
   - Implementing WebSocket-based messaging with database persistence
   - Solution: Combined Socket.IO for real-time delivery with PostgreSQL for message storage

4. **AI Matching Algorithm**
   - Calculating match scores efficiently for recommendations
   - Solution: Implemented scoring service that uses optimized database queries

### 8.4 Future Enhancements

Potential improvements for the platform:

1. **Technical Enhancements**
   - Implement database partitioning for large tables (messages, notifications)
   - Add full-text search using PostgreSQL FTS or Elasticsearch
   - Implement read replicas for improved read performance
   - Add comprehensive database backup and recovery procedures

2. **Feature Additions**
   - Video call integration for mentorship sessions
   - Advanced analytics dashboard with aggregated insights
   - Machine learning models for better job/mentor matching
   - Email notification system for important events
   - Mobile applications (iOS/Android)

3. **Business Features**
   - Payment integration for premium features
   - Employer subscription plans
   - Mentor monetization options
   - Course marketplace
   - Certification system

### 8.5 Conclusion Statement

Collabio successfully demonstrates a production-ready, database-driven web application that addresses real-world challenges in career development and job searching. The project showcases:

- **Strong foundation in database design principles**
- **Practical application of theoretical concepts**
- **Industry-standard development practices**
- **Scalable and maintainable architecture**

The platform is ready for deployment and can serve as a valuable tool for students seeking career opportunities, employers looking for talent, and mentors willing to guide the next generation of professionals.

---

## 9. REFERENCES

### 9.1 Technical Documentation

1. **PostgreSQL Official Documentation**
   - PostgreSQL 14 Documentation
   - URL: https://www.postgresql.org/docs/14/
   - Used for: Database design, SQL syntax, advanced features

2. **Flask Framework**
   - Flask Official Documentation
   - URL: https://flask.palletsprojects.com/
   - Used for: Web framework implementation

3. **SQLAlchemy**
   - SQLAlchemy ORM Documentation
   - URL: https://docs.sqlalchemy.org/
   - Used for: Database ORM, migrations

4. **React Documentation**
   - React Official Documentation
   - URL: https://react.dev/
   - Used for: Frontend development

5. **Socket.IO**
   - Socket.IO Documentation
   - URL: https://socket.io/docs/
   - Used for: Real-time WebSocket communication

### 9.2 Academic Resources

1. **Database System Concepts** by Silberschatz, Korth, and Sudarshan
   - Used for: Normalization theory, ER modeling

2. **Database Management Systems** by Raghu Ramakrishnan and Johannes Gehrke
   - Used for: Query optimization, indexing strategies

3. Course Lectures and Materials
   - Database Systems Course, Fall 2025
   - Instructor: [Instructor Name]

### 9.3 Online Resources

1. **PostgreSQL Tutorial**
   - URL: https://www.postgresqltutorial.com/
   - Used for: Advanced PostgreSQL features

2. **Database Design Best Practices**
   - Various articles on database normalization and design patterns

3. **Stack Overflow**
   - URL: https://stackoverflow.com/
   - Used for: Troubleshooting specific implementation challenges

### 9.4 Tools and Libraries

1. **Development Tools**
   - Visual Studio Code (Code Editor)
   - PostgreSQL 14 (Database)
   - pgAdmin 4 (Database Administration)
   - Postman (API Testing)

2. **Backend Libraries**
   - Flask 3.0, Flask-SQLAlchemy, Flask-JWT-Extended
   - Flask-SocketIO, Flask-CORS, Bcrypt
   - Python 3.10

3. **Frontend Libraries**
   - React 18.3, TypeScript 5.8, Vite 5.4
   - TailwindCSS, shadcn/ui, React Router
   - TanStack Query

---

## APPENDICES

### Appendix A: Installation Guide

Please refer to `README.md` for detailed setup instructions.

### Appendix B: API Documentation

Please refer to `backend/README.md` for complete API endpoint documentation.

### Appendix C: Source Code

- **GitHub Repository**: [Repository URL]
- **Live Demo**: [Demo URL if deployed]

---

<div align="center">

**End of Report**

---

**Project Report Generated:** November 26, 2025
**Platform:** Collabio - AI-Powered Career Platform
**Course:** Database Systems

</div>
