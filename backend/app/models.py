from .extensions import db
from datetime import datetime, date
from passlib.hash import bcrypt

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(50), default='hr')  # admin, hr, supervisor, employee
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = bcrypt.hash(password)

    def check_password(self, password):
        return bcrypt.verify(password, self.password_hash)

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120))
    phone = db.Column(db.String(40))
    role = db.Column(db.String(80))  # field_worker, supervisor, admin
    wage_type = db.Column(db.String(20), default='daily')  # daily or monthly
    wage_amount = db.Column(db.Float, default=0.0)
    farm_location = db.Column(db.String(120))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    check_in = db.Column(db.DateTime)
    check_out = db.Column(db.DateTime)
    notes = db.Column(db.String(300))

class PayrollAdjustment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    period_start = db.Column(db.Date, nullable=False)
    period_end = db.Column(db.Date, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    reason = db.Column(db.String(300))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
