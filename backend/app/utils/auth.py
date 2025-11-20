"""
Authentication utilities
"""
from functools import wraps
from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from app.models.user import User


def token_required(fn):
    """Decorator to require JWT token"""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            print(f"[DEBUG token_required] ===== Starting token verification for {fn.__name__} =====")
            print(f"[DEBUG token_required] Authorization header: {request.headers.get('Authorization', 'NOT FOUND')}")
            print(f"[DEBUG token_required] All headers: {dict(request.headers)}")
            verify_jwt_in_request()
            print(f"[DEBUG token_required] JWT verified successfully for {fn.__name__}")
            return fn(*args, **kwargs)
        except Exception as e:
            print(f"[DEBUG token_required] JWT verification FAILED for {fn.__name__}")
            print(f"[DEBUG token_required] Error type: {type(e).__name__}")
            print(f"[DEBUG token_required] Error message: {str(e)}")
            import traceback
            traceback.print_exc()
            return jsonify({'error': 'Invalid or expired token', 'message': str(e)}), 401
    return wrapper


def get_current_user():
    """Get current user from JWT token"""
    try:
        verify_jwt_in_request()
        user_id = get_jwt_identity()
        user = User.query.filter_by(user_id=user_id, deleted_at=None).first()
        return user
    except:
        return None


def get_user_type():
    """Get current user type from JWT token"""
    user = get_current_user()
    return user.user_type if user else None


def user_type_required(*allowed_types):
    """Decorator to require specific user types"""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            user = get_current_user()
            print(f"[DEBUG user_type_required] User: {user}")
            print(f"[DEBUG user_type_required] User ID: {user.user_id if user else None}")
            print(f"[DEBUG user_type_required] User Type: {user.user_type if user else None}")
            print(f"[DEBUG user_type_required] Allowed Types: {allowed_types}")
            if not user:
                print(f"[DEBUG user_type_required] No user found - returning 401")
                return jsonify({'error': 'Authentication required'}), 401
            if user.user_type not in allowed_types:
                print(f"[DEBUG user_type_required] User type '{user.user_type}' not in {allowed_types} - returning 403")
                return jsonify({'error': 'Access denied', 'message': f'This endpoint is only for {", ".join(allowed_types)}'}), 403
            print(f"[DEBUG user_type_required] Access granted!")
            return fn(*args, **kwargs)
        return wrapper
    return decorator
