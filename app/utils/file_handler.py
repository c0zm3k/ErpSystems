from werkzeug.utils import secure_filename
from datetime import datetime
import os
import uuid

ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx'}

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_file_securely(file, upload_type='notes'):
    """
    Save file securely with validation
    
    Args:
        file: File object from request.files
        upload_type: 'notes' or 'certificates'
    
    Returns:
        Tuple of (file_path, file_name) or (None, None) if failed
    """
    if not file or file.filename == '':
        return None, None
    
    if not allowed_file(file.filename):
        return None, None
    
    filename = secure_filename(file.filename)
    # Add UUID to prevent filename conflicts
    file_ext = filename.rsplit('.', 1)[1].lower()
    unique_filename = f"{uuid.uuid4()}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.{file_ext}"
    
    # Determine upload path
    from flask import current_app
    upload_path = os.path.join(
        current_app.config['UPLOAD_FOLDER'],
        upload_type,
        unique_filename
    )
    
    try:
        os.makedirs(os.path.dirname(upload_path), exist_ok=True)
        file.save(upload_path)
        return upload_path, unique_filename
    except Exception as e:
        print(f"File save error: {e}")
        return None, None

def delete_file(file_path):
    """Safely delete a file"""
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
    except Exception as e:
        print(f"File delete error: {e}")
    return False
