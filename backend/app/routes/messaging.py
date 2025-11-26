"""
Messaging Routes (REST API for conversations)
Real-time messaging handled by WebSockets
"""
from flask import Blueprint, request
from app.utils.auth import token_required, get_current_user
from app.utils.helpers import success_response, error_response, paginate
from app.utils.validators import validate_required_fields
from app.models.all_models import Conversation, ConversationParticipant, Message
from app.extensions import db

messaging_bp = Blueprint('messaging', __name__)


@messaging_bp.route('/conversations', methods=['GET'])
@token_required
def get_conversations():
    """Get my conversations"""
    from app.models.user import User
    from app.models.student import StudentProfile
    from app.models.all_models import EmployerProfile

    user = get_current_user()
    print(f"[DEBUG get_conversations] User ID: {user.user_id}")

    # Get conversations where user is participant
    conversations = Conversation.query.join(ConversationParticipant).filter(
        ConversationParticipant.user_id == user.user_id,
        ConversationParticipant.deleted_at.is_(None),
        Conversation.deleted_at.is_(None)
    ).order_by(Conversation.updated_at.desc()).all()

    print(f"[DEBUG get_conversations] Found {len(conversations)} conversations")

    # Manually build conversation list with participant info
    conversations_data = []
    for conv in conversations:
        # Get all participants except current user
        participants = ConversationParticipant.query.filter_by(
            conversation_id=conv.conversation_id,
            deleted_at=None
        ).all()

        print(f"[DEBUG] Conversation {conv.conversation_id} has {len(participants)} participants")

        # Get the other participant (not current user)
        other_participants = []
        for p in participants:
            if p.user_id != user.user_id:
                participant_user = User.query.get(p.user_id)
                if participant_user:
                    # Get profile info based on user type
                    profile_info = {}
                    if participant_user.user_type == 'student':
                        student_profile = StudentProfile.query.filter_by(student_id=participant_user.user_id).first()
                        if student_profile:
                            profile_info = {
                                'full_name': student_profile.full_name,
                                'profile_picture_url': student_profile.profile_picture
                            }
                    elif participant_user.user_type == 'employer':
                        employer_profile = EmployerProfile.query.filter_by(employer_id=participant_user.user_id).first()
                        if employer_profile:
                            profile_info = {
                                'full_name': employer_profile.company_name,
                                'profile_picture_url': employer_profile.company_logo
                            }

                    other_participants.append({
                        'user_id': participant_user.user_id,
                        'email': participant_user.email,
                        'user_type': participant_user.user_type,
                        **profile_info
                    })

        # Get latest message
        latest_message = Message.query.filter_by(
            conversation_id=conv.conversation_id,
            deleted_at=None
        ).order_by(Message.sent_at.desc()).first()

        latest_message_data = None
        if latest_message:
            latest_message_data = {
                'message_id': latest_message.message_id,
                'message_text': latest_message.message_text,
                'sent_at': latest_message.sent_at.isoformat() if latest_message.sent_at else None,
                'sender_id': latest_message.sender_id
            }

        conversations_data.append({
            'conversation_id': conv.conversation_id,
            'created_at': conv.created_at.isoformat() if conv.created_at else None,
            'updated_at': conv.updated_at.isoformat() if conv.updated_at else None,
            'participants': other_participants,
            'latest_message': latest_message_data
        })

    print(f"[DEBUG get_conversations] Returning {len(conversations_data)} conversations")

    result = {
        'data': conversations_data,
        'meta': {
            'page': 1,
            'per_page': len(conversations_data),
            'total': len(conversations_data),
            'pages': 1
        }
    }

    return success_response(data=result)


@messaging_bp.route('/conversations/<conversation_id>', methods=['GET'])
@token_required
def get_conversation(conversation_id):
    """Get conversation details and messages"""
    from app.models.user import User
    from app.models.student import StudentProfile
    from app.models.all_models import EmployerProfile

    user = get_current_user()

    # Verify user is participant
    participant = ConversationParticipant.query.filter_by(
        conversation_id=conversation_id,
        user_id=user.user_id,
        deleted_at=None
    ).first()

    if not participant:
        return error_response('Conversation not found or unauthorized', status=404)

    conversation = Conversation.query.filter_by(
        conversation_id=conversation_id,
        deleted_at=None
    ).first()

    if not conversation:
        return error_response('Conversation not found', status=404)

    # Get messages
    messages_query = Message.query.filter_by(
        conversation_id=conversation_id,
        deleted_at=None
    ).order_by(Message.sent_at.asc())

    messages = [msg.to_dict() for msg in messages_query.all()]

    # Get participants with full details
    participants_query = ConversationParticipant.query.filter_by(
        conversation_id=conversation_id,
        deleted_at=None
    ).all()

    participants = []
    for p in participants_query:
        participant_user = User.query.get(p.user_id)
        if participant_user:
            # Get profile info based on user type
            profile_info = {}
            if participant_user.user_type == 'student':
                student_profile = StudentProfile.query.filter_by(student_id=participant_user.user_id).first()
                if student_profile:
                    profile_info = {
                        'full_name': student_profile.full_name,
                        'profile_picture_url': student_profile.profile_picture
                    }
            elif participant_user.user_type == 'employer':
                employer_profile = EmployerProfile.query.filter_by(employer_id=participant_user.user_id).first()
                if employer_profile:
                    profile_info = {
                        'full_name': employer_profile.company_name,
                        'profile_picture_url': employer_profile.company_logo
                    }

            participants.append({
                'user_id': participant_user.user_id,
                'email': participant_user.email,
                'user_type': participant_user.user_type,
                'joined_at': p.joined_at.isoformat() if p.joined_at else None,
                **profile_info
            })

    data = {
        'conversation_id': conversation.conversation_id,
        'created_at': conversation.created_at.isoformat() if conversation.created_at else None,
        'updated_at': conversation.updated_at.isoformat() if conversation.updated_at else None,
        'participants': participants,
        'messages': messages
    }

    return success_response(data=data)


@messaging_bp.route('/conversations', methods=['POST'])
@token_required
def create_conversation():
    """Create new conversation"""
    user = get_current_user()
    data = request.get_json()

    valid, error = validate_required_fields(data, ['participant_ids'])
    if not valid:
        return error_response(error, status=400)

    participant_ids = data['participant_ids']
    if not isinstance(participant_ids, list) or len(participant_ids) == 0:
        return error_response('participant_ids must be a non-empty array', status=400)

    # Add current user to participants if not included
    if user.user_id not in participant_ids:
        participant_ids.append(user.user_id)

    try:
        # Create conversation
        conversation = Conversation()
        conversation.save()

        # Add participants
        for participant_id in participant_ids:
            participant = ConversationParticipant(
                conversation_id=conversation.conversation_id,
                user_id=participant_id
            )
            participant.save()

        return success_response(
            data={'conversation_id': conversation.conversation_id},
            message='Conversation created successfully',
            status=201
        )

    except Exception as e:
        db.session.rollback()
        return error_response(f'Failed to create conversation: {str(e)}', status=500)


@messaging_bp.route('/conversations/<conversation_id>/messages', methods=['POST'])
@token_required
def send_message(conversation_id):
    """Send a message (REST endpoint, prefer WebSocket for real-time)"""
    user = get_current_user()
    data = request.get_json()

    valid, error = validate_required_fields(data, ['message_text'])
    if not valid:
        return error_response(error, status=400)

    # Verify user is participant
    participant = ConversationParticipant.query.filter_by(
        conversation_id=conversation_id,
        user_id=user.user_id,
        deleted_at=None
    ).first()

    if not participant:
        return error_response('Conversation not found or unauthorized', status=404)

    try:
        message = Message(
            conversation_id=conversation_id,
            sender_id=user.user_id,
            message_text=data['message_text'],
            attachment_url=data.get('attachment_url')
        )
        message.save()

        return success_response(
            data=message.to_dict(),
            message='Message sent successfully',
            status=201
        )

    except Exception as e:
        db.session.rollback()
        return error_response(f'Failed to send message: {str(e)}', status=500)


@messaging_bp.route('/conversations/<conversation_id>/mark-read', methods=['POST'])
@token_required
def mark_messages_read(conversation_id):
    """Mark all messages in conversation as read"""
    user = get_current_user()

    # Verify user is participant
    participant = ConversationParticipant.query.filter_by(
        conversation_id=conversation_id,
        user_id=user.user_id,
        deleted_at=None
    ).first()

    if not participant:
        return error_response('Conversation not found or unauthorized', status=404)

    try:
        # Mark all unread messages as read (except user's own messages)
        Message.query.filter(
            Message.conversation_id == conversation_id,
            Message.sender_id != user.user_id,
            Message.is_read == False,
            Message.deleted_at.is_(None)
        ).update({'is_read': True})

        # Update last_read_at
        participant.last_read_at = db.func.current_timestamp()
        db.session.commit()

        return success_response(message='Messages marked as read')

    except Exception as e:
        db.session.rollback()
        return error_response(f'Failed to mark messages as read: {str(e)}', status=500)


@messaging_bp.route('/unread-count', methods=['GET'])
@token_required
def get_unread_count():
    """Get total unread message count"""
    user = get_current_user()

    # Count unread messages in all user's conversations
    count = Message.query.join(ConversationParticipant).filter(
        ConversationParticipant.user_id == user.user_id,
        Message.sender_id != user.user_id,
        Message.is_read == False,
        Message.deleted_at.is_(None),
        ConversationParticipant.deleted_at.is_(None)
    ).count()

    return success_response(data={'unread_count': count})
