"""
Job Routes
"""
from flask import Blueprint, request
from datetime import datetime
from app.utils.auth import token_required, user_type_required, get_current_user
from app.utils.helpers import success_response, error_response, paginate, parse_datetime
from app.utils.validators import validate_required_fields
from app.models.all_models import Job, JobSkillRequired, JobApplication, SavedJob
from app.extensions import db

jobs_bp = Blueprint('jobs', __name__)


@jobs_bp.route('/', methods=['GET'])
@token_required
def get_jobs():
    """Get all active jobs (paginated, filterable)"""
    user = get_current_user()

    # If employer, only return their jobs
    if user.user_type == 'employer' and user.employer_profile:
        query = Job.query.filter_by(
            employer_id=user.employer_profile.employer_id,
            deleted_at=None
        )
    else:
        # For students, return all active jobs
        query = Job.query.filter_by(status='active', deleted_at=None)

    # Filters
    if 'job_type' in request.args:
        query = query.filter_by(job_type=request.args['job_type'])

    if 'work_mode' in request.args:
        query = query.filter_by(work_mode=request.args['work_mode'])

    if 'location' in request.args:
        query = query.filter(Job.location.ilike(f"%{request.args['location']}%"))

    if 'company' in request.args:
        query = query.filter(Job.company_name.ilike(f"%{request.args['company']}%"))

    # Search by title or description
    if 'search' in request.args:
        search_term = f"%{request.args['search']}%"
        query = query.filter(
            db.or_(
                Job.title.ilike(search_term),
                Job.description.ilike(search_term)
            )
        )

    # Sort
    sort_by = request.args.get('sort_by', 'posted_at')
    if sort_by == 'posted_at':
        query = query.order_by(Job.posted_at.desc())
    elif sort_by == 'salary':
        query = query.order_by(Job.salary_max.desc())

    result = paginate(query)
    return success_response(data=result)


@jobs_bp.route('/<job_id>', methods=['GET'])
@token_required
def get_job(job_id):
    """Get single job"""
    job = Job.query.filter_by(job_id=job_id, deleted_at=None).first()

    if not job:
        return error_response('Job not found', status=404)

    # Increment views
    job.views_count += 1
    db.session.commit()

    return success_response(data=job.to_dict(include_skills=True))


@jobs_bp.route('/', methods=['POST'])
@token_required
@user_type_required('employer')
def create_job():
    """Create new job posting"""
    user = get_current_user()
    data = request.get_json()

    valid, error = validate_required_fields(data, ['title', 'description', 'job_type'])
    if not valid:
        return error_response(error, status=400)

    try:
        job = Job(
            employer_id=user.employer_profile.employer_id,
            title=data['title'],
            company_name=user.employer_profile.company_name,
            description=data['description'],
            location=data.get('location'),
            job_type=data['job_type'],
            work_mode=data.get('work_mode'),
            salary_min=data.get('salary_min'),
            salary_max=data.get('salary_max'),
            salary_currency=data.get('salary_currency', 'USD'),
            salary_period=data.get('salary_period'),
            requirements=data.get('requirements'),
            expires_at=parse_datetime(data.get('expires_at')) if data.get('expires_at') else None,
            status=data.get('status', 'active')
        )
        job.save()

        # Add required skills
        if 'skills' in data and isinstance(data['skills'], list):
            for skill_name in data['skills']:
                skill = JobSkillRequired(
                    job_id=job.job_id,
                    skill_name=skill_name,
                    is_required=True
                )
                skill.save()

        return success_response(
            data=job.to_dict(include_skills=True),
            message='Job created successfully',
            status=201
        )

    except Exception as e:
        db.session.rollback()
        return error_response(f'Failed to create job: {str(e)}', status=500)


@jobs_bp.route('/<job_id>', methods=['PUT'])
@token_required
@user_type_required('employer')
def update_job(job_id):
    """Update job posting"""
    user = get_current_user()
    job = Job.query.filter_by(
        job_id=job_id,
        employer_id=user.employer_profile.employer_id,
        deleted_at=None
    ).first()

    if not job:
        return error_response('Job not found or unauthorized', status=404)

    data = request.get_json()
    allowed_fields = ['title', 'description', 'location', 'job_type', 'work_mode',
                     'salary_min', 'salary_max', 'salary_period', 'requirements', 'status']

    for field in allowed_fields:
        if field in data:
            setattr(job, field, data[field])

    if 'expires_at' in data:
        job.expires_at = parse_datetime(data['expires_at']) if data['expires_at'] else None

    db.session.commit()
    return success_response(data=job.to_dict(), message='Job updated successfully')


@jobs_bp.route('/<job_id>', methods=['DELETE'])
@token_required
@user_type_required('employer')
def delete_job(job_id):
    """Delete job posting"""
    user = get_current_user()
    job = Job.query.filter_by(
        job_id=job_id,
        employer_id=user.employer_profile.employer_id,
        deleted_at=None
    ).first()

    if not job:
        return error_response('Job not found or unauthorized', status=404)

    job.soft_delete()
    return success_response(message='Job deleted successfully')


@jobs_bp.route('/<job_id>/apply', methods=['POST'])
@token_required
@user_type_required('student')
def apply_to_job(job_id):
    """Apply to a job"""
    user = get_current_user()
    student = user.student_profile
    data = request.get_json() or {}

    job = Job.query.filter_by(job_id=job_id, status='active', deleted_at=None).first()
    if not job:
        return error_response('Job not found or no longer active', status=404)

    # Check if already applied
    existing = JobApplication.query.filter_by(
        job_id=job_id,
        student_id=student.student_id,
        deleted_at=None
    ).first()

    if existing:
        return error_response('Already applied to this job', status=409)

    try:
        application = JobApplication(
            job_id=job_id,
            student_id=student.student_id,
            cover_letter=data.get('cover_letter'),
            resume_url=data.get('resume_url', student.resume_url)
        )
        application.save()

        # Update student applications count
        student.applications_count += 1
        db.session.commit()

        return success_response(
            data=application.to_dict(),
            message='Application submitted successfully',
            status=201
        )

    except Exception as e:
        db.session.rollback()
        return error_response(f'Failed to submit application: {str(e)}', status=500)


@jobs_bp.route('/applications/my', methods=['GET'])
@token_required
@user_type_required('student')
def get_my_applications():
    """Get my job applications"""
    user = get_current_user()
    student = user.student_profile

    query = JobApplication.query.filter_by(
        student_id=student.student_id,
        deleted_at=None
    ).order_by(JobApplication.applied_at.desc())

    result = paginate(query)
    return success_response(data=result)


@jobs_bp.route('/<job_id>/applications', methods=['GET'])
@token_required
@user_type_required('employer')
def get_job_applications(job_id):
    """Get applications for a job (employer only)"""
    print(f"[DEBUG] get_job_applications called for job_id: {job_id}")
    try:
        user = get_current_user()
        print(f"[DEBUG] User: {user}, Type: {user.user_type if user else 'None'}")

        if not user or not user.employer_profile:
            print(f"[DEBUG] No employer profile found")
            return error_response('Employer profile not found', status=404)

        print(f"[DEBUG] Employer ID: {user.employer_profile.employer_id}")

        # Verify job belongs to employer
        job = Job.query.filter_by(
            job_id=job_id,
            employer_id=user.employer_profile.employer_id,
            deleted_at=None
        ).first()

        print(f"[DEBUG] Job found: {job is not None}")

        if not job:
            print(f"[DEBUG] Job not found or doesn't belong to employer")
            return error_response('Job not found or unauthorized', status=404)
    except Exception as e:
        print(f"[ERROR] get_job_applications exception: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        return error_response(f'Error fetching applications: {str(e)}', status=500)

    query = JobApplication.query.filter_by(
        job_id=job_id,
        deleted_at=None
    ).order_by(JobApplication.applied_at.desc())

    # Filter by status
    if 'status' in request.args:
        query = query.filter_by(status=request.args['status'])

    # Get page and per_page from request args
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    per_page = min(per_page, 100)  # Max limit

    # Paginate
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    # Serialize with student information
    applications_data = [app.to_dict(include_student=True) for app in pagination.items]

    result = {
        'data': applications_data,
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

    return success_response(data=result)


@jobs_bp.route('/applications/<application_id>/status', methods=['PUT'])
@token_required
@user_type_required('employer')
def update_application_status(application_id):
    """Update application status (employer only)"""
    from app.models.all_models import Conversation, ConversationParticipant, Message, Notification

    user = get_current_user()
    data = request.get_json()

    valid, error = validate_required_fields(data, ['status'])
    if not valid:
        return error_response(error, status=400)

    # Valid statuses
    valid_statuses = ['pending', 'reviewing', 'shortlisted', 'rejected', 'accepted']
    if data['status'] not in valid_statuses:
        return error_response(f"Invalid status. Must be one of: {', '.join(valid_statuses)}", status=400)

    application = JobApplication.query.filter_by(
        application_id=application_id,
        deleted_at=None
    ).first()

    if not application:
        return error_response('Application not found', status=404)

    # Verify application belongs to employer's job
    if application.job.employer_id != user.employer_profile.employer_id:
        return error_response('Unauthorized', status=403)

    old_status = application.status
    application.status = data['status']

    print(f"[DEBUG] Status change: {old_status} -> {data['status']}")
    print(f"[DEBUG] Should send message: {data['status'] == 'accepted' and old_status != 'accepted'}")

    try:
        # If application is accepted, create conversation and send message
        if data['status'] == 'accepted' and old_status != 'accepted':
            print(f"[DEBUG] Creating conversation and sending message...")
            employer_user_id = user.user_id
            student_user_id = application.student.user.user_id
            print(f"[DEBUG] Employer user ID: {employer_user_id}, Student user ID: {student_user_id}")

            # Check if conversation already exists between employer and student
            existing_conversation = db.session.query(Conversation).join(
                ConversationParticipant,
                Conversation.conversation_id == ConversationParticipant.conversation_id
            ).filter(
                ConversationParticipant.user_id.in_([employer_user_id, student_user_id]),
                Conversation.deleted_at == None
            ).group_by(Conversation.conversation_id).having(
                db.func.count(ConversationParticipant.user_id) == 2
            ).first()

            if not existing_conversation:
                # Create new conversation
                print(f"[DEBUG] Creating new conversation...")
                conversation = Conversation()
                conversation.save()
                print(f"[DEBUG] Conversation created with ID: {conversation.conversation_id}")

                # Add participants
                employer_participant = ConversationParticipant(
                    conversation_id=conversation.conversation_id,
                    user_id=employer_user_id
                )
                employer_participant.save()
                print(f"[DEBUG] Added employer participant")

                student_participant = ConversationParticipant(
                    conversation_id=conversation.conversation_id,
                    user_id=student_user_id
                )
                student_participant.save()
                print(f"[DEBUG] Added student participant")
            else:
                conversation = existing_conversation
                print(f"[DEBUG] Using existing conversation ID: {conversation.conversation_id}")

            # Send automated message from employer to student
            message_text = f"Congratulations! Your application for the {application.job.title} position has been accepted. We're excited to move forward with you. Feel free to reach out if you have any questions!"

            print(f"[DEBUG] Creating message...")
            message = Message(
                conversation_id=conversation.conversation_id,
                sender_id=employer_user_id,
                message_text=message_text
            )
            message.save()
            print(f"[DEBUG] Message saved with ID: {message.message_id}")

            # Create notification for student
            print(f"[DEBUG] Creating notification...")
            notification = Notification(
                user_id=student_user_id,
                type='application_accepted',
                title='Application Accepted!',
                message=f'Your application for {application.job.title} at {application.job.company_name} has been accepted!',
                link_url=f'/student/applications'
            )
            notification.save()
            print(f"[DEBUG] Notification saved with ID: {notification.notification_id}")
            print(f"[DEBUG] *** Message and notification created successfully! ***")

        db.session.commit()

        return success_response(
            data=application.to_dict(),
            message=f'Application status updated to {data["status"]}'
        )

    except Exception as e:
        db.session.rollback()
        return error_response(f'Failed to update application status: {str(e)}', status=500)


@jobs_bp.route('/<job_id>/save', methods=['POST'])
@token_required
@user_type_required('student')
def save_job(job_id):
    """Save/bookmark a job"""
    user = get_current_user()
    student = user.student_profile

    job = Job.query.filter_by(job_id=job_id, deleted_at=None).first()
    if not job:
        return error_response('Job not found', status=404)

    # Check if already saved
    existing = SavedJob.query.filter_by(
        student_id=student.student_id,
        job_id=job_id,
        deleted_at=None
    ).first()

    if existing:
        return error_response('Job already saved', status=409)

    saved = SavedJob(
        student_id=student.student_id,
        job_id=job_id
    )
    saved.save()

    return success_response(message='Job saved successfully', status=201)


@jobs_bp.route('/<job_id>/unsave', methods=['DELETE'])
@token_required
@user_type_required('student')
def unsave_job(job_id):
    """Remove job from saved"""
    user = get_current_user()
    student = user.student_profile

    saved = SavedJob.query.filter_by(
        student_id=student.student_id,
        job_id=job_id,
        deleted_at=None
    ).first()

    if not saved:
        return error_response('Saved job not found', status=404)

    saved.soft_delete()
    return success_response(message='Job removed from saved')


@jobs_bp.route('/saved/my', methods=['GET'])
@token_required
@user_type_required('student')
def get_my_saved_jobs():
    """Get my saved jobs"""
    user = get_current_user()
    student = user.student_profile

    query = SavedJob.query.filter_by(
        student_id=student.student_id,
        deleted_at=None
    ).order_by(SavedJob.saved_at.desc())

    result = paginate(query)
    return success_response(data=result)


@jobs_bp.route('/recommendations', methods=['GET'])
@token_required
@user_type_required('student')
def get_recommended_jobs():
    """Get AI-matched job recommendations"""
    user = get_current_user()
    student = user.student_profile

    from app.services.ai_matching import get_recommended_jobs

    limit = request.args.get('limit', 10, type=int)
    recommendations = get_recommended_jobs(student, limit=limit)

    return success_response(data=recommendations, message=f'Found {len(recommendations)} recommended jobs')
