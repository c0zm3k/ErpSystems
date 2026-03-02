from flask import Flask
from flask_login import LoginManager
from app.config import config
from app.models import db, User
import os

login_manager = LoginManager()

def create_app(config_name='development'):
    """Flask application factory"""
    app = Flask(__name__, 
                template_folder='../templates',
                static_folder='../static')
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in first.'
    login_manager.login_message_category = 'info'
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Create upload folder if it doesn't exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'notes'), exist_ok=True)
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'certificates'), exist_ok=True)
    
    # Register blueprints
    from app.auth import auth_bp
    from app.main import main_bp
    from app.student import student_bp
    from app.faculty import faculty_bp
    from app.admin import admin_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(student_bp)
    app.register_blueprint(faculty_bp)
    app.register_blueprint(admin_bp)
    
    # Create database tables
    with app.app_context():
        db.create_all()
        _create_default_users()
    
    return app

def _create_default_users():
    """Create default admin, faculty, and student users if they don't exist"""
    from app.models import User, Student, Faculty
    
    # Default admin
    if not User.query.filter_by(username='admin').first():
        admin = User(
            username='admin',
            email='admin@erp.edu',
            role='admin',
            is_active=True
        )
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
    
    # Default faculty
    if not User.query.filter_by(username='faculty').first():
        faculty_user = User(
            username='faculty',
            email='faculty@erp.edu',
            role='faculty',
            is_active=True
        )
        faculty_user.set_password('faculty123')
        db.session.add(faculty_user)
        db.session.commit()
        
        faculty = Faculty(
            user_id=faculty_user.id,
            designation='Assistant Professor',
            department='Computer Science',
            phone='9876543210'
        )
        db.session.add(faculty)
        db.session.commit()
    
    # Default student
    if not User.query.filter_by(username='student').first():
        student_user = User(
            username='student',
            email='student@erp.edu',
            role='student',
            is_active=True
        )
        student_user.set_password('student123')
        db.session.add(student_user)
        db.session.commit()
        
        student = Student(
            user_id=student_user.id,
            roll_no='CS2024001',
            department='Computer Science',
            semester=4,
            phone='9123456789'
        )
        db.session.add(student)
        db.session.commit()
