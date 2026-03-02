from flask import Blueprint

student_bp = Blueprint('student', __name__, url_prefix='/student', template_folder='../templates')

from app.student import routes
