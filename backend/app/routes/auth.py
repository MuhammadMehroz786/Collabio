"""
Authentication Routes
Endpoints for user registration, login, logout
"""
from flask import Blueprint, request
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required
from app.extensions import db
from app.models.user import User
from app.models.student import StudentProfile
from app.models.employer import EmployerProfile
from app.models.mentor import MentorProfile
from app.utils.validators import validate_email, validate_password, validate_required_fields
from app.utils.helpers import success_response, error_response
from app.utils.auth import token_required

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Register new user
    Body: {email, password, user_type, full_name or company_name}
    """
    data = request.get_json()

    # Validate required fields
    valid, error = validate_required_fields(data, ['email', 'password', 'user_type'])
    if not valid:
        return error_response(error, status=400)

    # Validate user_type
    if data['user_type'] not in ['student', 'employer', 'mentor']:
        return error_response('Invalid user_type. Must be student, employer, or mentor', status=400)

    # Validate email
    valid, error = validate_email(data['email'])
    if not valid:
        return error_response(error, status=400)

    # Validate password
    valid, error = validate_password(data['password'])
    if not valid:
        return error_response(error, status=400)

    # Check if user already exists
    if User.query.filter_by(email=data['email'], deleted_at=None).first():
        return error_response('Email already registered', status=409)

    try:
        # Create user
        user = User(
            email=data['email'],
            password=data['password'],
            user_type=data['user_type']
        )
        user.save()

        # Create corresponding profile
        if data['user_type'] == 'student':
            if 'full_name' not in data:
                return error_response('full_name is required for students', status=400)
            profile = StudentProfile(
                student_id=user.user_id,
                full_name=data['full_name']
            )
        elif data['user_type'] == 'employer':
            if 'company_name' not in data:
                return error_response('company_name is required for employers', status=400)
            profile = EmployerProfile(
                employer_id=user.user_id,
                company_name=data['company_name']
            )
        else:  # mentor
            if 'full_name' not in data or 'current_role' not in data or 'current_company' not in data:
                return error_response('full_name, current_role, and current_company are required for mentors', status=400)
            profile = MentorProfile(
                mentor_id=user.user_id,
                full_name=data['full_name'],
                current_role=data['current_role'],
                current_company=data['current_company']
            )

        profile.save()

        # Generate tokens
        access_token = create_access_token(identity=user.user_id)
        refresh_token = create_refresh_token(identity=user.user_id)

        return success_response(
            data={
                'user': user.to_dict(include_profile=True),
                'access_token': access_token,
                'refresh_token': refresh_token
            },
            message='User registered successfully',
            status=201
        )

    except Exception as e:
        db.session.rollback()
        return error_response(f'Registration failed: {str(e)}', status=500)


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Login user
    Body: {email, password}
    """
    data = request.get_json()

    # Validate required fields
    valid, error = validate_required_fields(data, ['email', 'password'])
    if not valid:
        return error_response(error, status=400)

    # Find user
    user = User.query.filter_by(email=data['email'], deleted_at=None).first()

    if not user or not user.check_password(data['password']):
        return error_response('Invalid email or password', status=401)

    if not user.is_active:
        return error_response('Account is inactive', status=403)

    try:
        # Update last login
        user.update_last_login()

        # Generate tokens
        access_token = create_access_token(identity=user.user_id)
        refresh_token = create_refresh_token(identity=user.user_id)

        return success_response(
            data={
                'user': user.to_dict(include_profile=True),
                'access_token': access_token,
                'refresh_token': refresh_token
            },
            message='Login successful'
        )

    except Exception as e:
        return error_response(f'Login failed: {str(e)}', status=500)


@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """
    Refresh access token
    Requires: Valid refresh token in Authorization header
    """
    try:
        user_id = get_jwt_identity()
        new_access_token = create_access_token(identity=user_id)

        return success_response(
            data={'access_token': new_access_token},
            message='Token refreshed successfully'
        )

    except Exception as e:
        return error_response(f'Token refresh failed: {str(e)}', status=500)


@auth_bp.route('/me', methods=['GET'])
@token_required
def get_current_user_info():
    """
    Get current user information
    Requires: Valid access token
    """
    try:
        from app.utils.auth import get_current_user
        user = get_current_user()

        if not user:
            return error_response('User not found', status=404)

        return success_response(
            data=user.to_dict(include_profile=True),
            message='User info retrieved successfully'
        )

    except Exception as e:
        return error_response(f'Failed to get user info: {str(e)}', status=500)


@auth_bp.route('/change-password', methods=['POST'])
@token_required
def change_password():
    """
    Change user password
    Body: {old_password, new_password}
    """
    data = request.get_json()

    valid, error = validate_required_fields(data, ['old_password', 'new_password'])
    if not valid:
        return error_response(error, status=400)

    from app.utils.auth import get_current_user
    user = get_current_user()

    if not user.check_password(data['old_password']):
        return error_response('Current password is incorrect', status=401)

    # Validate new password
    valid, error = validate_password(data['new_password'])
    if not valid:
        return error_response(error, status=400)

    try:
        user.set_password(data['new_password'])
        user.save()

        return success_response(message='Password changed successfully')

    except Exception as e:
        db.session.rollback()
        return error_response(f'Password change failed: {str(e)}', status=500)
