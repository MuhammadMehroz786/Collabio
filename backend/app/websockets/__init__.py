"""
WebSocket Event Handlers
"""
from flask_socketio import emit, join_room, leave_room
from flask_jwt_extended import decode_token
from app.extensions import socketio, db
from app.models.websocket import WebSocketSession
from app.models.messaging import Message


def register_socket_events(socketio_instance):
    """Register all WebSocket event handlers"""

    @socketio_instance.on('connect')
    def handle_connect(auth):
        """Handle client connection"""
        try:
            # Verify JWT token
            token = auth.get('token')
            if not token:
                return False

            decoded = decode_token(token)
            user_id = decoded['sub']

            # Create WebSocket session
            session = WebSocketSession(
                user_id=user_id,
                socket_id=request.sid
            )
            session.save()

            emit('connected', {'message': 'Successfully connected'})
            return True

        except Exception as e:
            print(f"Connection error: {e}")
            return False

    @socketio_instance.on('disconnect')
    def handle_disconnect():
        """Handle client disconnection"""
        try:
            session = WebSocketSession.query.filter_by(socket_id=request.sid).first()
            if session:
                session.is_online = False
                db.session.commit()

        except Exception as e:
            print(f"Disconnection error: {e}")

    @socketio_instance.on('join_conversation')
    def handle_join_conversation(data):
        """Join a conversation room"""
        try:
            conversation_id = data.get('conversation_id')
            if not conversation_id:
                emit('error', {'message': 'conversation_id required'})
                return

            join_room(conversation_id)
            emit('joined_conversation', {'conversation_id': conversation_id})

        except Exception as e:
            emit('error', {'message': str(e)})

    @socketio_instance.on('leave_conversation')
    def handle_leave_conversation(data):
        """Leave a conversation room"""
        try:
            conversation_id = data.get('conversation_id')
            if not conversation_id:
                return

            leave_room(conversation_id)
            emit('left_conversation', {'conversation_id': conversation_id})

        except Exception as e:
            emit('error', {'message': str(e)})

    @socketio_instance.on('send_message')
    def handle_send_message(data):
        """Send a message in a conversation"""
        try:
            conversation_id = data.get('conversation_id')
            message_text = data.get('message_text')

            if not conversation_id or not message_text:
                emit('error', {'message': 'conversation_id and message_text required'})
                return

            # Get sender from session
            session = WebSocketSession.query.filter_by(socket_id=request.sid, is_online=True).first()
            if not session:
                emit('error', {'message': 'Not authenticated'})
                return

            # Create message
            message = Message(
                conversation_id=conversation_id,
                sender_id=session.user_id,
                message_text=message_text,
                attachment_url=data.get('attachment_url')
            )
            message.save()

            # Broadcast to conversation room
            socketio_instance.emit(
                'new_message',
                message.to_dict(),
                room=conversation_id
            )

        except Exception as e:
            emit('error', {'message': str(e)})

    @socketio_instance.on('mark_read')
    def handle_mark_read(data):
        """Mark messages as read"""
        try:
            conversation_id = data.get('conversation_id')
            if not conversation_id:
                return

            session = WebSocketSession.query.filter_by(socket_id=request.sid, is_online=True).first()
            if not session:
                return

            # Mark all messages as read in this conversation
            messages = Message.query.filter_by(
                conversation_id=conversation_id,
                is_read=False,
                deleted_at=None
            ).filter(Message.sender_id != session.user_id).all()

            for msg in messages:
                msg.is_read = True

            db.session.commit()

            emit('messages_marked_read', {'conversation_id': conversation_id})

        except Exception as e:
            emit('error', {'message': str(e)})

    @socketio_instance.on('typing')
    def handle_typing(data):
        """Broadcast typing indicator"""
        try:
            conversation_id = data.get('conversation_id')
            is_typing = data.get('is_typing', False)

            if not conversation_id:
                return

            session = WebSocketSession.query.filter_by(socket_id=request.sid, is_online=True).first()
            if not session:
                return

            # Broadcast to conversation room
            socketio_instance.emit(
                'user_typing',
                {
                    'user_id': session.user_id,
                    'is_typing': is_typing
                },
                room=conversation_id,
                skip_sid=request.sid  # Don't send to sender
            )

        except Exception as e:
            pass  # Silently fail for typing indicators
