from flask import Blueprint

faculty_bp = Blueprint('faculty', __name__, url_prefix='/faculty', template_folder='../templates')

from app.faculty import routes
