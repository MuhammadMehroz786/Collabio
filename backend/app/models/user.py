"""
User Model
"""
import uuid
from datetime import datetime
from app.extensions import db, bcrypt
from app.models.base import BaseModel, SoftDeleteMixin, TimestampMixin


class User(BaseModel, TimestampMixin, SoftDeleteMixin):
    """User model for authentication"""
    __tablename__ = 'users'

    user_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    user_type = db.Column(
        db.String(20),
        nullable=False,
        index=True
    )
    is_verified = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    last_login = db.Column(db.DateTime, nullable=True)

    # Relationships
    student_profile = db.relationship('StudentProfile', backref='user', uselist=False, cascade='all, delete-orphan')
    employer_profile = db.relationship('EmployerProfile', backref='user', uselist=False, cascade='all, delete-orphan')
    mentor_profile = db.relationship('MentorProfile', backref='user', uselist=False, cascade='all, delete-orphan')
    notifications = db.relationship('Notification', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    achievements = db.relationship('UserAchievement', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    posts = db.relationship('Post', backref='author', lazy='dynamic', foreign_keys='Post.author_id')

    def __init__(self, email, password, user_type):
        self.email = email
        self.set_password(password)
        self.user_type = user_type

    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        """Check if password matches"""
        return bcrypt.check_password_hash(self.password_hash, password)

    def update_last_login(self):
        """Update last login timestamp"""
        self.last_login = datetime.utcnow()
        db.session.commit()

    def to_dict(self, include_profile=False):
        """Convert to dictionary"""
        data = {
            'user_id': self.user_id,
            'email': self.email,
            'user_type': self.user_type,
            'is_verified': self.is_verified,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None
        }

        if include_profile:
            if self.user_type == 'student' and self.student_profile:
                data['profile'] = self.student_profile.to_dict()
            elif self.user_type == 'employer' and self.employer_profile:
                data['profile'] = self.employer_profile.to_dict()
            elif self.user_type == 'mentor' and self.mentor_profile:
                data['profile'] = self.mentor_profile.to_dict()

        return data

    def __repr__(self):
        return f'<User {self.email}>'
