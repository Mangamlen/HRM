# Run this to create some demo employees and attendance data
from app import create_app
from app.extensions import db
from app.models import Employee, Attendance, User
from datetime import date, datetime, timedelta
app = create_app()
with app.app_context():
    if not Employee.query.first():
        e1 = Employee(first_name='Ramesh', last_name='Devi', phone='9123456780', role='field_worker', wage_type='daily', wage_amount=300, farm_location='North Field')
        e2 = Employee(first_name='Sita', last_name='K.', phone='9123456799', role='supervisor', wage_type='monthly', wage_amount=15000, farm_location='Orchard')
        db.session.add_all([e1,e2]); db.session.commit()
        # add attendance for past 7 days
        for i in range(7):
            d = date.today() - timedelta(days=i)
            a = Attendance(employee_id=e1.id, date=d, check_in=datetime.utcnow())
            db.session.add(a)
        db.session.commit()
        print('Seeded demo data')
    else:
        print('Data exists')
