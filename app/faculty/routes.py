from flask import render_template, redirect, url_for, flash, request, send_file
from flask_login import login_required, current_user
from app.faculty import faculty_bp
from app.models import db, Attendance, Student, Note, Leave
from app.utils.file_handler import save_file_securely
from datetime import datetime
import os

@faculty_bp.route('/dashboard')
@login_required
def dashboard():
    """Faculty dashboard"""
    if current_user.role != 'faculty':
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('auth.login'))
    
    faculty = current_user.faculty
    
    # Get students in faculty's department
    students = Student.query.filter_by(department=faculty.department).all()
    
    # Pending leaves to review
    pending_leaves = Leave.query.filter_by(status='pending').all()
    
    # Notes uploaded
    notes = Note.query.filter_by(user_id=current_user.id).all()
    
    stats = {
        'total_students': len(students),
        'pending_leaves': len(pending_leaves),
        'notes_uploaded': len(notes)
    }
    
    return render_template('dashboard/faculty_dashboard.html',
                         faculty=faculty,
                         stats=stats,
                         students=students,
                         pending_leaves=pending_leaves)

@faculty_bp.route('/mark-attendance', methods=['GET', 'POST'])
@login_required
def mark_attendance():
    """Mark attendance for students"""
    if current_user.role != 'faculty':
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('auth.login'))
    
    faculty = current_user.faculty
    
    if request.method == 'POST':
        attendance_date = request.form.get('attendance_date')
        
        if not attendance_date:
            flash('Please select a date.', 'danger')
            return redirect(url_for('faculty.mark_attendance'))
        
        try:
            att_date = datetime.strptime(attendance_date, '%Y-%m-%d').date()
        except ValueError:
            flash('Invalid date format.', 'danger')
            return redirect(url_for('faculty.mark_attendance'))
        
        # Get all students in faculty's department
        students = Student.query.filter_by(department=faculty.department).all()
        
        for student in students:
            status = request.form.get(f'student_{student.id}', 'absent')
            
            # Check if attendance already exists
            existing = Attendance.query.filter_by(
                student_id=student.id,
                date=att_date
            ).first()
            
            if existing:
                existing.status = status
                existing.marked_by = current_user.username
            else:
                attendance = Attendance(
                    student_id=student.id,
                    date=att_date,
                    status=status,
                    marked_by=current_user.username
                )
                db.session.add(attendance)
        
        db.session.commit()
        flash(f'Attendance marked successfully for {att_date}.', 'success')
        return redirect(url_for('faculty.mark_attendance'))
    
    # Get students in department
    students = Student.query.filter_by(department=faculty.department).all()
    
    return render_template('attendance/mark_attendance.html', students=students)

@faculty_bp.route('/upload-notes', methods=['GET', 'POST'])
@login_required
def upload_notes():
    """Upload study notes"""
    if current_user.role != 'faculty':
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        subject = request.form.get('subject', '').strip()
        description = request.form.get('description', '').strip()
        semester = request.form.get('semester', type=int)
        
        if not title or not subject:
            flash('Title and subject are required.', 'danger')
            return redirect(url_for('faculty.upload_notes'))
        
        if 'file' not in request.files:
            flash('No file selected.', 'danger')
            return redirect(url_for('faculty.upload_notes'))
        
        file = request.files['file']
        
        if file.filename == '':
            flash('No file selected.', 'danger')
            return redirect(url_for('faculty.upload_notes'))
        
        file_path, file_name = save_file_securely(file, 'notes')
        
        if file_path:
            note = Note(
                user_id=current_user.id,
                title=title,
                subject=subject,
                description=description,
                file_path=file_path,
                file_name=file_name,
                department=current_user.faculty.department,
                semester=semester
            )
            db.session.add(note)
            db.session.commit()
            
            flash('Notes uploaded successfully.', 'success')
            return redirect(url_for('faculty.upload_notes'))
        else:
            flash('File upload failed.', 'danger')
    
    return render_template('notes/upload_notes.html')

@faculty_bp.route('/my-notes')
@login_required
def my_notes():
    """View uploaded notes"""
    if current_user.role != 'faculty':
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('auth.login'))
    
    notes = Note.query.filter_by(user_id=current_user.id)\
        .order_by(Note.upload_date.desc()).all()
    
    return render_template('notes/faculty_notes.html', notes=notes)

@faculty_bp.route('/delete-note/<int:note_id>', methods=['POST'])
@login_required
def delete_note(note_id):
    """Delete a note"""
    if current_user.role != 'faculty':
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('auth.login'))
    
    note = Note.query.get(note_id)
    
    if not note or note.user_id != current_user.id:
        flash('Note not found or unauthorized.', 'danger')
        return redirect(url_for('faculty.my_notes'))
    
    # Delete file
    if os.path.exists(note.file_path):
        os.remove(note.file_path)
    
    db.session.delete(note)
    db.session.commit()
    
    flash('Note deleted successfully.', 'success')
    return redirect(url_for('faculty.my_notes'))
@faculty_bp.route('/apply-leave', methods=['GET', 'POST'])
@login_required
def apply_leave():
    """Apply for leave"""
    if current_user.role != 'faculty':
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        reason = request.form.get('reason', '').strip()
        
        if not start_date or not end_date or not reason:
            flash('All fields are required.', 'danger')
            return redirect(url_for('faculty.apply_leave'))
        
        try:
            start = datetime.strptime(start_date, '%Y-%m-%d').date()
            end = datetime.strptime(end_date, '%Y-%m-%d').date()
            
            if start >= end:
                flash('End date must be after start date.', 'danger')
                return redirect(url_for('faculty.apply_leave'))
            
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
            return redirect(url_for('faculty.my_leaves'))
        except ValueError:
            flash('Invalid date format.', 'danger')
    
    return render_template('leave/apply_leave.html')

@faculty_bp.route('/my-leaves')
@login_required
def my_leaves():
    """View my leave applications"""
    if current_user.role != 'faculty':
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('auth.login'))
    
    leaves = Leave.query.filter_by(user_id=current_user.id)\
        .order_by(Leave.applied_at.desc()).all()
    
    return render_template('leave/faculty_leaves.html', leaves=leaves)