"""
Student Routes
"""
from flask import Blueprint, request
from app.utils.auth import token_required, user_type_required, get_current_user
from app.utils.helpers import success_response, error_response, paginate, parse_date
from app.utils.validators import validate_required_fields, validate_date_range
from app.utils.file_handler import save_file
from app.models.student import StudentProfile, StudentEducation, StudentExperience, StudentSkill
from app.extensions import db

students_bp = Blueprint('students', __name__)


@students_bp.route('/', methods=['GET'])
@token_required
def get_students():
    """Get all students (paginated)"""
    query = StudentProfile.query.filter_by(deleted_at=None)

    # Filter by location
    if 'location' in request.args:
        query = query.filter(StudentProfile.location.ilike(f"%{request.args['location']}%"))

    result = paginate(query)
    return success_response(data=result)


@students_bp.route('/<student_id>', methods=['GET'])
@token_required
def get_student(student_id):
    """Get single student profile"""
    student = StudentProfile.query.filter_by(student_id=student_id, deleted_at=None).first()
    if not student:
        return error_response('Student not found', status=404)
    return success_response(data=student.to_dict(include_relations=True))


@students_bp.route('/me', methods=['GET'])
@token_required
@user_type_required('student')
def get_my_profile():
    """Get current student's profile"""
    user = get_current_user()
    student = user.student_profile
    return success_response(data=student.to_dict(include_relations=True))


@students_bp.route('/me', methods=['PUT'])
@token_required
@user_type_required('student')
def update_my_profile():
    """Update current student's profile"""
    user = get_current_user()
    student = user.student_profile
    data = request.get_json()

    allowed_fields = ['full_name', 'bio', 'location', 'phone_number', 'date_of_birth',
                      'portfolio_url', 'linkedin_url', 'github_url']

    for field in allowed_fields:
        if field in data:
            if field == 'date_of_birth' and data[field]:
                student.date_of_birth = parse_date(data[field])
            else:
                setattr(student, field, data[field])

    db.session.commit()
    return success_response(data=student.to_dict(), message='Profile updated successfully')


@students_bp.route('/me/profile-picture', methods=['POST'])
@token_required
@user_type_required('student')
def upload_profile_picture():
    """Upload profile picture"""
    if 'file' not in request.files:
        return error_response('No file provided', status=400)

    file = request.files['file']
    user = get_current_user()
    student = user.student_profile

    result = save_file(file, category='profiles', resize_image=(400, 400))

    if not result['success']:
        return error_response(result['error'], status=400)

    student.profile_picture = result['file_path']
    db.session.commit()

    return success_response(data={'profile_picture': student.profile_picture},
                          message='Profile picture uploaded successfully')


@students_bp.route('/me/resume', methods=['POST'])
@token_required
@user_type_required('student')
def upload_resume():
    """Upload resume"""
    if 'file' not in request.files:
        return error_response('No file provided', status=400)

    file = request.files['file']
    user = get_current_user()
    student = user.student_profile

    result = save_file(file, category='resumes')

    if not result['success']:
        return error_response(result['error'], status=400)

    student.resume_url = result['file_path']
    db.session.commit()

    return success_response(data={'resume_url': student.resume_url},
                          message='Resume uploaded successfully')


# Education endpoints
@students_bp.route('/me/education', methods=['GET'])
@token_required
@user_type_required('student')
def get_my_education():
    """Get my education records"""
    user = get_current_user()
    student = user.student_profile
    education = student.education.filter_by(deleted_at=None).all()
    return success_response(data=[edu.to_dict() for edu in education])


@students_bp.route('/me/education', methods=['POST'])
@token_required
@user_type_required('student')
def add_education():
    """Add education record"""
    user = get_current_user()
    student = user.student_profile
    data = request.get_json()

    valid, error = validate_required_fields(data, ['institution_name', 'degree', 'field_of_study', 'start_date'])
    if not valid:
        return error_response(error, status=400)

    start_date = parse_date(data['start_date'])
    end_date = parse_date(data.get('end_date')) if data.get('end_date') else None

    if end_date:
        valid, error = validate_date_range(start_date, end_date)
        if not valid:
            return error_response(error, status=400)

    education = StudentEducation(
        student_id=student.student_id,
        institution_name=data['institution_name'],
        degree=data['degree'],
        field_of_study=data['field_of_study'],
        start_date=start_date,
        end_date=end_date,
        gpa=data.get('gpa'),
        is_current=data.get('is_current', False)
    )
    education.save()

    return success_response(data=education.to_dict(), message='Education added successfully', status=201)


@students_bp.route('/me/education/<education_id>', methods=['PUT'])
@token_required
@user_type_required('student')
def update_education(education_id):
    """Update education record"""
    user = get_current_user()
    education = StudentEducation.query.filter_by(
        education_id=education_id,
        student_id=user.student_profile.student_id,
        deleted_at=None
    ).first()

    if not education:
        return error_response('Education record not found', status=404)

    data = request.get_json()
    allowed_fields = ['institution_name', 'degree', 'field_of_study', 'start_date',
                     'end_date', 'gpa', 'is_current']

    for field in allowed_fields:
        if field in data:
            if field in ['start_date', 'end_date'] and data[field]:
                setattr(education, field, parse_date(data[field]))
            else:
                setattr(education, field, data[field])

    db.session.commit()
    return success_response(data=education.to_dict(), message='Education updated successfully')


@students_bp.route('/me/education/<education_id>', methods=['DELETE'])
@token_required
@user_type_required('student')
def delete_education(education_id):
    """Delete education record"""
    user = get_current_user()
    education = StudentEducation.query.filter_by(
        education_id=education_id,
        student_id=user.student_profile.student_id,
        deleted_at=None
    ).first()

    if not education:
        return error_response('Education record not found', status=404)

    education.soft_delete()
    return success_response(message='Education deleted successfully')


# Experience endpoints
@students_bp.route('/me/experience', methods=['GET'])
@token_required
@user_type_required('student')
def get_my_experience():
    """Get my experience records"""
    user = get_current_user()
    student = user.student_profile
    experience = student.experience.filter_by(deleted_at=None).all()
    return success_response(data=[exp.to_dict() for exp in experience])


@students_bp.route('/me/experience', methods=['POST'])
@token_required
@user_type_required('student')
def add_experience():
    """Add experience record"""
    user = get_current_user()
    student = user.student_profile
    data = request.get_json()

    valid, error = validate_required_fields(data, ['company_name', 'position', 'start_date'])
    if not valid:
        return error_response(error, status=400)

    start_date = parse_date(data['start_date'])
    end_date = parse_date(data.get('end_date')) if data.get('end_date') else None

    if end_date:
        valid, error = validate_date_range(start_date, end_date)
        if not valid:
            return error_response(error, status=400)

    experience = StudentExperience(
        student_id=student.student_id,
        company_name=data['company_name'],
        position=data['position'],
        location=data.get('location'),
        start_date=start_date,
        end_date=end_date,
        description=data.get('description'),
        is_current=data.get('is_current', False)
    )
    experience.save()

    return success_response(data=experience.to_dict(), message='Experience added successfully', status=201)


@students_bp.route('/me/experience/<experience_id>', methods=['DELETE'])
@token_required
@user_type_required('student')
def delete_experience(experience_id):
    """Delete experience record"""
    user = get_current_user()
    experience = StudentExperience.query.filter_by(
        experience_id=experience_id,
        student_id=user.student_profile.student_id,
        deleted_at=None
    ).first()

    if not experience:
        return error_response('Experience record not found', status=404)

    experience.soft_delete()
    return success_response(message='Experience deleted successfully')


# Skills endpoints
@students_bp.route('/me/skills', methods=['GET'])
@token_required
@user_type_required('student')
def get_my_skills():
    """Get my skills"""
    user = get_current_user()
    student = user.student_profile
    skills = student.skills.filter_by(deleted_at=None).all()
    return success_response(data=[skill.to_dict() for skill in skills])


@students_bp.route('/me/skills', methods=['POST'])
@token_required
@user_type_required('student')
def add_skill():
    """Add skill"""
    user = get_current_user()
    student = user.student_profile
    data = request.get_json()

    valid, error = validate_required_fields(data, ['skill_name'])
    if not valid:
        return error_response(error, status=400)

    # Check if skill already exists
    existing = student.skills.filter_by(
        skill_name=data['skill_name'],
        deleted_at=None
    ).first()

    if existing:
        return error_response('Skill already exists', status=409)

    skill = StudentSkill(
        student_id=student.student_id,
        skill_name=data['skill_name'],
        proficiency_level=data.get('proficiency_level')
    )
    skill.save()

    return success_response(data=skill.to_dict(), message='Skill added successfully', status=201)


@students_bp.route('/me/skills/<skill_id>', methods=['DELETE'])
@token_required
@user_type_required('student')
def delete_skill(skill_id):
    """Delete skill"""
    user = get_current_user()
    skill = StudentSkill.query.filter_by(
        skill_id=skill_id,
        student_id=user.student_profile.student_id,
        deleted_at=None
    ).first()

    if not skill:
        return error_response('Skill not found', status=404)

    skill.soft_delete()
    return success_response(message='Skill deleted successfully')
