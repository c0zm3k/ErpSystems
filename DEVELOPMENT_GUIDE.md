# Development Guide - College ERP System

This guide helps developers extend and customize the College ERP system.

---

## 🛠️ Development Environment Setup

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Git
- Code Editor (VS Code, PyCharm, etc.)
- SQLite Viewer (optional)

### Setup Virtual Environment
```bash
cd e:\CSSD\ErpSystem

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt
```

### Running Development Server
```bash
# With auto-reload on code changes
python run.py

# Server runs on http://localhost:5000
# Debugger PIN shown in console
```

---

## 📁 Project Structure & Organization

### App Package (`app/`)
```
app/
├── __init__.py              # Flask app factory
├── config.py               # Configuration
├── models.py               # Database models
├── auth/                   # Authentication
├── main/                   # Main routes
├── student/                # Student features
├── faculty/                # Faculty features
├── admin/                  # Admin features
└── utils/                  # Utilities
```

### Blueprint Pattern
Each module (auth, student, faculty, admin) is a Blueprint:

```python
# In app/student/__init__.py
from flask import Blueprint
student_bp = Blueprint('student', __name__, url_prefix='/student')
from app.student import routes

# In app/student/routes.py
from app.student import student_bp

@student_bp.route('/dashboard')
def dashboard():
    return render_template('dashboard/student_dashboard.html')
```

---

## 🗄️ Working with Database

### Models Location
All models are in `app/models.py`

### Creating a New Model
```python
# In app/models.py
class MyModel(db.Model):
    __tablename__ = 'my_models'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', backref='my_models')
```

### Database Operations

#### Create (INSERT)
```python
from app.models import db, Student
new_student = Student(
    user_id=1,
    roll_no='CS2024001',
    department='CS',
    semester=4
)
db.session.add(new_student)
db.session.commit()
```

#### Read (SELECT)
```python
# Get one record
student = Student.query.get(1)
student = Student.query.filter_by(roll_no='CS2024001').first()

# Get all records
all_students = Student.query.all()

# Filter with conditions
students = Student.query.filter(Student.semester >= 4).all()
```

#### Update (UPDATE)
```python
student = Student.query.get(1)
student.semester = 5
db.session.commit()
```

#### Delete (DELETE)
```python
student = Student.query.get(1)
db.session.delete(student)
db.session.commit()
```

### Reset Database
```bash
# Delete database file
rm erp_system.db

# Restart app (recreates database)
python run.py
```

---

## 🌐 Adding New Routes

### Step 1: Create Route File
```python
# In app/mynewmodule/routes.py
from flask import render_template, redirect, url_for
from flask_login import login_required, current_user
from app.mynewmodule import mynewmodule_bp

@mynewmodule_bp.route('/list')
@login_required
def list_items():
    items = Item.query.all()
    return render_template('mynewmodule/list.html', items=items)

@mynewmodule_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_item():
    if request.method == 'POST':
        # Handle form submission
        return redirect(url_for('mynewmodule.list_items'))
    return render_template('mynewmodule/add.html')
```

### Step 2: Create Blueprint
```python
# In app/mynewmodule/__init__.py
from flask import Blueprint

mynewmodule_bp = Blueprint('mynewmodule', __name__, url_prefix='/mynewmodule')

from app.mynewmodule import routes
```

### Step 3: Register Blueprint
```python
# In app/__init__.py
from app.mynewmodule import mynewmodule_bp
app.register_blueprint(mynewmodule_bp)
```

### Step 4: Create Template
```html
<!-- In templates/mynewmodule/list.html -->
{% extends "base.html" %}

{% block content %}
<h1>My Items</h1>
{% for item in items %}
    <p>{{ item.name }}</p>
{% endfor %}
{% endblock %}
```

---

## 🎨 Template Development

### Template Location
```
templates/
├── base.html              # Inherit from this
├── auth/
├── dashboard/
└── mynewmodule/          # Your templates here
```

### Creating Templates

```html
<!-- Extend base template -->
{% extends "base.html" %}

<!-- Define block title -->
{% block title %}My Page - College ERP{% endblock %}

<!-- Define content block -->
{% block content %}
<div class="space-y-6">
    <!-- Header -->
    <div class="bg-blue-50 rounded-lg p-6 border-l-4 border-blue-600">
        <h1 class="text-3xl font-bold text-gray-800">My Page</h1>
        <p class="text-gray-600 mt-2">Description here</p>
    </div>

    <!-- Content -->
    <div class="bg-white rounded-lg shadow-md p-6">
        {% if items %}
        <ul>
            {% for item in items %}
            <li>{{ item.name }}</li>
            {% endfor %}
        </ul>
        {% else %}
        <p>No items found</p>
        {% endif %}
    </div>
</div>
{% endblock %}
```

### Jinja2 Template Syntax

```html
<!-- Variables -->
{{ variable_name }}

<!-- Conditional -->
{% if condition %}
    <p>True</p>
{% else %}
    <p>False</p>
{% endif %}

<!-- Loops -->
{% for item in items %}
    <p>{{ item.name }}</p>
{% endfor %}

<!-- Filters -->
{{ name|upper }}
{{ date|strftime('%Y-%m-%d') }}

<!-- Comments -->
{# This is a comment #}

<!-- URL generation -->
<a href="{{ url_for('student.dashboard') }}">Dashboard</a>
```

---

## 🎯 Authentication & Authorization

### Current User
```python
from flask_login import current_user

# Get current logged-in user
user = current_user

# Check if authenticated
if current_user.is_authenticated:
    print(f"Logged in as {current_user.username}")
    print(f"Role: {current_user.role}")
```

### Role Checking
```python
# Restrict to students only
@app.route('/student-only')
@login_required
def student_only():
    if current_user.role != 'student':
        flash('Only students can access this', 'danger')
        return redirect(url_for('auth.login'))
    return render_template('student_page.html')

# Check in template
{% if current_user.role == 'admin' %}
    <a href="/admin">Admin Panel</a>
{% endif %}
```

### Password Hashing
```python
from app.models import User

# Create user with password
user = User(username='john', email='john@example.com')
user.set_password('mypassword123')
db.session.add(user)
db.session.commit()

# Verify password
if user.check_password('mypassword123'):
    print("Password correct!")
```

---

## 📤 File Upload Handling

### Upload Function
```python
from app.utils.file_handler import save_file_securely

@student_bp.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    
    # Save file securely
    file_path, file_name = save_file_securely(file, 'notes')
    
    if file_path:
        # File saved successfully
        note = Note(
            user_id=current_user.id,
            file_path=file_path,
            file_name=file_name
        )
        db.session.add(note)
        db.session.commit()
        flash('File uploaded!', 'success')
    else:
        flash('Invalid file type', 'danger')
    
    return redirect(url_for('student.dashboard'))
```

### File Handler Code
```python
# In app/utils/file_handler.py
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'doc', 'docx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_file_securely(file, upload_type='notes'):
    if not file or not allowed_file(file.filename):
        return None, None
    
    filename = secure_filename(file.filename)
    # Add UUID to prevent conflicts
    unique_filename = f"{uuid.uuid4()}_{datetime.utcnow().strftime('%Y%m%d')}.{ext}"
    
    upload_path = os.path.join(app.config['UPLOAD_FOLDER'], upload_type, unique_filename)
    file.save(upload_path)
    
    return upload_path, unique_filename
```

---

## 🎨 Styling with Tailwind CSS

### Tailwind Classes

```html
<!-- Spacing -->
<div class="p-6 m-4 mb-8"></div>

<!-- Colors -->
<div class="bg-blue-600 text-white"></div>
<div class="text-red-600">Error</div>

<!-- Responsive -->
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3"></div>

<!-- Flexbox -->
<div class="flex items-center justify-between gap-4"></div>

<!-- Display -->
<div class="hidden md:block"></div>

<!-- Borders -->
<div class="border border-gray-300 rounded-lg"></div>

<!-- Shadows -->
<div class="shadow-md hover:shadow-lg transition"></div>

<!-- State -->
<button class="bg-blue-600 hover:bg-blue-700 active:bg-blue-800"></button>
```

### Custom CSS
```css
/* In static/css/style.css */
.custom-class {
    @apply bg-blue-50 p-6 rounded-lg border-l-4 border-blue-600;
}

/* Animations */
@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

.fade-in {
    animation: fadeIn 0.3s ease-in;
}
```

---

## 🧪 Testing Routes

### Using curl
```bash
# GET request
curl http://localhost:5000/student/attendance

# POST request
curl -X POST http://localhost:5000/student/apply-leave \
  -d "start_date=2026-03-15&end_date=2026-03-20&reason=sick"
```

### Using Python
```python
from run import app

# Create test client
client = app.test_client()

# Test GET
response = client.get('/student/attendance')
print(response.status_code)  # 200, 404, 500, etc.
print(response.data.decode())  # HTML content

# Test POST
response = client.post('/auth/login', data={
    'username': 'student',
    'password': 'student123'
})
```

---

## 🐛 Debugging

### Print Statements
```python
from flask import current_app

@student_bp.route('/debug')
def debug():
    user = current_user
    current_app.logger.info(f"User: {user.username}")
    print(f"Debug: {user.role}")
    return "Check console"
```

### Flask Shell
```bash
# Start Flask shell
flask shell

# Now you can query database
>>> from app.models import Student
>>> students = Student.query.all()
>>> for s in students:
...     print(s.roll_no, s.user.username)
```

### Database Inspection
```bash
# View with SQLite
sqlite3 erp_system.db

# SQL commands
sqlite> .tables  # See all tables
sqlite> SELECT * FROM users;  # View users
sqlite> .schema students  # See table structure
```

### Flask Debug Toolbar
```python
# In app/__init__.py
from flask_debugtoolbar import DebugToolbarExtension

# toolbar = DebugToolbarExtension(app)
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
```

---

## 📊 Performance Optimization

### Database Query Optimization
```python
# BAD - N+1 query problem
for student in Student.query.all():
    print(student.user.username)  # Queries DB for each student

# GOOD - Use eager loading
students = Student.query.options(joinedload('user')).all()
for student in students:
    print(student.user.username)  # No extra queries
```

### Caching
```python
from functools import lru_cache

@lru_cache(maxsize=128)
def get_timetable():
    return Timetable.query.all()
```

### Template Caching
```python
# Automatically handled by Jinja2 in production
# Restart server to see template changes during development
```

---

## 🚀 Deployment Considerations

### Environment Variables
```env
# .env file
FLASK_ENV=production
SECRET_KEY=your-secure-random-key-here
DATABASE_URL=sqlite:///prod.db
```

### Security Checks
```python
# Ensure in app/config.py
SESSION_COOKIE_SECURE = True  # HTTPS only
SESSION_COOKIE_HTTPONLY = True  # No JavaScript access
```

### Using Gunicorn
```bash
# Install
pip install gunicorn

# Run
gunicorn -w 4 -b 0.0.0.0:8000 run:app
# -w 4: 4 worker processes
# -b 0.0.0.0:8000: Bind to all interfaces on port 8000
```

---

## 📚 Common Tasks

### Add New Database Field
```python
# 1. Add field to model in app/models.py
new_field = db.Column(db.String(100))

# 2. Delete database
rm erp_system.db

# 3. Restart server
python run.py
```

### Create New Admin Function
```python
# In app/admin/routes.py
@admin_bp.route('/my-function')
@login_required
def my_function():
    if current_user.role != 'admin':
        abort(403)  # Forbidden
    
    items = Item.query.all()
    return render_template('admin/my_function.html', items=items)
```

### Add Flash Message
```python
from flask import flash

# In route
flash('Successfully saved!', 'success')  # Green
flash('Error occurred!', 'danger')       # Red
flash('Note: This is info', 'info')      # Blue

# In template - auto-displayed by base.html
```

---

## 🔗 Useful Resources

- **Flask Docs**: https://flask.palletsprojects.com/
- **SQLAlchemy Docs**: https://docs.sqlalchemy.org/
- **Jinja2 Docs**: https://jinja.palletsprojects.com/
- **Tailwind CSS**: https://tailwindcss.com/
- **Flask-Login**: https://flask-login.readthedocs.io/

---

## 💡 Tips & Best Practices

1. **Always use @login_required** on protected routes
2. **Validate input** - Check form data before processing
3. **Use blueprints** - Keep code organized
4. **Database transactions** - Use db.session.commit()
5. **Error handling** - Show meaningful error messages
6. **Security first** - Hash passwords, validate files
7. **DRY principle** - Don't repeat code, use templates
8. **Test thoroughly** - Use test client before deploying
9. **Document code** - Add docstrings and comments
10. **Use version control** - Git for tracking changes

---

## 📝 Code Style Guide

### Python PEP 8
```python
# Good
def register_user(username, email):
    user = User(username=username, email=email)
    return user

# Bad
def registerUser(username,email):return User(username=username,email=email)
```

### Naming Conventions
```python
# Variables & functions: snake_case
user_name = "John"
def get_user_data():
    pass

# Classes: PascalCase
class UserModel:
    pass

# Constants: UPPER_SNAKE_CASE
MAX_FILE_SIZE = 16 * 1024 * 1024
```

---

## 🎓 Learning Path

1. Understand Flask basics (app factory, blueprints)
2. Learn SQLAlchemy models and queries
3. Master template rendering (Jinja2)
4. Implement authentication (Flask-Login)
5. Add file upload functionality
6. Style with Tailwind CSS
7. Deploy to production

---

**Happy Development! 🚀**

For questions or issues, refer to the README.md and inline code comments.
