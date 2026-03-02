"""
Sample Data Seeder for College ERP System
Run this script to populate the database with sample data for testing
"""

from app import create_app, db
from app.models import (
    User, Student, Faculty, Attendance, Leave, Fee, Note, 
    Certificate, Timetable, Staff
)
from datetime import datetime, timedelta
import random

app = create_app('development')

def seed_database():
    """Populate database with sample data"""
    with app.app_context():
        print("🌱 Starting database seeding...")
        
        # Clear existing data (optional)
        # db.drop_all()
        # db.create_all()
        
        # Add sample students
        print("📚 Adding students...")
        students_data = [
            ('CS2024001', 'Alice Kumar'),
            ('CS2024002', 'Bob Singh'),
            ('CS2024003', 'Carol Sharma'),
            ('EC2024001', 'David Patel'),
            ('EC2024002', 'Emma Wilson'),
        ]
        
        for roll_no, name in students_data:
            user = User(
                username=name.lower().replace(' ', '_'),
                email=f"{name.lower().replace(' ', '.')}@student.edu",
                role='student',
                is_active=True
            )
            user.set_password('password123')
            db.session.add(user)
            db.session.commit()
            
            dept = 'Computer Science' if roll_no.startswith('CS') else 'Electronics'
            student = Student(
                user_id=user.id,
                roll_no=roll_no,
                department=dept,
                semester=random.randint(1, 8),
                phone=f'98{random.randint(10000000, 99999999)}'
            )
            db.session.add(student)
        
        db.session.commit()
        
        # Add attendance records
        print("✅ Adding attendance records...")
        students = Student.query.all()
        for student in students:
            for i in range(30):
                date = datetime.utcnow().date() - timedelta(days=i)
                status = random.choice(['present', 'absent', 'leave'])
                
                # Check if record exists
                existing = Attendance.query.filter_by(
                    student_id=student.id,
                    date=date
                ).first()
                
                if not existing:
                    attendance = Attendance(
                        student_id=student.id,
                        date=date,
                        status=status,
                        marked_by='faculty'
                    )
                    db.session.add(attendance)
        
        db.session.commit()
        
        # Add fees
        print("💰 Adding fee records...")
        for student in students:
            for sem in range(1, 9):
                fee = Fee(
                    student_id=student.id,
                    semester=sem,
                    amount=50000 + random.randint(0, 10000),
                    status=random.choice(['paid', 'pending']),
                    paid_date=datetime.utcnow() if random.choice([True, False]) else None,
                    due_date=datetime.utcnow().date() + timedelta(days=random.randint(1, 60))
                )
                try:
                    db.session.add(fee)
                except:
                    db.session.rollback()
        
        db.session.commit()
        
        # Add sample timetable
        print("📅 Adding timetable...")
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        subjects = ['Database', 'Data Structures', 'Web Development', 'Algorithms', 'OOP']
        departments = ['Computer Science', 'Electronics']
        
        for dept in departments:
            for day in days:
                timetable = Timetable(
                    department=dept,
                    semester=4,
                    day_of_week=day,
                    start_time=f'{9 + random.randint(0, 6):02d}:00',
                    end_time=f'{10 + random.randint(0, 6):02d}:00',
                    subject=random.choice(subjects),
                    faculty_name='Dr. ' + random.choice(['Smith', 'Kumar', 'Patel']),
                    room_no=f'{random.randint(101, 310)}'
                )
                db.session.add(timetable)
        
        db.session.commit()
        
        # Add sample staff
        print("👥 Adding staff...")
        designations = ['Registrar', 'Finance Officer', 'Librarian', 'Director', 'HOD']
        departments_staff = ['Administration', 'Finance', 'Library', 'Academic', 'IT']
        
        for i in range(5):
            staff = Staff(
                name=f'Staff Member {i+1}',
                designation=designations[i],
                department=departments_staff[i],
                email=f'staff{i+1}@college.edu',
                phone=f'98{random.randint(10000000, 99999999)}',
                office=f'Block A, Room {101 + i}'
            )
            db.session.add(staff)
        
        db.session.commit()
        
        print("✨ Database seeding completed successfully!")
        print("\n📊 Summary:")
        print(f"  • Students: {Student.query.count()}")
        print(f"  • Faculty: {Faculty.query.count()}")
        print(f"  • Attendance Records: {Attendance.query.count()}")
        print(f"  • Fees: {Fee.query.count()}")
        print(f"  • Timetable Slots: {Timetable.query.count()}")
        print(f"  • Staff: {Staff.query.count()}")

if __name__ == '__main__':
    seed_database()
