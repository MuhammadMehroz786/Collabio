-- Collabio Database Schema
-- PostgreSQL Migration File
-- Created: 2025-10-16

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- ============================================================================
-- 1. USERS & AUTHENTICATION
-- ============================================================================

CREATE TABLE users (
    user_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    user_type VARCHAR(20) NOT NULL CHECK (user_type IN ('student', 'employer', 'mentor')),
    is_verified BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    deleted_at TIMESTAMP NULL
);

CREATE INDEX idx_users_email ON users(email) WHERE deleted_at IS NULL;
CREATE INDEX idx_users_type ON users(user_type) WHERE deleted_at IS NULL;
CREATE INDEX idx_users_deleted ON users(deleted_at);

-- ============================================================================
-- 2. STUDENT PROFILES
-- ============================================================================

CREATE TABLE student_profiles (
    student_id UUID PRIMARY KEY REFERENCES users(user_id) ON DELETE CASCADE,
    full_name VARCHAR(255) NOT NULL,
    profile_picture VARCHAR(500),
    bio TEXT,
    location VARCHAR(255),
    phone_number VARCHAR(20),
    date_of_birth DATE,
    resume_url VARCHAR(500),
    portfolio_url VARCHAR(500),
    linkedin_url VARCHAR(500),
    github_url VARCHAR(500),
    joined_date DATE NOT NULL DEFAULT CURRENT_DATE,
    connections_count INT DEFAULT 0,
    applications_count INT DEFAULT 0,
    deleted_at TIMESTAMP NULL
);

CREATE INDEX idx_student_profiles_deleted ON student_profiles(deleted_at);

CREATE TABLE student_education (
    education_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id UUID REFERENCES student_profiles(student_id) ON DELETE CASCADE,
    institution_name VARCHAR(255) NOT NULL,
    degree VARCHAR(100) NOT NULL,
    field_of_study VARCHAR(100) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE,
    gpa DECIMAL(3,2),
    is_current BOOLEAN DEFAULT FALSE,
    deleted_at TIMESTAMP NULL
);

CREATE INDEX idx_education_student ON student_education(student_id) WHERE deleted_at IS NULL;

CREATE TABLE student_experience (
    experience_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id UUID REFERENCES student_profiles(student_id) ON DELETE CASCADE,
    company_name VARCHAR(255) NOT NULL,
    position VARCHAR(100) NOT NULL,
    location VARCHAR(255),
    start_date DATE NOT NULL,
    end_date DATE,
    description TEXT,
    is_current BOOLEAN DEFAULT FALSE,
    deleted_at TIMESTAMP NULL
);

CREATE INDEX idx_experience_student ON student_experience(student_id) WHERE deleted_at IS NULL;

CREATE TABLE student_skills (
    skill_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id UUID REFERENCES student_profiles(student_id) ON DELETE CASCADE,
    skill_name VARCHAR(100) NOT NULL,
    proficiency_level VARCHAR(20) CHECK (proficiency_level IN ('beginner', 'intermediate', 'advanced')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL
);

CREATE INDEX idx_skills_student ON student_skills(student_id) WHERE deleted_at IS NULL;
CREATE INDEX idx_skills_name ON student_skills(skill_name) WHERE deleted_at IS NULL;

-- ============================================================================
-- 3. EMPLOYER PROFILES
-- ============================================================================

CREATE TABLE employer_profiles (
    employer_id UUID PRIMARY KEY REFERENCES users(user_id) ON DELETE CASCADE,
    company_name VARCHAR(255) NOT NULL,
    company_logo VARCHAR(500),
    industry VARCHAR(100),
    company_size VARCHAR(20) CHECK (company_size IN ('startup', 'small', 'medium', 'large', 'enterprise')),
    website VARCHAR(500),
    description TEXT,
    location VARCHAR(255),
    founded_year INT,
    deleted_at TIMESTAMP NULL
);

CREATE INDEX idx_employer_profiles_deleted ON employer_profiles(deleted_at);

-- ============================================================================
-- 4. MENTOR PROFILES
-- ============================================================================

CREATE TABLE mentor_profiles (
    mentor_id UUID PRIMARY KEY REFERENCES users(user_id) ON DELETE CASCADE,
    full_name VARCHAR(255) NOT NULL,
    profile_picture VARCHAR(500),
    "current_role" VARCHAR(255) NOT NULL,
    "current_company" VARCHAR(255) NOT NULL,
    bio TEXT,
    years_of_experience INT,
    rating DECIMAL(3,2) DEFAULT 0.0 CHECK (rating >= 0 AND rating <= 5),
    total_sessions INT DEFAULT 0,
    linkedin_url VARCHAR(500),
    deleted_at TIMESTAMP NULL
);

CREATE INDEX idx_mentor_profiles_rating ON mentor_profiles(rating DESC) WHERE deleted_at IS NULL;

CREATE TABLE mentor_expertise (
    expertise_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    mentor_id UUID REFERENCES mentor_profiles(mentor_id) ON DELETE CASCADE,
    expertise_area VARCHAR(100) NOT NULL,
    deleted_at TIMESTAMP NULL
);

CREATE INDEX idx_mentor_expertise_mentor ON mentor_expertise(mentor_id) WHERE deleted_at IS NULL;

-- ============================================================================
-- 5. JOBS & APPLICATIONS
-- ============================================================================

CREATE TABLE jobs (
    job_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    employer_id UUID REFERENCES employer_profiles(employer_id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    company_name VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    location VARCHAR(255),
    job_type VARCHAR(20) NOT NULL CHECK (job_type IN ('internship', 'full-time', 'part-time', 'contract')),
    work_mode VARCHAR(20) CHECK (work_mode IN ('remote', 'hybrid', 'on-site')),
    salary_min DECIMAL(10,2),
    salary_max DECIMAL(10,2),
    salary_currency VARCHAR(3) DEFAULT 'USD',
    salary_period VARCHAR(20) CHECK (salary_period IN ('hourly', 'monthly', 'yearly')),
    requirements TEXT,
    posted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP,
    status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active', 'closed', 'draft')),
    views_count INT DEFAULT 0,
    deleted_at TIMESTAMP NULL
);

CREATE INDEX idx_jobs_employer ON jobs(employer_id) WHERE deleted_at IS NULL;
CREATE INDEX idx_jobs_status ON jobs(status) WHERE deleted_at IS NULL;
CREATE INDEX idx_jobs_posted ON jobs(posted_at DESC) WHERE deleted_at IS NULL;
CREATE INDEX idx_jobs_type ON jobs(job_type) WHERE deleted_at IS NULL;

CREATE TABLE job_skills_required (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    job_id UUID REFERENCES jobs(job_id) ON DELETE CASCADE,
    skill_name VARCHAR(100) NOT NULL,
    is_required BOOLEAN DEFAULT TRUE,
    deleted_at TIMESTAMP NULL
);

CREATE INDEX idx_job_skills_job ON job_skills_required(job_id) WHERE deleted_at IS NULL;

CREATE TABLE job_applications (
    application_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    job_id UUID REFERENCES jobs(job_id) ON DELETE CASCADE,
    student_id UUID REFERENCES student_profiles(student_id) ON DELETE CASCADE,
    cover_letter TEXT,
    resume_url VARCHAR(500),
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'reviewing', 'shortlisted', 'rejected', 'accepted')),
    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL,
    UNIQUE(job_id, student_id)
);

CREATE INDEX idx_applications_job ON job_applications(job_id) WHERE deleted_at IS NULL;
CREATE INDEX idx_applications_student ON job_applications(student_id) WHERE deleted_at IS NULL;
CREATE INDEX idx_applications_status ON job_applications(status) WHERE deleted_at IS NULL;

CREATE TABLE saved_jobs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id UUID REFERENCES student_profiles(student_id) ON DELETE CASCADE,
    job_id UUID REFERENCES jobs(job_id) ON DELETE CASCADE,
    saved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL,
    UNIQUE(student_id, job_id)
);

CREATE INDEX idx_saved_jobs_student ON saved_jobs(student_id) WHERE deleted_at IS NULL;

-- ============================================================================
-- 6. MENTORSHIP SYSTEM
-- ============================================================================

CREATE TABLE mentorship_requests (
    request_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id UUID REFERENCES student_profiles(student_id) ON DELETE CASCADE,
    mentor_id UUID REFERENCES mentor_profiles(mentor_id) ON DELETE CASCADE,
    message TEXT,
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'accepted', 'rejected', 'completed')),
    requested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    responded_at TIMESTAMP,
    deleted_at TIMESTAMP NULL
);

CREATE INDEX idx_mentorship_requests_student ON mentorship_requests(student_id) WHERE deleted_at IS NULL;
CREATE INDEX idx_mentorship_requests_mentor ON mentorship_requests(mentor_id) WHERE deleted_at IS NULL;
CREATE INDEX idx_mentorship_requests_status ON mentorship_requests(status) WHERE deleted_at IS NULL;

CREATE TABLE mentorship_sessions (
    session_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    request_id UUID REFERENCES mentorship_requests(request_id) ON DELETE CASCADE,
    student_id UUID REFERENCES student_profiles(student_id) ON DELETE CASCADE,
    mentor_id UUID REFERENCES mentor_profiles(mentor_id) ON DELETE CASCADE,
    scheduled_at TIMESTAMP NOT NULL,
    duration_minutes INT,
    meeting_link VARCHAR(500),
    notes TEXT,
    status VARCHAR(20) DEFAULT 'scheduled' CHECK (status IN ('scheduled', 'completed', 'cancelled')),
    completed_at TIMESTAMP,
    deleted_at TIMESTAMP NULL
);

CREATE INDEX idx_sessions_student ON mentorship_sessions(student_id) WHERE deleted_at IS NULL;
CREATE INDEX idx_sessions_mentor ON mentorship_sessions(mentor_id) WHERE deleted_at IS NULL;
CREATE INDEX idx_sessions_scheduled ON mentorship_sessions(scheduled_at) WHERE deleted_at IS NULL;

CREATE TABLE mentorship_reviews (
    review_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID REFERENCES mentorship_sessions(session_id) ON DELETE CASCADE,
    student_id UUID REFERENCES student_profiles(student_id) ON DELETE CASCADE,
    mentor_id UUID REFERENCES mentor_profiles(mentor_id) ON DELETE CASCADE,
    rating INT NOT NULL CHECK (rating >= 1 AND rating <= 5),
    review_text TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL,
    UNIQUE(session_id, student_id)
);

CREATE INDEX idx_reviews_mentor ON mentorship_reviews(mentor_id) WHERE deleted_at IS NULL;

-- ============================================================================
-- 7. MESSAGING SYSTEM (WebSocket-ready)
-- ============================================================================

CREATE TABLE conversations (
    conversation_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL
);

CREATE INDEX idx_conversations_updated ON conversations(updated_at DESC) WHERE deleted_at IS NULL;

CREATE TABLE conversation_participants (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID REFERENCES conversations(conversation_id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(user_id) ON DELETE CASCADE,
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_read_at TIMESTAMP,
    deleted_at TIMESTAMP NULL,
    UNIQUE(conversation_id, user_id)
);

CREATE INDEX idx_participants_conversation ON conversation_participants(conversation_id) WHERE deleted_at IS NULL;
CREATE INDEX idx_participants_user ON conversation_participants(user_id) WHERE deleted_at IS NULL;

CREATE TABLE messages (
    message_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID REFERENCES conversations(conversation_id) ON DELETE CASCADE,
    sender_id UUID REFERENCES users(user_id) ON DELETE CASCADE,
    message_text TEXT NOT NULL,
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_read BOOLEAN DEFAULT FALSE,
    attachment_url VARCHAR(500),
    deleted_at TIMESTAMP NULL
);

CREATE INDEX idx_messages_conversation ON messages(conversation_id, sent_at DESC) WHERE deleted_at IS NULL;
CREATE INDEX idx_messages_sender ON messages(sender_id) WHERE deleted_at IS NULL;
CREATE INDEX idx_messages_unread ON messages(is_read) WHERE deleted_at IS NULL AND is_read = FALSE;
CREATE INDEX idx_messages_unread_conversation ON messages(conversation_id, is_read) WHERE deleted_at IS NULL;

-- ============================================================================
-- 8. COURSES & LEARNING
-- ============================================================================

CREATE TABLE courses (
    course_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    category VARCHAR(100),
    difficulty_level VARCHAR(20) CHECK (difficulty_level IN ('beginner', 'intermediate', 'advanced')),
    duration_weeks INT,
    thumbnail_url VARCHAR(500),
    total_students INT DEFAULT 0,
    instructor_name VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL
);

CREATE INDEX idx_courses_category ON courses(category) WHERE deleted_at IS NULL;
CREATE INDEX idx_courses_difficulty ON courses(difficulty_level) WHERE deleted_at IS NULL;

CREATE TABLE course_lessons (
    lesson_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    course_id UUID REFERENCES courses(course_id) ON DELETE CASCADE,
    lesson_number INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    content TEXT,
    video_url VARCHAR(500),
    duration_minutes INT,
    deleted_at TIMESTAMP NULL
);

CREATE INDEX idx_lessons_course ON course_lessons(course_id, lesson_number) WHERE deleted_at IS NULL;

CREATE TABLE course_enrollments (
    enrollment_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id UUID REFERENCES student_profiles(student_id) ON DELETE CASCADE,
    course_id UUID REFERENCES courses(course_id) ON DELETE CASCADE,
    enrolled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    progress_percentage INT DEFAULT 0 CHECK (progress_percentage >= 0 AND progress_percentage <= 100),
    completed_lessons INT DEFAULT 0,
    completed_at TIMESTAMP,
    status VARCHAR(20) DEFAULT 'in_progress' CHECK (status IN ('in_progress', 'completed', 'dropped')),
    deleted_at TIMESTAMP NULL,
    UNIQUE(student_id, course_id)
);

CREATE INDEX idx_enrollments_student ON course_enrollments(student_id) WHERE deleted_at IS NULL;
CREATE INDEX idx_enrollments_course ON course_enrollments(course_id) WHERE deleted_at IS NULL;

-- ============================================================================
-- 9. AI TOOLS USAGE
-- ============================================================================

CREATE TABLE ai_tool_usage (
    usage_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id UUID REFERENCES student_profiles(student_id) ON DELETE CASCADE,
    tool_name VARCHAR(100) NOT NULL CHECK (tool_name IN ('resume_builder', 'career_counselor', 'interview_prep', 'skill_gap')),
    used_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    result_data JSONB,
    deleted_at TIMESTAMP NULL
);

CREATE INDEX idx_ai_usage_student ON ai_tool_usage(student_id) WHERE deleted_at IS NULL;
CREATE INDEX idx_ai_usage_tool ON ai_tool_usage(tool_name) WHERE deleted_at IS NULL;
CREATE INDEX idx_ai_usage_date ON ai_tool_usage(used_at DESC) WHERE deleted_at IS NULL;

-- ============================================================================
-- 10. SOCIAL FEED
-- ============================================================================

CREATE TABLE posts (
    post_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    author_id UUID REFERENCES users(user_id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    post_type VARCHAR(20) NOT NULL CHECK (post_type IN ('job', 'mentor', 'general', 'achievement')),
    related_job_id UUID REFERENCES jobs(job_id) ON DELETE SET NULL,
    related_mentor_id UUID REFERENCES mentor_profiles(mentor_id) ON DELETE SET NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    likes_count INT DEFAULT 0,
    comments_count INT DEFAULT 0,
    deleted_at TIMESTAMP NULL
);

CREATE INDEX idx_posts_author ON posts(author_id) WHERE deleted_at IS NULL;
CREATE INDEX idx_posts_created ON posts(created_at DESC) WHERE deleted_at IS NULL;
CREATE INDEX idx_posts_type ON posts(post_type) WHERE deleted_at IS NULL;

CREATE TABLE post_likes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    post_id UUID REFERENCES posts(post_id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(user_id) ON DELETE CASCADE,
    liked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL,
    UNIQUE(post_id, user_id)
);

CREATE INDEX idx_post_likes_post ON post_likes(post_id) WHERE deleted_at IS NULL;
CREATE INDEX idx_post_likes_user ON post_likes(user_id) WHERE deleted_at IS NULL;

CREATE TABLE post_comments (
    comment_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    post_id UUID REFERENCES posts(post_id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(user_id) ON DELETE CASCADE,
    comment_text TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL
);

CREATE INDEX idx_comments_post ON post_comments(post_id, created_at) WHERE deleted_at IS NULL;
CREATE INDEX idx_comments_user ON post_comments(user_id) WHERE deleted_at IS NULL;

-- ============================================================================
-- 11. CONNECTIONS & NETWORKING
-- ============================================================================

CREATE TABLE connections (
    connection_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id_1 UUID REFERENCES users(user_id) ON DELETE CASCADE,
    user_id_2 UUID REFERENCES users(user_id) ON DELETE CASCADE,
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'accepted', 'rejected')),
    requested_by UUID REFERENCES users(user_id) ON DELETE CASCADE,
    requested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    accepted_at TIMESTAMP,
    deleted_at TIMESTAMP NULL,
    CHECK (user_id_1 < user_id_2)
);

CREATE INDEX idx_connections_user1 ON connections(user_id_1) WHERE deleted_at IS NULL;
CREATE INDEX idx_connections_user2 ON connections(user_id_2) WHERE deleted_at IS NULL;
CREATE INDEX idx_connections_status ON connections(status) WHERE deleted_at IS NULL;

-- ============================================================================
-- 12. NOTIFICATIONS
-- ============================================================================

CREATE TABLE notifications (
    notification_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(user_id) ON DELETE CASCADE,
    type VARCHAR(50) NOT NULL,
    title VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    link_url VARCHAR(500),
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL
);

CREATE INDEX idx_notifications_user ON notifications(user_id, created_at DESC) WHERE deleted_at IS NULL;
CREATE INDEX idx_notifications_unread ON notifications(user_id, is_read) WHERE deleted_at IS NULL AND is_read = FALSE;

-- ============================================================================
-- 13. ACHIEVEMENTS & GAMIFICATION
-- ============================================================================

CREATE TABLE achievements (
    achievement_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT NOT NULL,
    icon VARCHAR(100),
    badge_type VARCHAR(50) NOT NULL,
    deleted_at TIMESTAMP NULL
);

CREATE INDEX idx_achievements_type ON achievements(badge_type) WHERE deleted_at IS NULL;

CREATE TABLE user_achievements (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(user_id) ON DELETE CASCADE,
    achievement_id UUID REFERENCES achievements(achievement_id) ON DELETE CASCADE,
    earned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL,
    UNIQUE(user_id, achievement_id)
);

CREATE INDEX idx_user_achievements_user ON user_achievements(user_id) WHERE deleted_at IS NULL;

-- ============================================================================
-- 14. WEBSOCKET SESSION MANAGEMENT
-- ============================================================================

CREATE TABLE websocket_sessions (
    session_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(user_id) ON DELETE CASCADE,
    socket_id VARCHAR(255) NOT NULL UNIQUE,
    connected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_ping_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_online BOOLEAN DEFAULT TRUE,
    user_agent TEXT,
    ip_address VARCHAR(45)
);

CREATE INDEX idx_websocket_user ON websocket_sessions(user_id);
CREATE INDEX idx_websocket_online ON websocket_sessions(is_online) WHERE is_online = TRUE;

-- ============================================================================
-- 15. FILE UPLOADS TRACKING
-- ============================================================================

CREATE TABLE file_uploads (
    file_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(user_id) ON DELETE CASCADE,
    file_name VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    file_type VARCHAR(100),
    file_size BIGINT,
    category VARCHAR(50) NOT NULL CHECK (category IN ('profile', 'resume', 'logo', 'course', 'attachment')),
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL
);

CREATE INDEX idx_uploads_user ON file_uploads(user_id) WHERE deleted_at IS NULL;
CREATE INDEX idx_uploads_category ON file_uploads(category) WHERE deleted_at IS NULL;

-- ============================================================================
-- DATABASE TRIGGERS
-- ============================================================================

-- Update likes_count on posts
CREATE OR REPLACE FUNCTION update_post_likes_count()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' AND NEW.deleted_at IS NULL THEN
        UPDATE posts SET likes_count = likes_count + 1 WHERE post_id = NEW.post_id;
    ELSIF TG_OP = 'DELETE' OR (TG_OP = 'UPDATE' AND NEW.deleted_at IS NOT NULL AND OLD.deleted_at IS NULL) THEN
        UPDATE posts SET likes_count = likes_count - 1 WHERE post_id = OLD.post_id;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_post_likes_count
AFTER INSERT OR UPDATE OR DELETE ON post_likes
FOR EACH ROW EXECUTE FUNCTION update_post_likes_count();

-- Update comments_count on posts
CREATE OR REPLACE FUNCTION update_post_comments_count()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' AND NEW.deleted_at IS NULL THEN
        UPDATE posts SET comments_count = comments_count + 1 WHERE post_id = NEW.post_id;
    ELSIF TG_OP = 'DELETE' OR (TG_OP = 'UPDATE' AND NEW.deleted_at IS NOT NULL AND OLD.deleted_at IS NULL) THEN
        UPDATE posts SET comments_count = comments_count - 1 WHERE post_id = OLD.post_id;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_post_comments_count
AFTER INSERT OR UPDATE OR DELETE ON post_comments
FOR EACH ROW EXECUTE FUNCTION update_post_comments_count();

-- Update mentor rating when review added/updated
CREATE OR REPLACE FUNCTION update_mentor_rating()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE mentor_profiles
    SET rating = (
        SELECT COALESCE(AVG(rating)::DECIMAL(3,2), 0.0)
        FROM mentorship_reviews
        WHERE mentor_id = COALESCE(NEW.mentor_id, OLD.mentor_id) AND deleted_at IS NULL
    )
    WHERE mentor_id = COALESCE(NEW.mentor_id, OLD.mentor_id);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_mentor_rating
AFTER INSERT OR UPDATE OR DELETE ON mentorship_reviews
FOR EACH ROW EXECUTE FUNCTION update_mentor_rating();

-- Update conversation timestamp when message sent
CREATE OR REPLACE FUNCTION update_conversation_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE conversations
    SET updated_at = NEW.sent_at
    WHERE conversation_id = NEW.conversation_id;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_conversation_timestamp
AFTER INSERT ON messages
FOR EACH ROW EXECUTE FUNCTION update_conversation_timestamp();

-- Update updated_at timestamp automatically
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_users_updated_at BEFORE UPDATE ON users
FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER trigger_job_applications_updated_at BEFORE UPDATE ON job_applications
FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ============================================================================
-- SEED DATA - Sample Achievements
-- ============================================================================

INSERT INTO achievements (name, description, icon, badge_type) VALUES
('First Login', 'Complete your first login to Collabio', 'trophy', 'general'),
('Profile Complete', 'Fill out your complete profile information', 'user-check', 'profile'),
('First Application', 'Submit your first job application', 'briefcase', 'career'),
('Top Contributor', 'Create 50+ community posts', 'star', 'social'),
('Course Champion', 'Complete 5 courses', 'book-open', 'learning'),
('Networking Pro', 'Connect with 100+ professionals', 'users', 'networking'),
('Interview Ready', 'Complete 10+ mock interviews', 'video', 'ai_tools'),
('Mentor Matched', 'Complete your first mentorship session', 'heart', 'mentorship'),
('Resume Master', 'Update your resume 5+ times', 'file-text', 'ai_tools'),
('Early Adopter', 'Join Collabio in its first month', 'award', 'special');

-- ============================================================================
-- END OF SCHEMA
-- ============================================================================
