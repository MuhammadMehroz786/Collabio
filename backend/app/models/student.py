"""
Student Models
"""
import uuid
from datetime import date
from app.extensions import db
from app.models.base import BaseModel, SoftDeleteMixin


class StudentProfile(BaseModel, SoftDeleteMixin):
    """Student profile model"""
    __tablename__ = 'student_profiles'

    student_id = db.Column(db.String(36), db.ForeignKey('users.user_id', ondelete='CASCADE'), primary_key=True)
    full_name = db.Column(db.String(255), nullable=False)
    profile_picture = db.Column(db.String(500))
    bio = db.Column(db.Text)
    location = db.Column(db.String(255))
    phone_number = db.Column(db.String(20))
    date_of_birth = db.Column(db.Date)
    resume_url = db.Column(db.String(500))
    portfolio_url = db.Column(db.String(500))
    linkedin_url = db.Column(db.String(500))
    github_url = db.Column(db.String(500))
    joined_date = db.Column(db.Date, nullable=False, default=date.today)
    connections_count = db.Column(db.Integer, default=0)
    applications_count = db.Column(db.Integer, default=0)

    # Relationships
    education = db.relationship('StudentEducation', backref='student', lazy='dynamic', cascade='all, delete-orphan')
    experience = db.relationship('StudentExperience', backref='student', lazy='dynamic', cascade='all, delete-orphan')
    skills = db.relationship('StudentSkill', backref='student', lazy='dynamic', cascade='all, delete-orphan')
    applications = db.relationship('JobApplication', backref='student', lazy='dynamic', cascade='all, delete-orphan')
    saved_jobs = db.relationship('SavedJob', backref='student', lazy='dynamic', cascade='all, delete-orphan')
    enrollments = db.relationship('CourseEnrollment', backref='student', lazy='dynamic', cascade='all, delete-orphan')
    ai_usage = db.relationship('AIToolUsage', backref='student', lazy='dynamic', cascade='all, delete-orphan')

    def to_dict(self, include_relations=False):
        """Convert to dictionary"""
        data = {
            'student_id': self.student_id,
            'full_name': self.full_name,
            'profile_picture': self.profile_picture,
            'bio': self.bio,
            'location': self.location,
            'phone_number': self.phone_number,
            'date_of_birth': self.date_of_birth.isoformat() if self.date_of_birth else None,
            'resume_url': self.resume_url,
            'portfolio_url': self.portfolio_url,
            'linkedin_url': self.linkedin_url,
            'github_url': self.github_url,
            'joined_date': self.joined_date.isoformat() if self.joined_date else None,
            'connections_count': self.connections_count,
            'applications_count': self.applications_count
        }

        if include_relations:
            data['education'] = [edu.to_dict() for edu in self.education.filter_by(deleted_at=None)]
            data['experience'] = [exp.to_dict() for exp in self.experience.filter_by(deleted_at=None)]
            data['skills'] = [skill.to_dict() for skill in self.skills.filter_by(deleted_at=None)]

        return data

    def __repr__(self):
        return f'<StudentProfile {self.full_name}>'


class StudentEducation(BaseModel, SoftDeleteMixin):
    """Student education model"""
    __tablename__ = 'student_education'

    education_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    student_id = db.Column(db.String(36), db.ForeignKey('student_profiles.student_id', ondelete='CASCADE'), nullable=False)
    institution_name = db.Column(db.String(255), nullable=False)
    degree = db.Column(db.String(100), nullable=False)
    field_of_study = db.Column(db.String(100), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)
    gpa = db.Column(db.Numeric(3, 2))
    is_current = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            'education_id': self.education_id,
            'institution_name': self.institution_name,
            'degree': self.degree,
            'field_of_study': self.field_of_study,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'gpa': float(self.gpa) if self.gpa else None,
            'is_current': self.is_current
        }


class StudentExperience(BaseModel, SoftDeleteMixin):
    """Student experience model"""
    __tablename__ = 'student_experience'

    experience_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    student_id = db.Column(db.String(36), db.ForeignKey('student_profiles.student_id', ondelete='CASCADE'), nullable=False)
    company_name = db.Column(db.String(255), nullable=False)
    position = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(255))
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)
    description = db.Column(db.Text)
    is_current = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            'experience_id': self.experience_id,
            'company_name': self.company_name,
            'position': self.position,
            'location': self.location,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'description': self.description,
            'is_current': self.is_current
        }


class StudentSkill(BaseModel, SoftDeleteMixin):
    """Student skill model"""
    __tablename__ = 'student_skills'

    skill_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    student_id = db.Column(db.String(36), db.ForeignKey('student_profiles.student_id', ondelete='CASCADE'), nullable=False)
    skill_name = db.Column(db.String(100), nullable=False)
    proficiency_level = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def to_dict(self):
        return {
            'skill_id': self.skill_id,
            'skill_name': self.skill_name,
            'proficiency_level': self.proficiency_level,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
