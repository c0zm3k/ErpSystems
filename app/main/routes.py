from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.main import main_bp
from app.models import db, Timetable, Staff

@main_bp.route('/')
def home():
    """Home page"""
    if current_user.is_authenticated:
        if current_user.role == 'admin':
            return redirect(url_for('admin.dashboard'))
        elif current_user.role == 'faculty':
            return redirect(url_for('faculty.dashboard'))
        elif current_user.role == 'student':
            return redirect(url_for('student.dashboard'))
    return redirect(url_for('auth.login'))

@main_bp.route('/timetable')
@login_required
def timetable():
    """View timetable"""
    if current_user.role == 'student':
        department = current_user.student.department
        semester = current_user.student.semester
    elif current_user.role == 'faculty':
        department = current_user.faculty.department
        semester = None
    else:
        department = None
        semester = None
    
    timetables = Timetable.query.all()
    
    if department:
        timetables = [t for t in timetables if t.department == department]
    
    # Group by day
    days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    timetables_by_day = {}
    for day in days_order:
        timetables_by_day[day] = [t for t in timetables if t.day_of_week == day]
    
    return render_template('timetable/timetable.html', timetables_by_day=timetables_by_day)

@main_bp.route('/staff')
@login_required
def staff_list():
    """View staff directory"""
    staff = Staff.query.all()
    return render_template('staff/staff_list.html', staff=staff)
