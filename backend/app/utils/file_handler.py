"""
File handling utilities
"""
import os
import uuid
from werkzeug.utils import secure_filename
from flask import current_app, url_for
from PIL import Image


def save_file(file, category='general', resize_image=None):
    """
    Save uploaded file to local storage

    Args:
        file: FileStorage object from request.files
        category: Category folder (profile, resume, logo, course, attachment)
        resize_image: Tuple of (width, height) to resize images

    Returns:
        dict: {success: bool, file_path: str, file_id: str, error: str}
    """
    try:
        if not file:
            return {'success': False, 'error': 'No file provided'}

        # Validate file
        filename = secure_filename(file.filename)
        if not filename:
            return {'success': False, 'error': 'Invalid filename'}

        # Get file extension
        ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
        if ext not in current_app.config.get('ALLOWED_EXTENSIONS', set()):
            return {'success': False, 'error': f'File extension .{ext} not allowed'}

        # Generate unique file ID
        file_id = str(uuid.uuid4())
        new_filename = f"{file_id}.{ext}"

        # Create category folder if it doesn't exist
        upload_folder = current_app.config.get('UPLOAD_FOLDER', './uploads')
        category_path = os.path.join(upload_folder, category)
        os.makedirs(category_path, exist_ok=True)

        # Full file path
        file_path = os.path.join(category_path, new_filename)

        # Save file
        file.save(file_path)

        # Resize image if needed
        if resize_image and ext in ['jpg', 'jpeg', 'png', 'gif']:
            try:
                with Image.open(file_path) as img:
                    img.thumbnail(resize_image, Image.Resampling.LANCZOS)
                    img.save(file_path)
            except Exception as e:
                print(f"Error resizing image: {e}")

        # Return relative path for database storage
        relative_path = f"/uploads/{category}/{new_filename}"

        return {
            'success': True,
            'file_path': relative_path,
            'file_id': file_id,
            'filename': new_filename,
            'original_filename': filename,
            'size': os.path.getsize(file_path)
        }

    except Exception as e:
        return {'success': False, 'error': str(e)}


def delete_file(file_path):
    """
    Delete file from local storage

    Args:
        file_path: Relative file path (e.g., /uploads/profiles/abc123.jpg)

    Returns:
        bool: True if deleted successfully
    """
    try:
        if not file_path:
            return False

        # Remove leading slash if present
        if file_path.startswith('/'):
            file_path = file_path[1:]

        full_path = os.path.join(os.getcwd(), file_path)

        if os.path.exists(full_path):
            os.remove(full_path)
            return True
        return False

    except Exception as e:
        print(f"Error deleting file: {e}")
        return False


def get_file_url(file_path):
    """
    Get full URL for file

    Args:
        file_path: Relative file path

    Returns:
        str: Full URL to file
    """
    if not file_path:
        return None

    # If it's already a full URL, return as is
    if file_path.startswith('http://') or file_path.startswith('https://'):
        return file_path

    # Otherwise, construct URL
    app_url = current_app.config.get('APP_URL', 'http://localhost:5000')
    return f"{app_url}{file_path}"


def allowed_file(filename, allowed_extensions=None):
    """Check if file extension is allowed"""
    if not filename or '.' not in filename:
        return False

    ext = filename.rsplit('.', 1)[1].lower()

    if allowed_extensions is None:
        allowed_extensions = current_app.config.get('ALLOWED_EXTENSIONS', set())

    return ext in allowed_extensions
