from flask import render_template, redirect, url_for, flash, request, send_file
from flask_login import login_required, current_user
from app.admin import admin_bp
from app.models import db, User, Student, Faculty, Leave, Certificate, Timetable, Staff, Note, Fee, Attendance
from app.utils.file_handler import save_file_securely
from datetime import datetime
import os

@admin_bp.route('/dashboard')
@login_required
def dashboard():
    """Admin dashboard"""
    if current_user.role != 'admin':
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('auth.login'))
    
    stats = {
        'total_students': Student.query.count(),
        'total_faculty': Faculty.query.count(),
        'total_users': User.query.count(),
        'pending_leaves': Leave.query.filter_by(status='pending').count(),
        'pending_fees': Fee.query.filter_by(status='pending').count()
    }
    
    pending_leaves = Leave.query.filter_by(status='pending').all()
    
    return render_template('dashboard/admin_dashboard.html',
                         stats=stats,
                         pending_leaves=pending_leaves)

@admin_bp.route('/users')
@login_required
def users():
    """Manage users"""
    if current_user.role != 'admin':
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('auth.login'))
    
    page = request.args.get('page', 1, type=int)
    role_filter = request.args.get('role', 'all')
    
    query = User.query
    if role_filter != 'all':
        query = query.filter_by(role=role_filter)
    
    users = query.paginate(page=page, per_page=10)
    
    return render_template('admin/users.html', users=users, role_filter=role_filter)

@admin_bp.route('/students')
@login_required
def students():
    """Manage students"""
    if current_user.role != 'admin':
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('auth.login'))
    
    page = request.args.get('page', 1, type=int)
    dept_filter = request.args.get('department', 'all')
    
    query = Student.query
    if dept_filter != 'all':
        query = query.filter_by(department=dept_filter)
    
    students = query.paginate(page=page, per_page=10)
    
    departments = db.session.query(Student.department).distinct().all()
    departments = [d[0] for d in departments]
    
    return render_template('admin/students.html', 
                         students=students,
                         dept_filter=dept_filter,
                         departments=departments)

@admin_bp.route('/manage-leaves', methods=['GET', 'POST'])
@login_required
def manage_leaves():
    """Approve/Reject leave applications"""
    if current_user.role != 'admin':
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('auth.login'))
    
    page = request.args.get('page', 1, type=int)
    status_filter = request.args.get('status', 'pending')
    
    query = Leave.query
    if status_filter != 'all':
        query = query.filter_by(status=status_filter)
    
    leaves = query.paginate(page=page, per_page=10)
    
    return render_template('leave/manage_leave.html', leaves=leaves, status_filter=status_filter)

@admin_bp.route('/approve-leave/<int:leave_id>', methods=['POST'])
@login_required
def approve_leave(leave_id):
    """Approve leave"""
    if current_user.role != 'admin':
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('auth.login'))
    
    leave = Leave.query.get(leave_id)
    
    if not leave:
        flash('Leave not found.', 'danger')
        return redirect(url_for('admin.manage_leaves'))
    
    leave.status = 'approved'
    leave.resolved_by = current_user.username
    leave.resolved_at = datetime.utcnow()
    db.session.commit()
    
    flash('Leave approved.', 'success')
    return redirect(url_for('admin.manage_leaves'))

@admin_bp.route('/reject-leave/<int:leave_id>', methods=['POST'])
@login_required
def reject_leave(leave_id):
    """Reject leave"""
    if current_user.role != 'admin':
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('auth.login'))
    
    leave = Leave.query.get(leave_id)
    remarks = request.form.get('remarks', '')
    
    if not leave:
        flash('Leave not found.', 'danger')
        return redirect(url_for('admin.manage_leaves'))
    
    leave.status = 'rejected'
    leave.remarks = remarks
    leave.resolved_by = current_user.username
    leave.resolved_at = datetime.utcnow()
    db.session.commit()
    
    flash('Leave rejected.', 'success')
    return redirect(url_for('admin.manage_leaves'))

@admin_bp.route('/upload-certificate', methods=['GET', 'POST'])
@login_required
def upload_certificate():
    """Upload certificate for student"""
    if current_user.role != 'admin':
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        student_id = request.form.get('student_id', type=int)
        cert_type = request.form.get('certificate_type', '').strip()
        issue_date = request.form.get('issue_date')
        description = request.form.get('description', '').strip()
        
        if not student_id or not cert_type:
            flash('Student and certificate type are required.', 'danger')
            return redirect(url_for('admin.upload_certificate'))
        
        if 'file' not in request.files:
            flash('No file selected.', 'danger')
            return redirect(url_for('admin.upload_certificate'))
        
        file = request.files['file']
        
        if file.filename == '':
            flash('No file selected.', 'danger')
            return redirect(url_for('admin.upload_certificate'))
        
        student = Student.query.get(student_id)
        if not student:
            flash('Student not found.', 'danger')
            return redirect(url_for('admin.upload_certificate'))
        
        file_path, file_name = save_file_securely(file, 'certificates')
        
        if file_path:
            try:
                issue_dt = datetime.strptime(issue_date, '%Y-%m-%d').date() if issue_date else None
            except ValueError:
                issue_dt = None
            
            certificate = Certificate(
                user_id=current_user.id,
                student_id=student_id,
                certificate_type=cert_type,
                file_path=file_path,
                file_name=file_name,
                issue_date=issue_dt,
                description=description
            )
            db.session.add(certificate)
            db.session.commit()
            
            flash('Certificate uploaded successfully.', 'success')
            return redirect(url_for('admin.upload_certificate'))
        else:
            flash('File upload failed.', 'danger')
    
    students = Student.query.all()
    
    return render_template('certificates/upload_cert.html', students=students)

@admin_bp.route('/manage-timetable')
@login_required
def manage_timetable():
    """Manage timetable"""
    if current_user.role != 'admin':
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('auth.login'))
    
    timetables = Timetable.query.all()
    
    return render_template('admin/manage_timetable.html', timetables=timetables)

@admin_bp.route('/add-timetable', methods=['GET', 'POST'])
@login_required
def add_timetable():
    """Add timetable entry"""
    if current_user.role != 'admin':
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        department = request.form.get('department', '').strip()
        semester = request.form.get('semester', type=int)
        day_of_week = request.form.get('day_of_week', '').strip()
        start_time = request.form.get('start_time', '').strip()
        end_time = request.form.get('end_time', '').strip()
        subject = request.form.get('subject', '').strip()
        faculty_name = request.form.get('faculty_name', '').strip()
        room_no = request.form.get('room_no', '').strip()
        
        if not all([department, semester, day_of_week, start_time, end_time, subject]):
            flash('All fields are required.', 'danger')
            return redirect(url_for('admin.add_timetable'))
        
        timetable = Timetable(
            department=department,
            semester=semester,
            day_of_week=day_of_week,
            start_time=start_time,
            end_time=end_time,
            subject=subject,
            faculty_name=faculty_name,
            room_no=room_no
        )
        
        db.session.add(timetable)
        db.session.commit()
        
        flash('Timetable entry added successfully.', 'success')
        return redirect(url_for('admin.manage_timetable'))
    
    faculties = Faculty.query.all()
    departments = ['CS', 'EC', 'ME', 'CE', 'IT']
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    semesters = [1, 2, 3, 4, 5, 6, 7, 8]
    
    return render_template('admin/add_timetable.html', 
                         faculties=faculties,
                         departments=departments,
                         days=days,
                         semesters=semesters)

@admin_bp.route('/manage-timetable')
@login_required
def manage_staff():
    """Manage staff"""
    if current_user.role != 'admin':
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('auth.login'))
    
    staff = Staff.query.all()
    
    return render_template('admin/manage_staff.html', staff=staff)

@admin_bp.route('/add-staff', methods=['GET', 'POST'])
@login_required
def add_staff():
    """Add new staff member"""
    if current_user.role != 'admin':
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        designation = request.form.get('designation', '').strip()
        department = request.form.get('department', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        office = request.form.get('office', '').strip()
        
        if not name or not designation or not department:
            flash('Name, designation, and department are required.', 'danger')
            return redirect(url_for('admin.add_staff'))
        
        staff = Staff(
            name=name,
            designation=designation,
            department=department,
            email=email,
            phone=phone,
            office=office
        )
        db.session.add(staff)
        db.session.commit()
        
        flash('Staff member added successfully.', 'success')
        return redirect(url_for('admin.manage_staff'))
    
    return render_template('admin/add_staff.html')

@admin_bp.route('/delete-staff/<int:staff_id>', methods=['POST'])
@login_required
def delete_staff(staff_id):
    """Delete staff member"""
    if current_user.role != 'admin':
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('auth.login'))
    
    staff = Staff.query.get(staff_id)
    
    if not staff:
        flash('Staff not found.', 'danger')
        return redirect(url_for('admin.manage_staff'))
    
    db.session.delete(staff)
    db.session.commit()
    
    flash('Staff member deleted.', 'success')
    return redirect(url_for('admin.manage_staff'))
