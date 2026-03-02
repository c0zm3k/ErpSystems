from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.auth import auth_bp
from app.models import db, User, Student, Faculty
from werkzeug.security import check_password_hash

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login route"""
    if current_user.is_authenticated:
        return redirect(_get_dashboard_url(current_user.role))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        remember = request.form.get('remember', False)
        
        if not username or not password:
            flash('Username and password are required.', 'danger')
            return redirect(url_for('auth.login'))
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            if not user.is_active:
                flash('Your account is inactive. Contact admin.', 'danger')
                return redirect(url_for('auth.login'))
            
            login_user(user, remember=remember)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            return redirect(_get_dashboard_url(user.role))
        else:
            flash('Invalid username or password.', 'danger')
    
    return render_template('auth/login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    """User logout route"""
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('auth.login'))

def _get_dashboard_url(role):
    """Get dashboard URL based on user role"""
    if role == 'admin':
        return url_for('admin.dashboard')
    elif role == 'faculty':
        return url_for('faculty.dashboard')
    elif role == 'student':
        return url_for('student.dashboard')
    else:
        return url_for('main.home')
