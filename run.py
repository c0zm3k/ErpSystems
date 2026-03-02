import os
from app import create_app, db
from app.models import User, Student, Faculty, Attendance, Leave, Fee, Note, Certificate, Timetable, Staff

app = create_app(os.getenv('FLASK_ENV', 'development'))

@app.shell_context_processor
def make_shell_context():
    """Create shell context for Flask CLI"""
    return {
        'db': db,
        'User': User,
        'Student': Student,
        'Faculty': Faculty,
        'Attendance': Attendance,
        'Leave': Leave,
        'Fee': Fee,
        'Note': Note,
        'Certificate': Certificate,
        'Timetable': Timetable,
        'Staff': Staff
    }

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5500)
