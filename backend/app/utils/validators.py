"""
Validation utilities
"""
import re
from flask import current_app


def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not email or not re.match(pattern, email):
        return False, "Invalid email format"
    return True, None


def validate_password(password):
    """Validate password strength"""
    config = current_app.config
    min_length = config.get('PASSWORD_MIN_LENGTH', 8)

    if not password or len(password) < min_length:
        return False, f"Password must be at least {min_length} characters"

    if config.get('PASSWORD_REQUIRE_UPPERCASE', True) and not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"

    if config.get('PASSWORD_REQUIRE_LOWERCASE', True) and not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"

    if config.get('PASSWORD_REQUIRE_NUMBERS', True) and not re.search(r'\d', password):
        return False, "Password must contain at least one number"

    if config.get('PASSWORD_REQUIRE_SPECIAL', True) and not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, "Password must contain at least one special character"

    return True, None


def validate_file(filename, allowed_extensions=None):
    """Validate file extension"""
    if not filename:
        return False, "No filename provided"

    if '.' not in filename:
        return False, "File must have an extension"

    ext = filename.rsplit('.', 1)[1].lower()

    if allowed_extensions is None:
        allowed_extensions = current_app.config.get('ALLOWED_EXTENSIONS', set())

    if ext not in allowed_extensions:
        return False, f"File extension .{ext} is not allowed. Allowed: {', '.join(allowed_extensions)}"

    return True, None


def validate_required_fields(data, required_fields):
    """Check if all required fields are present"""
    missing = [field for field in required_fields if field not in data or not data[field]]
    if missing:
        return False, f"Missing required fields: {', '.join(missing)}"
    return True, None


def validate_date_range(start_date, end_date):
    """Validate that end_date is after start_date"""
    if end_date and start_date and end_date < start_date:
        return False, "End date must be after start date"
    return True, None
