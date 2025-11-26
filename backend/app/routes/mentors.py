"""
Mentor Routes
"""
from flask import Blueprint, request
from app.utils.auth import token_required, user_type_required, get_current_user
from app.utils.helpers import success_response, error_response, paginate, parse_datetime
from app.utils.validators import validate_required_fields
from app.models.all_models import MentorProfile, MentorshipRequest, MentorshipSession, MentorshipReview
from app.extensions import db

mentors_bp = Blueprint('mentors', __name__)


@mentors_bp.route('/', methods=['GET'])
def get_mentors():
    """Get all mentors (public)"""
    query = MentorProfile.query.filter_by(deleted_at=None)

    # Filter by expertise
    if 'expertise' in request.args:
        from app.models.all_models import MentorExpertise
        expertise_filter = request.args['expertise']
        query = query.join(MentorExpertise).filter(
            MentorExpertise.expertise_area.ilike(f"%{expertise_filter}%"),
            MentorExpertise.deleted_at.is_(None)
        )

    # Filter by rating
    if 'min_rating' in request.args:
        min_rating = float(request.args['min_rating'])
        query = query.filter(MentorProfile.rating >= min_rating)

    # Sort
    sort_by = request.args.get('sort_by', 'rating')
    if sort_by == 'rating':
        query = query.order_by(MentorProfile.rating.desc())
    elif sort_by == 'sessions':
        query = query.order_by(MentorProfile.total_sessions.desc())

    # Get paginated results and include expertise in each mentor
    result = paginate(query)
    # Transform data to include expertise
    if 'data' in result and isinstance(result['data'], list):
        result['data'] = [mentor.to_dict(include_expertise=True) for mentor in query.limit(result['meta']['per_page']).offset((result['meta']['page'] - 1) * result['meta']['per_page']).all()]

    return success_response(data=result)


@mentors_bp.route('/<mentor_id>', methods=['GET'])
def get_mentor(mentor_id):
    """Get mentor profile (public)"""
    mentor = MentorProfile.query.filter_by(mentor_id=mentor_id, deleted_at=None).first()
    if not mentor:
        return error_response('Mentor not found', status=404)
    return success_response(data=mentor.to_dict(include_expertise=True))


@mentors_bp.route('/<mentor_id>/request', methods=['POST'])
@token_required
@user_type_required('student')
def request_mentorship(mentor_id):
    """Request mentorship session"""
    user = get_current_user()
    student = user.student_profile
    data = request.get_json() or {}

    mentor = MentorProfile.query.filter_by(mentor_id=mentor_id, deleted_at=None).first()
    if not mentor:
        return error_response('Mentor not found', status=404)

    # Check if already have pending request
    existing = MentorshipRequest.query.filter_by(
        student_id=student.student_id,
        mentor_id=mentor_id,
        status='pending',
        deleted_at=None
    ).first()

    if existing:
        return error_response('Already have a pending request with this mentor', status=409)

    try:
        request_obj = MentorshipRequest(
            student_id=student.student_id,
            mentor_id=mentor_id,
            message=data.get('message')
        )
        request_obj.save()

        return success_response(
            data=request_obj.to_dict(),
            message='Mentorship request sent successfully',
            status=201
        )

    except Exception as e:
        db.session.rollback()
        return error_response(f'Failed to send request: {str(e)}', status=500)


@mentors_bp.route('/requests/my', methods=['GET'])
@token_required
def get_my_requests():
    """Get my mentorship requests (student or mentor)"""
    user = get_current_user()

    if user.user_type == 'student':
        query = MentorshipRequest.query.filter_by(
            student_id=user.student_profile.student_id,
            deleted_at=None
        )
    elif user.user_type == 'mentor':
        query = MentorshipRequest.query.filter_by(
            mentor_id=user.mentor_profile.mentor_id,
            deleted_at=None
        )
    else:
        return error_response('Only students and mentors can access this endpoint', status=403)

    # Filter by status
    if 'status' in request.args:
        query = query.filter_by(status=request.args['status'])

    query = query.order_by(MentorshipRequest.requested_at.desc())
    result = paginate(query)
    return success_response(data=result)


@mentors_bp.route('/requests/<request_id>/respond', methods=['PUT'])
@token_required
@user_type_required('mentor')
def respond_to_request(request_id):
    """Respond to mentorship request (accept/reject) and send message to student"""
    from app.models.all_models import Conversation, ConversationParticipant, Message

    user = get_current_user()
    data = request.get_json()

    valid, error = validate_required_fields(data, ['status'])
    if not valid:
        return error_response(error, status=400)

    if data['status'] not in ['accepted', 'rejected']:
        return error_response('Status must be "accepted" or "rejected"', status=400)

    request_obj = MentorshipRequest.query.filter_by(
        request_id=request_id,
        mentor_id=user.mentor_profile.mentor_id,
        deleted_at=None
    ).first()

    if not request_obj:
        return error_response('Request not found or unauthorized', status=404)

    if request_obj.status != 'pending':
        return error_response('Request has already been responded to', status=400)

    try:
        request_obj.status = data['status']
        request_obj.responded_at = db.func.current_timestamp()

        # Create or get conversation between mentor and student
        existing_conversation = Conversation.query.join(ConversationParticipant).filter(
            ConversationParticipant.user_id.in_([user.user_id, request_obj.student_id]),
            Conversation.deleted_at.is_(None)
        ).group_by(Conversation.conversation_id).having(
            db.func.count(ConversationParticipant.participant_id) == 2
        ).first()

        if not existing_conversation:
            # Create new conversation
            conversation = Conversation()
            conversation.save()

            # Add mentor participant
            ConversationParticipant(
                conversation_id=conversation.conversation_id,
                user_id=user.user_id
            ).save()

            # Add student participant
            ConversationParticipant(
                conversation_id=conversation.conversation_id,
                user_id=request_obj.student_id
            ).save()

            conversation_id = conversation.conversation_id
        else:
            conversation_id = existing_conversation.conversation_id

        # Send message to student
        mentor_name = user.mentor_profile.full_name
        if data['status'] == 'accepted':
            message_text = f"Great news! I've accepted your mentorship request. I'm excited to work with you and help you grow in your career. Let's schedule our first session soon!"
        else:
            message_text = f"Thank you for your interest in mentorship. Unfortunately, I'm unable to take on new mentees at this time due to my current commitments. I wish you the best in finding a mentor who can support your goals!"

        message = Message(
            conversation_id=conversation_id,
            sender_id=user.user_id,
            message_text=message_text
        )
        message.save()

        db.session.commit()

        return success_response(
            data=request_obj.to_dict(),
            message=f'Request {data["status"]} and message sent to student'
        )

    except Exception as e:
        db.session.rollback()
        return error_response(f'Failed to respond: {str(e)}', status=500)


@mentors_bp.route('/sessions/my', methods=['GET'])
@token_required
def get_my_sessions():
    """Get my mentorship sessions"""
    user = get_current_user()

    if user.user_type == 'student':
        query = MentorshipSession.query.filter_by(
            student_id=user.student_profile.student_id,
            deleted_at=None
        )
    elif user.user_type == 'mentor':
        query = MentorshipSession.query.filter_by(
            mentor_id=user.mentor_profile.mentor_id,
            deleted_at=None
        )
    else:
        return error_response('Only students and mentors can access this endpoint', status=403)

    query = query.order_by(MentorshipSession.scheduled_at.desc())
    result = paginate(query)
    return success_response(data=result)


@mentors_bp.route('/sessions/<session_id>/review', methods=['POST'])
@token_required
@user_type_required('student')
def review_session(session_id):
    """Review a mentorship session"""
    user = get_current_user()
    data = request.get_json()

    valid, error = validate_required_fields(data, ['rating'])
    if not valid:
        return error_response(error, status=400)

    rating = int(data['rating'])
    if rating < 1 or rating > 5:
        return error_response('Rating must be between 1 and 5', status=400)

    session = MentorshipSession.query.filter_by(
        session_id=session_id,
        student_id=user.student_profile.student_id,
        status='completed',
        deleted_at=None
    ).first()

    if not session:
        return error_response('Session not found or not completed', status=404)

    # Check if already reviewed
    existing = MentorshipReview.query.filter_by(
        session_id=session_id,
        deleted_at=None
    ).first()

    if existing:
        return error_response('Session already reviewed', status=409)

    try:
        review = MentorshipReview(
            session_id=session_id,
            student_id=user.student_profile.student_id,
            mentor_id=session.mentor_id,
            rating=rating,
            review_text=data.get('review_text')
        )
        review.save()

        return success_response(message='Review submitted successfully', status=201)

    except Exception as e:
        db.session.rollback()
        return error_response(f'Failed to submit review: {str(e)}', status=500)


@mentors_bp.route('/recommendations', methods=['GET'])
@token_required
@user_type_required('student')
def get_recommended_mentors():
    """Get AI-matched mentor recommendations"""
    user = get_current_user()
    student = user.student_profile

    from app.services.ai_matching import get_recommended_mentors

    limit = request.args.get('limit', 10, type=int)
    recommendations = get_recommended_mentors(student, limit=limit)

    return success_response(data=recommendations, message=f'Found {len(recommendations)} recommended mentors')
