# College ERP Mini System

A comprehensive web-based Enterprise Resource Planning (ERP) system designed for colleges and educational institutions. This application manages student data, attendance, fees, leaves, notes, certificates, timetables, and more.

## 🎯 Features

### For Students
- ✅ Personal Dashboard with quick stats (attendance, fees, certificates)
- ✅ View Attendance Records (daily/monthly)
- ✅ Fee Management (semester-wise fees, payment status)
- ✅ Leave Applications (apply, track status)
- ✅ Study Materials (download notes uploaded by faculty)
- ✅ Download Certificates
- ✅ View Timetable and Staff Directory

### For Faculty
- ✅ Faculty Dashboard with department analytics
- ✅ Mark Attendance (bulk mark for students)
- ✅ Upload Study Notes/Materials (PDF, DOC, JPG, PNG)
- ✅ Manage Uploaded Notes
- ✅ View Student List
- ✅ Access Timetable

### For Admin
- ✅ Admin Dashboard with system statistics
- ✅ User Management (view all users by role)
- ✅ Student Management (filter by department)
- ✅ Leave Approval System (approve/reject applications)
- ✅ Certificate Management (upload for students)
- ✅ Timetable Management
- ✅ Staff Directory Management
- ✅ System Overview and Analytics

## 🛠️ Technology Stack

### Frontend
- **HTML5** - Markup
- **CSS3 & Tailwind CSS** - Responsive Design
- **JavaScript** - Client-side Logic
- **Font Awesome Icons** - UI Icons

### Backend
- **Python 3.x** - Server Language
- **Flask 2.3.3** - Web Framework
- **Flask-SQLAlchemy 3.0.5** - ORM
- **Flask-Login 0.6.2** - Authentication
- **SQLite3** - Database
- **Werkzeug** - Security & Utilities

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Virtual Environment (recommended)

### Setup Steps

1. **Clone/Download the project**
   ```bash
   cd e:\CSSD\ErpSystem
   ```

2. **Create a Virtual Environment (optional but recommended)**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application**
   ```bash
   python run.py
   ```

5. **Access the Application**
   Open your browser and navigate to:
   ```
   http://localhost:5000
   ```

## 👥 Default Login Credentials

The system comes with 3 default accounts for testing:

| Role | Username | Password |
|------|----------|----------|
| **Admin** | admin | admin123 |
| **Faculty** | faculty | faculty123 |
| **Student** | student | student123 |

> ⚠️ **Important**: Change these credentials in production!

## 📁 Project Structure

```
ErpSystem/
├── app/                      # Main Flask application
│   ├── __init__.py          # Flask app factory
│   ├── config.py            # Configuration settings
│   ├── models.py            # Database models
│   ├── auth/                # Authentication routes
│   ├── main/                # Main routes (home, timetable, staff)
│   ├── student/             # Student-specific routes
│   ├── faculty/             # Faculty-specific routes
│   ├── admin/               # Admin-specific routes
│   └── utils/               # Utility functions
├── templates/               # HTML templates (Jinja2)
│   ├── base.html           # Base template
│   ├── auth/               # Login/Auth pages
│   ├── dashboard/          # Role-based dashboards
│   ├── attendance/         # Attendance pages
│   ├── timetable/          # Timetable pages
│   ├── leave/              # Leave management pages
│   ├── fees/               # Fee pages
│   ├── notes/              # Notes/Materials pages
│   ├── certificates/       # Certificate pages
│   ├── staff/              # Staff directory
│   └── admin/              # Admin-specific pages
├── static/                  # Static files
│   ├── css/                # Stylesheets
│   ├── js/                 # JavaScript files
│   └── uploads/            # User uploaded files
├── run.py                  # Entry point
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables
├── .gitignore             # Git ignore file
└── README.md              # This file
```

## 🗄️ Database Models

### User (Authentication)
- username, email, password_hash, role, is_active

### Student
- roll_no, department, semester, phone, address

### Faculty
- designation, department, phone, office

### Attendance
- student_id, date, status, marked_by

### Leave
- user_id, start_date, end_date, reason, status

### Fee
- student_id, semester, amount, status, due_date, paid_date

### Note (Study Materials)
- user_id (faculty), title, subject, file_path, department, semester

### Certificate
- user_id (admin), student_id, certificate_type, file_path, issue_date

### Timetable
- department, semester, day_of_week, subject, faculty_name, room_no

### Staff
- name, designation, department, email, phone, office

## 🔐 Security Features

- ✅ Password hashing using Werkzeug
- ✅ SQL injection prevention (SQLAlchemy ORM)
- ✅ Session-based authentication (Flask-Login)
- ✅ File upload validation and secure naming
- ✅ Role-based access control (RBAC)
- ✅ CSRF protection ready (Flask-WTF)

## 📝 Key Routes & Endpoints

### Authentication
- `GET/POST /auth/login` - Login page
- `GET /auth/logout` - Logout

### Student Routes
- `GET /student/dashboard` - Student dashboard
- `GET /student/attendance` - View attendance
- `GET /student/fees` - View fees
- `GET/POST /student/apply-leave` - Apply for leave
- `GET /student/my-leaves` - View leave applications
- `GET /student/notes` - View study notes
- `GET /student/certificates` - Download certificates

### Faculty Routes
- `GET /faculty/dashboard` - Faculty dashboard
- `GET/POST /faculty/mark-attendance` - Mark attendance
- `GET/POST /faculty/upload-notes` - Upload notes
- `GET /faculty/my-notes` - Manage uploaded notes
- `POST /faculty/delete-note/<id>` - Delete note

### Admin Routes
- `GET /admin/dashboard` - Admin dashboard
- `GET /admin/users` - Manage users
- `GET /admin/students` - Manage students
- `GET/POST /admin/manage-leaves` - Leave management
- `GET/POST /admin/upload-certificate` - Upload certificates
- `GET /admin/manage-timetable` - Manage timetable
- `GET /admin/manage-staff` - Manage staff

### Main Routes
- `GET /` - Home (redirects based on login)
- `GET /timetable` - View timetable
- `GET /staff` - Staff directory

## 🚀 Deployment

### Development
```bash
python run.py
```

### Production (using Gunicorn)
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

### Environment Variables
Update `.env` file for production:
```env
FLASK_ENV=production
SECRET_KEY=your-secure-key-here
DATABASE_URL=sqlite:///db.sqlite3
```

## 📊 Usage Examples

### 1. Admin Adding a Staff Member
1. Login as admin
2. Go to Admin Dashboard → Manage Staff → Add Staff Member
3. Fill in details and submit

### 2. Faculty Marking Attendance
1. Login as faculty
2. Go to Faculty Dashboard → Mark Attendance
3. Select date and mark present/absent/leave for each student
4. Click Save

### 3. Student Applying for Leave
1. Login as student
2. Go to Student Dashboard → Apply for Leave
3. Fill in dates, reason, and submit
4. Admin reviews and approves/rejects

### 4. Faculty Uploading Notes
1. Login as faculty
2. Go to Faculty Dashboard → Upload Notes
3. Select file (PDF, DOC, JPG, PNG)
4. Add title, subject, description
5. Upload

## 🐛 Troubleshooting

### Database Issues
If you encounter database errors:
```bash
# Delete the existing database
rm erp_system.db

# Restart the app (it will recreate database)
python run.py
```

### Port Already in Use
If port 5000 is busy:
```bash
python run.py --port 5001
```

### Import Errors
Ensure all dependencies are installed:
```bash
pip install -r requirements.txt --force-reinstall
```

## 📞 Support

For issues, bugs, or feature requests, please create an issue in the project repository.

## 📄 License

This project is provided as-is for educational purposes.

## 👨‍💻 Development

### Adding New Features
1. Create routes in respective blueprint (student, faculty, admin)
2. Create database models if needed in `models.py`
3. Create HTML templates in `templates/` folder
4. Update `base.html` navigation if needed
5. Test thoroughly before deploying

### Database Migrations
If you modify models:
1. Delete `erp_system.db` 
2. Restart the app (it will recreate with new schema)

## 🎓 Educational Use

This system is designed for educational institutions and can be:
- **Customized** with additional features
- **Extended** with more modules (grades, notifications, etc.)
- **Integrated** with third-party services
- **Deployed** on cloud platforms

## 📈 Future Enhancements

Potential features to add:
- Email notifications for leave/fee updates
- Grades and marks management
- Online examination system
- SMS alerts
- Mobile app
- Advanced reporting and analytics
- Payment gateway integration
- Hostel management
- Library management

---

**Created**: March 2026
**Version**: 1.0.0
**Status**: Production Ready ✅
