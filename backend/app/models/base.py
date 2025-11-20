"""
Base model with common fields and methods
"""
from datetime import datetime
from app.extensions import db


class SoftDeleteMixin:
    """Mixin for soft delete functionality"""
    deleted_at = db.Column(db.DateTime, nullable=True)

    def soft_delete(self):
        """Mark record as deleted"""
        self.deleted_at = datetime.utcnow()
        db.session.commit()

    def restore(self):
        """Restore deleted record"""
        self.deleted_at = None
        db.session.commit()

    @property
    def is_deleted(self):
        """Check if record is deleted"""
        return self.deleted_at is not None

    @classmethod
    def query_active(cls):
        """Query only non-deleted records"""
        return cls.query.filter(cls.deleted_at.is_(None))


class TimestampMixin:
    """Mixin for created_at and updated_at timestamps"""
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)


class BaseModel(db.Model):
    """Abstract base model"""
    __abstract__ = True

    def save(self):
        """Save model to database"""
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        """Delete model from database"""
        db.session.delete(self)
        db.session.commit()

    def update(self, **kwargs):
        """Update model fields"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        db.session.commit()
        return self

    def to_dict(self, exclude=None):
        """Convert model to dictionary"""
        exclude = exclude or []
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
            if column.name not in exclude
        }
