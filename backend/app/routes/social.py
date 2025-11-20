"""
Social Feed Routes
"""
from flask import Blueprint, request
from app.utils.auth import token_required, get_current_user
from app.utils.helpers import success_response, error_response, paginate
from app.utils.validators import validate_required_fields
from app.models.all_models import Post, PostLike, PostComment
from app.extensions import db

social_bp = Blueprint('social', __name__)


@social_bp.route('/feed', methods=['GET'])
@token_required
def get_feed():
    """Get social feed (posts)"""
    query = Post.query.filter_by(deleted_at=None).order_by(Post.created_at.desc())

    # Filter by post type
    if 'type' in request.args:
        query = query.filter_by(post_type=request.args['type'])

    result = paginate(query)
    return success_response(data=result)


@social_bp.route('/posts', methods=['POST'])
@token_required
def create_post():
    """Create a post"""
    user = get_current_user()
    data = request.get_json()

    valid, error = validate_required_fields(data, ['content', 'post_type'])
    if not valid:
        return error_response(error, status=400)

    valid_types = ['job', 'mentor', 'general', 'achievement']
    if data['post_type'] not in valid_types:
        return error_response(f'Invalid post_type. Must be one of: {", ".join(valid_types)}', status=400)

    try:
        post = Post(
            author_id=user.user_id,
            content=data['content'],
            post_type=data['post_type'],
            related_job_id=data.get('related_job_id'),
            related_mentor_id=data.get('related_mentor_id')
        )
        post.save()

        return success_response(data={'post_id': post.post_id}, message='Post created successfully', status=201)

    except Exception as e:
        db.session.rollback()
        return error_response(f'Failed to create post: {str(e)}', status=500)


@social_bp.route('/posts/<post_id>', methods=['GET'])
@token_required
def get_post(post_id):
    """Get single post"""
    post = Post.query.filter_by(post_id=post_id, deleted_at=None).first()
    if not post:
        return error_response('Post not found', status=404)

    data = {
        'post_id': post.post_id,
        'author_id': post.author_id,
        'content': post.content,
        'post_type': post.post_type,
        'likes_count': post.likes_count,
        'comments_count': post.comments_count,
        'created_at': post.created_at.isoformat() if post.created_at else None
    }

    return success_response(data=data)


@social_bp.route('/posts/<post_id>', methods=['DELETE'])
@token_required
def delete_post(post_id):
    """Delete a post"""
    user = get_current_user()

    post = Post.query.filter_by(
        post_id=post_id,
        author_id=user.user_id,
        deleted_at=None
    ).first()

    if not post:
        return error_response('Post not found or unauthorized', status=404)

    post.soft_delete()
    return success_response(message='Post deleted successfully')


@social_bp.route('/posts/<post_id>/like', methods=['POST'])
@token_required
def like_post(post_id):
    """Like a post"""
    user = get_current_user()

    post = Post.query.filter_by(post_id=post_id, deleted_at=None).first()
    if not post:
        return error_response('Post not found', status=404)

    # Check if already liked
    existing = PostLike.query.filter_by(
        post_id=post_id,
        user_id=user.user_id,
        deleted_at=None
    ).first()

    if existing:
        return error_response('Already liked this post', status=409)

    try:
        like = PostLike(
            post_id=post_id,
            user_id=user.user_id
        )
        like.save()

        return success_response(message='Post liked successfully', status=201)

    except Exception as e:
        db.session.rollback()
        return error_response(f'Failed to like post: {str(e)}', status=500)


@social_bp.route('/posts/<post_id>/unlike', methods=['DELETE'])
@token_required
def unlike_post(post_id):
    """Unlike a post"""
    user = get_current_user()

    like = PostLike.query.filter_by(
        post_id=post_id,
        user_id=user.user_id,
        deleted_at=None
    ).first()

    if not like:
        return error_response('Like not found', status=404)

    like.soft_delete()
    return success_response(message='Post unliked successfully')


@social_bp.route('/posts/<post_id>/comments', methods=['GET'])
@token_required
def get_post_comments(post_id):
    """Get comments for a post"""
    post = Post.query.filter_by(post_id=post_id, deleted_at=None).first()
    if not post:
        return error_response('Post not found', status=404)

    query = PostComment.query.filter_by(
        post_id=post_id,
        deleted_at=None
    ).order_by(PostComment.created_at.desc())

    result = paginate(query)
    return success_response(data=result)


@social_bp.route('/posts/<post_id>/comments', methods=['POST'])
@token_required
def add_comment(post_id):
    """Add a comment to a post"""
    user = get_current_user()
    data = request.get_json()

    valid, error = validate_required_fields(data, ['comment_text'])
    if not valid:
        return error_response(error, status=400)

    post = Post.query.filter_by(post_id=post_id, deleted_at=None).first()
    if not post:
        return error_response('Post not found', status=404)

    try:
        comment = PostComment(
            post_id=post_id,
            user_id=user.user_id,
            comment_text=data['comment_text']
        )
        comment.save()

        return success_response(message='Comment added successfully', status=201)

    except Exception as e:
        db.session.rollback()
        return error_response(f'Failed to add comment: {str(e)}', status=500)


@social_bp.route('/comments/<comment_id>', methods=['DELETE'])
@token_required
def delete_comment(comment_id):
    """Delete a comment"""
    user = get_current_user()

    comment = PostComment.query.filter_by(
        comment_id=comment_id,
        user_id=user.user_id,
        deleted_at=None
    ).first()

    if not comment:
        return error_response('Comment not found or unauthorized', status=404)

    comment.soft_delete()
    return success_response(message='Comment deleted successfully')
