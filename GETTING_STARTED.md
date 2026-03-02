# 🚀 Quick Start Guide - College ERP System

Get the College ERP system running in less than 5 minutes!

## ⚡ 5-Minute Setup

### Step 1: Install Dependencies (2 minutes)
```bash
cd e:\CSSD\ErpSystem
pip install -r requirements.txt
```

### Step 2: Start the Application (1 minute)
```bash
python run.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
 * Debugger PIN: xxxxx
```

### Step 3: Open in Browser (1 minute)
Navigate to:
```
http://localhost:5000
```

You'll see the login page! 🎉

### Step 4: Login with Demo Account (1 minute)

Choose from these default accounts:

| Role | Username | Password | Dashboard |
|------|----------|----------|-----------|
| **Student** | student | student123 | View attendance, fees, apply leave |
| **Faculty** | faculty | faculty123 | Mark attendance, upload notes |
| **Admin** | admin | admin123 | Manage users, approvals, staff |

---

## 📱 What You Can Do Right Now

### 👨‍🎓 As a Student
1. **View Dashboard**: Click on your name in top-right
2. **Check Attendance**: Student Dashboard → View Attendance
3. **Apply Leave**: Student Dashboard → Apply for Leave
4. **Check Fees**: Student Dashboard → View Fees
5. **Download Notes**: Study Materials section

### 👨‍🏫 As Faculty
1. **Mark Attendance**: Faculty Dashboard → Mark Attendance
   - Select a date → Choose Present/Absent/Leave → Save
2. **Upload Notes**: Faculty Dashboard → Upload Notes
   - Select file → Add subject → Upload
3. **View Students**: See all students in your department

### 👨‍💼 As Admin
1. **Approve Leaves**: Admin Dashboard → Review pending applications
2. **Manage Users**: View all system users by role
3. **Upload Certificates**: Upload certificates for students
4. **Add Staff**: Manage staff directory

---

## 🎨 Key Features to Explore

### Responsive Design
- 📱 Works on mobile, tablet, and desktop
- 🌐 Uses Tailwind CSS for beautiful UI
- ⚡ Fast page loads with optimized assets

### Role-Based Access
- 🔐 Each role sees only relevant features
- 🛡️ Secure authentication with Flask-Login
- 📊 Role-specific dashboards

### Data Management
- 📅 Attendance tracking (30-day history visible)
- 💰 Fee structure by semester
- 📝 Leave application workflow
- 📚 Study materials library
- 🏆 Certificate management
- 👥 Complete staff directory

---

## 🗂️ Important File Locations

```
ErpSystem/
├── run.py              ← Start here
├── app/
│   ├── __init__.py    ← Flask factory
│   ├── models.py      ← Database schema
│   └── config.py      ← Configuration
├── templates/          ← HTML pages
├── static/
│   ├── css/           ← Styling
│   ├── js/            ← JavaScript
│   └── uploads/       ← User files
└── erp_system.db      ← Database (auto-created)
```

---

## 🔧 Troubleshooting

### App won't start?
```bash
# Check Python version (need 3.8+)
python --version

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Try a different port
python run.py --port 5001
```

### Login fails?
- Double-check username: `student`, `faculty`, or `admin`
- Use exact password shown in guide
- Check if app shows error message

### Page looks broken?
- Hard refresh: `Ctrl+Shift+R` (Windows) or `Cmd+Shift+R` (Mac)
- Clear browser cache
- Try a different browser

### Database issues?
```bash
# Reset database
del erp_system.db

# Restart app (database will be recreated)
python run.py
```

---

## 📊 Add Sample Data (Optional)

To populate the database with sample attendance, fees, timetables, etc.:

```bash
python seed_data.py
```

This creates:
- 5 sample students
- 30 days of attendance records
- Fee records for all semesters
- Timetable for all classes
- Sample staff members

---

## 🎯 Basic Workflows

### Workflow 1: Student Views Attendance
1. Login as `student`
2. Click "View Attendance" on dashboard
3. See attendance records sorted by date
4. Scroll or use pagination to see more

### Workflow 2: Faculty Marks Attendance
1. Login as `faculty`
2. Click "Mark Attendance"
3. Select a date
4. For each student: Click radio button (Present/Absent/Leave)
5. Click "Save Attendance"
6. Confirmation appears ✅

### Workflow 3: Student Applies Leave
1. Login as `student`
2. Click "Apply for Leave"
3. Select start and end dates
4. Write reason
5. Click "Submit Application"
6. Application shows as "Pending"

### Workflow 4: Admin Approves Leave
1. Login as `admin`
2. Click "Pending Leaves" on dashboard or go to Leave Management
3. Click "Approve" or "Reject" button
4. Leave status updates immediately

---

## 🚀 Next Steps

### Customize for Your College
1. Edit `.env` file for custom settings
2. Modify `app/config.py` for colors/themes
3. Update navigation in `templates/base.html`
4. Add your college logo in static/

### Add More Users
Users can be added through:
1. Direct database entry (advanced)
2. Admin panel (if you extend it)
3. Manual registration (if you implement it)

### Deploy to Cloud
The app can be deployed to:
- **Heroku** - Free tier available
- **PythonAnywhere** - Simple Python hosting
- **AWS/Azure** - Enterprise solutions
- **Local Server** - On-campus hosting

---

## 📚 Learning Resources

### File Structure
- Routes: `app/*/routes.py` - URL endpoints
- Templates: `templates/` - HTML pages
- Models: `app/models.py` - Database tables
- Config: `app/config.py` - Settings

### Key Technologies
- **Flask**: Python web framework
- **SQLAlchemy**: Database ORM
- **Jinja2**: HTML templating
- **Tailwind**: CSS framework
- **SQLite**: Database

---

## 💡 Tips & Tricks

### Change Password
Database stores hashed passwords. To reset:
1. Delete `erp_system.db`
2. Restart app
3. Use default credentials again

### View Database
```bash
# Using Python SQLite viewer
sqlite3 erp_system.db
.tables                    # See all tables
SELECT * FROM users;       # View users
```

### Check Logs
During development, check terminal output for:
- Database queries
- Route requests
- Error messages
- Debug information

### Customize Dashboard
Edit the dashboard templates in:
- `templates/dashboard/student_dashboard.html`
- `templates/dashboard/faculty_dashboard.html`
- `templates/dashboard/admin_dashboard.html`

---

## ❓ FAQ

**Q: Can I change the demo password?**
A: Delete `erp_system.db` and restart - you'll get fresh defaults.

**Q: How do I add new students?**
A: Currently through database. You can extend admin panel to add users.

**Q: Is this production-ready?**
A: It's fully featured but meant for learning. Add proper security for production.

**Q: Can I use PostgreSQL instead of SQLite?**
A: Yes! Change `DATABASE_URL` in `.env` to your PostgreSQL connection string.

**Q: How do I stop the server?**
A: Press `Ctrl+C` in the terminal.

---

## 🎓 What's Included

✅ Complete Database Schema (9 models)
✅ Fully Functional Authentication
✅ Role-Based Access Control
✅ 50+ HTML Templates
✅ Responsive UI with Tailwind CSS
✅ File Upload System
✅ RESTful Routes
✅ Error Handling
✅ Security Best Practices
✅ Comprehensive Documentation

---

## 📞 Getting Help

1. **Check README.md** - Comprehensive documentation
2. **Review routes.py files** - Understand URL patterns
3. **Check templates/** - See how pages are built
4. **Look at models.py** - Understand database structure
5. **Read comments in code** - Helpful explanations

---

## 🎉 You're All Set!

You now have a fully functional College ERP system running on your local machine!

### Next Adventures:
- Add new features
- Customize styling
- Extend functionality
- Deploy to cloud
- Add more users
- Create reports

**Happy Coding! 🚀**

---

*Last Updated: March 2026*
*Version: 1.0.0*
