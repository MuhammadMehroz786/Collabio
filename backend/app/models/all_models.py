"""
All remaining models in consolidated format
Import this in __init__.py as needed
"""
import uuid
from datetime import datetime, date
from app.extensions import db
from app.models.base import BaseModel, SoftDeleteMixin, TimestampMixin


# EMPLOYER MODEL
class EmployerProfile(BaseModel, SoftDeleteMixin):
    __tablename__ = 'employer_profiles'

    employer_id = db.Column(db.String(36), db.ForeignKey('users.user_id', ondelete='CASCADE'), primary_key=True)
    company_name = db.Column(db.String(255), nullable=False)
    company_logo = db.Column(db.String(500))
    industry = db.Column(db.String(100))
    company_size = db.Column(db.String(20))
    website = db.Column(db.String(500))
    description = db.Column(db.Text)
    location = db.Column(db.String(255))
    founded_year = db.Column(db.Integer)

    jobs = db.relationship('Job', backref='employer', lazy='dynamic', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'employer_id': self.employer_id,
            'company_name': self.company_name,
            'company_logo': self.company_logo,
            'industry': self.industry,
            'company_size': self.company_size,
            'website': self.website,
            'description': self.description,
            'location': self.location,
            'founded_year': self.founded_year
        }


# MENTOR MODELS
class MentorProfile(BaseModel, SoftDeleteMixin):
    __tablename__ = 'mentor_profiles'

    mentor_id = db.Column(db.String(36), db.ForeignKey('users.user_id', ondelete='CASCADE'), primary_key=True)
    full_name = db.Column(db.String(255), nullable=False)
    profile_picture = db.Column(db.String(500))
    current_role = db.Column(db.String(255), nullable=False)
    current_company = db.Column(db.String(255), nullable=False)
    bio = db.Column(db.Text)
    years_of_experience = db.Column(db.Integer)
    rating = db.Column(db.Numeric(3, 2), default=0.0)
    total_sessions = db.Column(db.Integer, default=0)
    linkedin_url = db.Column(db.String(500))

    expertise = db.relationship('MentorExpertise', backref='mentor', lazy='dynamic', cascade='all, delete-orphan')
    mentorship_requests = db.relationship('MentorshipRequest', backref='mentor', lazy='dynamic', foreign_keys='MentorshipRequest.mentor_id')

    def to_dict(self, include_expertise=False):
        data = {
            'mentor_id': self.mentor_id,
            'full_name': self.full_name,
            'profile_picture': self.profile_picture,
            'current_role': self.current_role,
            'current_company': self.current_company,
            'bio': self.bio,
            'years_of_experience': self.years_of_experience,
            'rating': float(self.rating) if self.rating else 0.0,
            'total_sessions': self.total_sessions,
            'linkedin_url': self.linkedin_url
        }
        if include_expertise:
            data['expertise'] = [e.expertise_area for e in self.expertise.filter_by(deleted_at=None)]
        return data


class MentorExpertise(BaseModel, SoftDeleteMixin):
    __tablename__ = 'mentor_expertise'

    expertise_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    mentor_id = db.Column(db.String(36), db.ForeignKey('mentor_profiles.mentor_id', ondelete='CASCADE'))
    expertise_area = db.Column(db.String(100), nullable=False)


# JOB MODELS
class Job(BaseModel, SoftDeleteMixin, TimestampMixin):
    __tablename__ = 'jobs'

    job_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    employer_id = db.Column(db.String(36), db.ForeignKey('employer_profiles.employer_id', ondelete='CASCADE'))
    title = db.Column(db.String(255), nullable=False)
    company_name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(255))
    job_type = db.Column(db.String(20), nullable=False)
    work_mode = db.Column(db.String(20))
    salary_min = db.Column(db.Numeric(10, 2))
    salary_max = db.Column(db.Numeric(10, 2))
    salary_currency = db.Column(db.String(3), default='USD')
    salary_period = db.Column(db.String(20))
    requirements = db.Column(db.Text)
    posted_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='active')
    views_count = db.Column(db.Integer, default=0)

    skills_required = db.relationship('JobSkillRequired', backref='job', lazy='dynamic', cascade='all, delete-orphan')
    applications = db.relationship('JobApplication', backref='job', lazy='dynamic', cascade='all, delete-orphan')

    def to_dict(self, include_skills=False):
        data = {
            'job_id': self.job_id,
            'employer_id': self.employer_id,
            'title': self.title,
            'company_name': self.company_name,
            'description': self.description,
            'location': self.location,
            'job_type': self.job_type,
            'work_mode': self.work_mode,
            'salary_min': float(self.salary_min) if self.salary_min else None,
            'salary_max': float(self.salary_max) if self.salary_max else None,
            'salary_currency': self.salary_currency,
            'salary_period': self.salary_period,
            'requirements': self.requirements,
            'posted_at': self.posted_at.isoformat() if self.posted_at else None,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'status': self.status,
            'views_count': self.views_count
        }
        if include_skills:
            data['skills'] = [s.skill_name for s in self.skills_required.filter_by(deleted_at=None)]
        return data


class JobSkillRequired(BaseModel, SoftDeleteMixin):
    __tablename__ = 'job_skills_required'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    job_id = db.Column(db.String(36), db.ForeignKey('jobs.job_id', ondelete='CASCADE'))
    skill_name = db.Column(db.String(100), nullable=False)
    is_required = db.Column(db.Boolean, default=True)


class JobApplication(BaseModel, SoftDeleteMixin):
    __tablename__ = 'job_applications'

    application_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    job_id = db.Column(db.String(36), db.ForeignKey('jobs.job_id', ondelete='CASCADE'))
    student_id = db.Column(db.String(36), db.ForeignKey('student_profiles.student_id', ondelete='CASCADE'))
    cover_letter = db.Column(db.Text)
    resume_url = db.Column(db.String(500))
    status = db.Column(db.String(20), default='pending')
    applied_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self, include_student=False):
        data = {
            'application_id': self.application_id,
            'job_id': self.job_id,
            'student_id': self.student_id,
            'cover_letter': self.cover_letter,
            'resume_url': self.resume_url,
            'status': self.status,
            'applied_at': self.applied_at.isoformat() if self.applied_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

        if include_student and self.student:
            # Split full_name into first and last name for compatibility
            name_parts = (self.student.full_name or '').split(' ', 1)
            first_name = name_parts[0] if len(name_parts) > 0 else ''
            last_name = name_parts[1] if len(name_parts) > 1 else ''

            data['student'] = {
                'student_id': self.student.student_id,
                'full_name': self.student.full_name,
                'user': {
                    'user_id': self.student.user.user_id,
                    'first_name': first_name,
                    'last_name': last_name,
                    'email': self.student.user.email
                }
            }

        return data


class SavedJob(BaseModel, SoftDeleteMixin):
    __tablename__ = 'saved_jobs'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    student_id = db.Column(db.String(36), db.ForeignKey('student_profiles.student_id', ondelete='CASCADE'))
    job_id = db.Column(db.String(36), db.ForeignKey('jobs.job_id', ondelete='CASCADE'))
    saved_at = db.Column(db.DateTime, default=datetime.utcnow)


# MENTORSHIP MODELS
class MentorshipRequest(BaseModel, SoftDeleteMixin):
    __tablename__ = 'mentorship_requests'

    request_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    student_id = db.Column(db.String(36), db.ForeignKey('student_profiles.student_id', ondelete='CASCADE'))
    mentor_id = db.Column(db.String(36), db.ForeignKey('mentor_profiles.mentor_id', ondelete='CASCADE'))
    message = db.Column(db.Text)
    status = db.Column(db.String(20), default='pending')
    requested_at = db.Column(db.DateTime, default=datetime.utcnow)
    responded_at = db.Column(db.DateTime)

    def to_dict(self):
        return {
            'request_id': self.request_id,
            'student_id': self.student_id,
            'mentor_id': self.mentor_id,
            'message': self.message,
            'status': self.status,
            'requested_at': self.requested_at.isoformat() if self.requested_at else None,
            'responded_at': self.responded_at.isoformat() if self.responded_at else None
        }


class MentorshipSession(BaseModel, SoftDeleteMixin):
    __tablename__ = 'mentorship_sessions'

    session_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    request_id = db.Column(db.String(36), db.ForeignKey('mentorship_requests.request_id', ondelete='CASCADE'))
    student_id = db.Column(db.String(36), db.ForeignKey('student_profiles.student_id', ondelete='CASCADE'))
    mentor_id = db.Column(db.String(36), db.ForeignKey('mentor_profiles.mentor_id', ondelete='CASCADE'))
    scheduled_at = db.Column(db.DateTime, nullable=False)
    duration_minutes = db.Column(db.Integer)
    meeting_link = db.Column(db.String(500))
    notes = db.Column(db.Text)
    status = db.Column(db.String(20), default='scheduled')
    completed_at = db.Column(db.DateTime)


class MentorshipReview(BaseModel, SoftDeleteMixin):
    __tablename__ = 'mentorship_reviews'

    review_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = db.Column(db.String(36), db.ForeignKey('mentorship_sessions.session_id', ondelete='CASCADE'))
    student_id = db.Column(db.String(36), db.ForeignKey('student_profiles.student_id', ondelete='CASCADE'))
    mentor_id = db.Column(db.String(36), db.ForeignKey('mentor_profiles.mentor_id', ondelete='CASCADE'))
    rating = db.Column(db.Integer, nullable=False)
    review_text = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# MESSAGING MODELS
class Conversation(BaseModel, SoftDeleteMixin, TimestampMixin):
    __tablename__ = 'conversations'

    conversation_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    participants = db.relationship('ConversationParticipant', backref='conversation', lazy='dynamic', cascade='all, delete-orphan')
    messages = db.relationship('Message', backref='conversation', lazy='dynamic', cascade='all, delete-orphan')


class ConversationParticipant(BaseModel, SoftDeleteMixin):
    __tablename__ = 'conversation_participants'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    conversation_id = db.Column(db.String(36), db.ForeignKey('conversations.conversation_id', ondelete='CASCADE'))
    user_id = db.Column(db.String(36), db.ForeignKey('users.user_id', ondelete='CASCADE'))
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_read_at = db.Column(db.DateTime)


class Message(BaseModel, SoftDeleteMixin):
    __tablename__ = 'messages'

    message_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    conversation_id = db.Column(db.String(36), db.ForeignKey('conversations.conversation_id', ondelete='CASCADE'))
    sender_id = db.Column(db.String(36), db.ForeignKey('users.user_id', ondelete='CASCADE'))
    message_text = db.Column(db.Text, nullable=False)
    sent_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_read = db.Column(db.Boolean, default=False)
    attachment_url = db.Column(db.String(500))

    def to_dict(self):
        return {
            'message_id': self.message_id,
            'conversation_id': self.conversation_id,
            'sender_id': self.sender_id,
            'message_text': self.message_text,
            'sent_at': self.sent_at.isoformat() if self.sent_at else None,
            'is_read': self.is_read,
            'attachment_url': self.attachment_url
        }


# COURSE MODELS
class Course(BaseModel, SoftDeleteMixin, TimestampMixin):
    __tablename__ = 'courses'

    course_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(100))
    difficulty_level = db.Column(db.String(20))
    duration_weeks = db.Column(db.Integer)
    thumbnail_url = db.Column(db.String(500))
    total_students = db.Column(db.Integer, default=0)
    instructor_name = db.Column(db.String(255))

    lessons = db.relationship('CourseLesson', backref='course', lazy='dynamic', cascade='all, delete-orphan')
    enrollments = db.relationship('CourseEnrollment', backref='course', lazy='dynamic', cascade='all, delete-orphan')

    def to_dict(self, include_lessons=False):
        data = {
            'course_id': self.course_id,
            'title': self.title,
            'description': self.description,
            'category': self.category,
            'difficulty_level': self.difficulty_level,
            'duration_weeks': self.duration_weeks,
            'thumbnail_url': self.thumbnail_url,
            'total_students': self.total_students,
            'instructor_name': self.instructor_name
        }
        if include_lessons:
            data['lessons'] = [l.to_dict() for l in self.lessons.filter_by(deleted_at=None).order_by('lesson_number')]
        return data


class CourseLesson(BaseModel, SoftDeleteMixin):
    __tablename__ = 'course_lessons'

    lesson_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    course_id = db.Column(db.String(36), db.ForeignKey('courses.course_id', ondelete='CASCADE'))
    lesson_number = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text)
    video_url = db.Column(db.String(500))
    duration_minutes = db.Column(db.Integer)

    def to_dict(self):
        return {
            'lesson_id': self.lesson_id,
            'lesson_number': self.lesson_number,
            'title': self.title,
            'content': self.content,
            'video_url': self.video_url,
            'duration_minutes': self.duration_minutes
        }


class CourseEnrollment(BaseModel, SoftDeleteMixin):
    __tablename__ = 'course_enrollments'

    enrollment_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    student_id = db.Column(db.String(36), db.ForeignKey('student_profiles.student_id', ondelete='CASCADE'))
    course_id = db.Column(db.String(36), db.ForeignKey('courses.course_id', ondelete='CASCADE'))
    enrolled_at = db.Column(db.DateTime, default=datetime.utcnow)
    progress_percentage = db.Column(db.Integer, default=0)
    completed_lessons = db.Column(db.Integer, default=0)
    completed_at = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='in_progress')


# AI TOOL USAGE
class AIToolUsage(BaseModel, SoftDeleteMixin):
    __tablename__ = 'ai_tool_usage'

    usage_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    student_id = db.Column(db.String(36), db.ForeignKey('student_profiles.student_id', ondelete='CASCADE'))
    tool_name = db.Column(db.String(100), nullable=False)
    used_at = db.Column(db.DateTime, default=datetime.utcnow)
    result_data = db.Column(db.JSON)


# SOCIAL MODELS
class Post(BaseModel, SoftDeleteMixin, TimestampMixin):
    __tablename__ = 'posts'

    post_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    author_id = db.Column(db.String(36), db.ForeignKey('users.user_id', ondelete='CASCADE'))
    content = db.Column(db.Text, nullable=False)
    post_type = db.Column(db.String(20), nullable=False)
    related_job_id = db.Column(db.String(36), db.ForeignKey('jobs.job_id', ondelete='SET NULL'))
    related_mentor_id = db.Column(db.String(36), db.ForeignKey('mentor_profiles.mentor_id', ondelete='SET NULL'))
    likes_count = db.Column(db.Integer, default=0)
    comments_count = db.Column(db.Integer, default=0)

    likes = db.relationship('PostLike', backref='post', lazy='dynamic', cascade='all, delete-orphan')
    comments = db.relationship('PostComment', backref='post', lazy='dynamic', cascade='all, delete-orphan')


class PostLike(BaseModel, SoftDeleteMixin):
    __tablename__ = 'post_likes'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    post_id = db.Column(db.String(36), db.ForeignKey('posts.post_id', ondelete='CASCADE'))
    user_id = db.Column(db.String(36), db.ForeignKey('users.user_id', ondelete='CASCADE'))
    liked_at = db.Column(db.DateTime, default=datetime.utcnow)


class PostComment(BaseModel, SoftDeleteMixin):
    __tablename__ = 'post_comments'

    comment_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    post_id = db.Column(db.String(36), db.ForeignKey('posts.post_id', ondelete='CASCADE'))
    user_id = db.Column(db.String(36), db.ForeignKey('users.user_id', ondelete='CASCADE'))
    comment_text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# CONNECTION MODEL
class Connection(BaseModel, SoftDeleteMixin):
    __tablename__ = 'connections'

    connection_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id_1 = db.Column(db.String(36), db.ForeignKey('users.user_id', ondelete='CASCADE'))
    user_id_2 = db.Column(db.String(36), db.ForeignKey('users.user_id', ondelete='CASCADE'))
    status = db.Column(db.String(20), default='pending')
    requested_by = db.Column(db.String(36), db.ForeignKey('users.user_id', ondelete='CASCADE'))
    requested_at = db.Column(db.DateTime, default=datetime.utcnow)
    accepted_at = db.Column(db.DateTime)


# NOTIFICATION MODEL
class Notification(BaseModel, SoftDeleteMixin):
    __tablename__ = 'notifications'

    notification_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.user_id', ondelete='CASCADE'))
    type = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    message = db.Column(db.Text, nullable=False)
    link_url = db.Column(db.String(500))
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'notification_id': self.notification_id,
            'type': self.type,
            'title': self.title,
            'message': self.message,
            'link_url': self.link_url,
            'is_read': self.is_read,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


# ACHIEVEMENT MODELS
class Achievement(BaseModel, SoftDeleteMixin):
    __tablename__ = 'achievements'

    achievement_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=False)
    icon = db.Column(db.String(100))
    badge_type = db.Column(db.String(50), nullable=False)


class UserAchievement(BaseModel, SoftDeleteMixin):
    __tablename__ = 'user_achievements'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.user_id', ondelete='CASCADE'))
    achievement_id = db.Column(db.String(36), db.ForeignKey('achievements.achievement_id', ondelete='CASCADE'))
    earned_at = db.Column(db.DateTime, default=datetime.utcnow)


# WEBSOCKET SESSION MODEL
class WebSocketSession(BaseModel):
    __tablename__ = 'websocket_sessions'

    session_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.user_id', ondelete='CASCADE'))
    socket_id = db.Column(db.String(255), nullable=False, unique=True)
    connected_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_ping_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_online = db.Column(db.Boolean, default=True)
    user_agent = db.Column(db.Text)
    ip_address = db.Column(db.String(45))


# FILE UPLOAD MODEL
class FileUpload(BaseModel, SoftDeleteMixin):
    __tablename__ = 'file_uploads'

    file_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.user_id', ondelete='CASCADE'))
    file_name = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    file_type = db.Column(db.String(100))
    file_size = db.Column(db.BigInteger)
    category = db.Column(db.String(50), nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
