from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.student import student_bp
from app.models import db, Attendance, Leave, Fee, Note, Certificate
from datetime import datetime, timedelta
from sqlalchemy import func

@student_bp.route('/dashboard')
@login_required
def dashboard():
    """Student dashboard"""
    if current_user.role != 'student':
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('auth.login'))
    
    student = current_user.student
    
    # Attendance stats
    today = datetime.utcnow().date()
    thirty_days_ago = today - timedelta(days=30)
    
    attendance_records = Attendance.query.filter(
        Attendance.student_id == student.id,
        Attendance.date >= thirty_days_ago
    ).all()
    
    total_days = len(attendance_records)
    present_days = len([a for a in attendance_records if a.status == 'present'])
    attendance_percentage = (present_days / total_days * 100) if total_days > 0 else 0
    
    # Fee details
    fees = Fee.query.filter_by(student_id=student.id).all()
    total_fees = sum(f.amount for f in fees)
    pending_fees = sum(f.amount for f in fees if f.status == 'pending')
    
    # Leave status
    leaves = Leave.query.filter_by(user_id=current_user.id).all()
    pending_leaves = len([l for l in leaves if l.status == 'pending'])
    approved_leaves = len([l for l in leaves if l.status == 'approved'])
    
    # Available certificates
    certificates = Certificate.query.filter_by(student_id=student.id).all()
    
    # Available notes
    notes = Note.query.all()
    
    return render_template('dashboard/student_dashboard.html',
                         student=student,
                         attendance_percentage=round(attendance_percentage, 2),
                         fees=fees,
                         total_fees=total_fees,
                         pending_fees=pending_fees,
                         pending_leaves=pending_leaves,
                         approved_leaves=approved_leaves,
                         certificates=certificates,
                         notes=notes)

@student_bp.route('/attendance')
@login_required
def view_attendance():
    """View student attendance"""
    if current_user.role != 'student':
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('auth.login'))
    
    student = current_user.student
    page = request.args.get('page', 1, type=int)
    
    attendance_records = Attendance.query.filter_by(student_id=student.id)\
        .order_by(Attendance.date.desc())\
        .paginate(page=page, per_page=10)
    
    return render_template('attendance/view_attendance.html', attendance=attendance_records)

@student_bp.route('/fees')
@login_required
def fees():
    """View fees"""
    if current_user.role != 'student':
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('auth.login'))
    
    student = current_user.student
    fee_records = Fee.query.filter_by(student_id=student.id).all()
    
    total_amount = sum(f.amount for f in fee_records)
    paid_amount = sum(f.amount for f in fee_records if f.status == 'paid')
    pending_amount = total_amount - paid_amount
    
    return render_template('fees/fees.html',
                         fees=fee_records,
                         total_amount=total_amount,
                         paid_amount=paid_amount,
                         pending_amount=pending_amount)

@student_bp.route('/apply-leave', methods=['GET', 'POST'])
@login_required
def apply_leave():
    """Apply for leave"""
    if current_user.role != 'student':
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        reason = request.form.get('reason', '').strip()
        
        if not start_date or not end_date or not reason:
            flash('All fields are required.', 'danger')
            return redirect(url_for('student.apply_leave'))
        
        try:
            start = datetime.strptime(start_date, '%Y-%m-%d').date()
            end = datetime.strptime(end_date, '%Y-%m-%d').date()
            
            if start >= end:
                flash('End date must be after start date.', 'danger')
                return redirect(url_for('student.apply_leave'))
            
            leave = Leave(
                user_id=current_user.id,
                start_date=start,
                end_date=end,
                reason=reason,
                status='pending'
            )
            db.session.add(leave)
            db.session.commit()
            
            flash('Leave application submitted successfully.', 'success')
            return redirect(url_for('student.my_leaves'))
        except ValueError:
            flash('Invalid date format.', 'danger')
    
    return render_template('leave/apply_leave.html')

@student_bp.route('/my-leaves')
@login_required
def my_leaves():
    """View my leave applications"""
    if current_user.role != 'student':
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('auth.login'))
    
    leaves = Leave.query.filter_by(user_id=current_user.id)\
        .order_by(Leave.applied_at.desc()).all()
    
    return render_template('leave/student_leaves.html', leaves=leaves)

@student_bp.route('/notes')
@login_required
def view_notes():
    """View study notes"""
    if current_user.role != 'student':
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('auth.login'))
    
    student = current_user.student
    
    # Get notes for student's department and semester
    notes = Note.query.filter(
        (Note.department == student.department) |
        (Note.semester == student.semester) |
        (Note.department == None)
    ).order_by(Note.upload_date.desc()).all()
    
    return render_template('notes/view_notes.html', notes=notes)

@student_bp.route('/certificates')
@login_required
def certificates():
    """Download certificates"""
    if current_user.role != 'student':
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('auth.login'))
    
    student = current_user.student
    certificates = Certificate.query.filter_by(student_id=student.id).all()
    
    return render_template('certificates/download_cert.html', certificates=certificates)
