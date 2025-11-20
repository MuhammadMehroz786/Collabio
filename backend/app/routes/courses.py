"""
Courses Routes
"""
from flask import Blueprint, request
from app.utils.auth import token_required, user_type_required, get_current_user
from app.utils.helpers import success_response, error_response, paginate
from app.models.all_models import Course, CourseEnrollment
from app.extensions import db

courses_bp = Blueprint('courses', __name__)


@courses_bp.route('/', methods=['GET'])
@token_required
def get_courses():
    """Get all courses"""
    query = Course.query.filter_by(deleted_at=None)

    # Filter by category
    if 'category' in request.args:
        query = query.filter_by(category=request.args['category'])

    # Filter by difficulty
    if 'difficulty' in request.args:
        query = query.filter_by(difficulty_level=request.args['difficulty'])

    # Search
    if 'search' in request.args:
        search_term = f"%{request.args['search']}%"
        query = query.filter(
            db.or_(
                Course.title.ilike(search_term),
                Course.description.ilike(search_term)
            )
        )

    query = query.order_by(Course.total_students.desc())
    result = paginate(query)
    return success_response(data=result)


@courses_bp.route('/<course_id>', methods=['GET'])
@token_required
def get_course(course_id):
    """Get course details"""
    course = Course.query.filter_by(course_id=course_id, deleted_at=None).first()
    if not course:
        return error_response('Course not found', status=404)
    return success_response(data=course.to_dict(include_lessons=True))


@courses_bp.route('/<course_id>/enroll', methods=['POST'])
@token_required
@user_type_required('student')
def enroll_in_course(course_id):
    """Enroll in a course"""
    user = get_current_user()
    student = user.student_profile

    course = Course.query.filter_by(course_id=course_id, deleted_at=None).first()
    if not course:
        return error_response('Course not found', status=404)

    # Check if already enrolled
    existing = CourseEnrollment.query.filter_by(
        student_id=student.student_id,
        course_id=course_id,
        deleted_at=None
    ).first()

    if existing:
        return error_response('Already enrolled in this course', status=409)

    try:
        enrollment = CourseEnrollment(
            student_id=student.student_id,
            course_id=course_id
        )
        enrollment.save()

        # Update course total_students
        course.total_students += 1
        db.session.commit()

        return success_response(message='Enrolled successfully', status=201)

    except Exception as e:
        db.session.rollback()
        return error_response(f'Failed to enroll: {str(e)}', status=500)


@courses_bp.route('/my-enrollments', methods=['GET'])
@token_required
@user_type_required('student')
def get_my_enrollments():
    """Get my course enrollments"""
    user = get_current_user()
    student = user.student_profile

    query = CourseEnrollment.query.filter_by(
        student_id=student.student_id,
        deleted_at=None
    ).order_by(CourseEnrollment.enrolled_at.desc())

    # Filter by status
    if 'status' in request.args:
        query = query.filter_by(status=request.args['status'])

    result = paginate(query)
    return success_response(data=result)


@courses_bp.route('/enrollments/<enrollment_id>/progress', methods=['PUT'])
@token_required
@user_type_required('student')
def update_progress(enrollment_id):
    """Update course progress"""
    user = get_current_user()
    data = request.get_json()

    enrollment = CourseEnrollment.query.filter_by(
        enrollment_id=enrollment_id,
        student_id=user.student_profile.student_id,
        deleted_at=None
    ).first()

    if not enrollment:
        return error_response('Enrollment not found', status=404)

    if 'progress_percentage' in data:
        enrollment.progress_percentage = min(max(int(data['progress_percentage']), 0), 100)

    if 'completed_lessons' in data:
        enrollment.completed_lessons = int(data['completed_lessons'])

    # Auto-complete if 100%
    if enrollment.progress_percentage == 100 and not enrollment.completed_at:
        enrollment.completed_at = db.func.current_timestamp()
        enrollment.status = 'completed'

    db.session.commit()
    return success_response(message='Progress updated successfully')
