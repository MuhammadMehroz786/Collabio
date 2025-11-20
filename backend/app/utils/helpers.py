"""
Helper utilities
"""
from flask import request, jsonify, current_app
from datetime import datetime


def paginate(query, page=None, per_page=None):
    """
    Paginate a SQLAlchemy query

    Args:
        query: SQLAlchemy query object
        page: Page number (default from request args)
        per_page: Items per page (default from config)

    Returns:
        dict: Paginated results with metadata
    """
    page = page or request.args.get('page', 1, type=int)
    per_page = per_page or request.args.get('per_page', current_app.config.get('PAGINATION_DEFAULT_LIMIT', 20), type=int)

    # Enforce max limit
    max_limit = current_app.config.get('PAGINATION_MAX_LIMIT', 100)
    per_page = min(per_page, max_limit)

    # Paginate
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    return {
        'data': [item.to_dict() if hasattr(item, 'to_dict') else item for item in pagination.items],
        'meta': {
            'page': page,
            'per_page': per_page,
            'total': pagination.total,
            'pages': pagination.pages,
            'has_next': pagination.has_next,
            'has_prev': pagination.has_prev,
            'next_page': page + 1 if pagination.has_next else None,
            'prev_page': page - 1 if pagination.has_prev else None
        }
    }


def success_response(data=None, message=None, status=200):
    """
    Create standardized success response

    Args:
        data: Response data
        message: Success message
        status: HTTP status code

    Returns:
        tuple: (response, status_code)
    """
    response = {
        'success': True,
        'timestamp': datetime.utcnow().isoformat()
    }

    if message:
        response['message'] = message

    if data is not None:
        response['data'] = data

    return jsonify(response), status


def error_response(message, errors=None, status=400):
    """
    Create standardized error response

    Args:
        message: Error message
        errors: Detailed errors (dict or list)
        status: HTTP status code

    Returns:
        tuple: (response, status_code)
    """
    response = {
        'success': False,
        'error': message,
        'timestamp': datetime.utcnow().isoformat()
    }

    if errors:
        response['errors'] = errors

    return jsonify(response), status


def parse_date(date_string, date_format='%Y-%m-%d'):
    """
    Parse date string to date object

    Args:
        date_string: Date string
        date_format: Expected date format

    Returns:
        date object or None
    """
    if not date_string:
        return None

    try:
        return datetime.strptime(date_string, date_format).date()
    except ValueError:
        return None


def parse_datetime(datetime_string, datetime_format='%Y-%m-%d %H:%M:%S'):
    """
    Parse datetime string to datetime object

    Args:
        datetime_string: Datetime string
        datetime_format: Expected datetime format

    Returns:
        datetime object or None
    """
    if not datetime_string:
        return None

    try:
        return datetime.strptime(datetime_string, datetime_format)
    except ValueError:
        return None


def get_or_404(model, record_id, error_message=None):
    """
    Get record by ID or return 404 error

    Args:
        model: SQLAlchemy model class
        record_id: Record ID
        error_message: Custom error message

    Returns:
        Model instance or error response
    """
    record = model.query.filter_by(deleted_at=None).filter(
        getattr(model, f'{model.__tablename__[:-1]}_id') == record_id
    ).first()

    if not record:
        message = error_message or f"{model.__name__} not found"
        return error_response(message, status=404)

    return record


def filter_dict(data, allowed_keys):
    """
    Filter dictionary to only include allowed keys

    Args:
        data: Dictionary to filter
        allowed_keys: List of allowed keys

    Returns:
        Filtered dictionary
    """
    return {key: value for key, value in data.items() if key in allowed_keys}
