from flask import Blueprint, request, jsonify, current_app, send_file
from .extensions import db
from .models import User, Employee, Attendance, PayrollAdjustment
from .auth import generate_token, login_required
from datetime import date, datetime

api_bp = Blueprint('api', __name__)

# ---- Auth ----
@api_bp.route('/auth/login', methods=['POST'])
def login():
    data = request.json or {}
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'msg':'username and password required'}), 400
    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return jsonify({'msg':'invalid credentials'}), 401
    token = generate_token(user)
    return jsonify({'access_token': token, 'user': {'username': user.username, 'role': user.role}})

# ---- Users (admin) ----
@api_bp.route('/users', methods=['GET'])
@login_required(role='admin')
def list_users():
    users = User.query.all()
    return jsonify([{'id':u.id,'username':u.username,'role':u.role} for u in users])

@api_bp.route('/users', methods=['POST'])
@login_required(role='admin')
def create_user():
    data = request.json or {}
    u = User(username=data.get('username'), role=data.get('role','hr'))
    u.set_password(data.get('password','password'))
    db.session.add(u)
    db.session.commit()
    return jsonify({'msg':'created','id':u.id})

# ---- Employees ----
@api_bp.route('/employees', methods=['GET'])
@login_required()
def employees_list():
    emps = Employee.query.order_by(Employee.id).all()
    return jsonify([{
        'id':e.id,'first_name':e.first_name,'last_name':e.last_name,'phone':e.phone,
        'role':e.role,'wage_type':e.wage_type,'wage_amount':e.wage_amount,'farm_location':e.farm_location
    } for e in emps])

@api_bp.route('/employees', methods=['POST'])
@login_required()
def employees_create():
    data = request.json or {}
    e = Employee(
        first_name=data.get('first_name'),
        last_name=data.get('last_name'),
        phone=data.get('phone'),
        role=data.get('role','field_worker'),
        wage_type=data.get('wage_type','daily'),
        wage_amount=float(data.get('wage_amount') or 0),
        farm_location=data.get('farm_location')
    )
    db.session.add(e)
    db.session.commit()
    return jsonify({'msg':'created','id':e.id})

@api_bp.route('/employees/<int:id>', methods=['PUT','PATCH'])
@login_required()
def employees_update(id):
    e = Employee.query.get_or_404(id)
    data = request.json or {}
    for k in ('first_name','last_name','phone','role','wage_type','wage_amount','farm_location'):
        if k in data:
            setattr(e, k, data[k])
    db.session.commit()
    return jsonify({'msg':'updated'})

@api_bp.route('/employees/<int:id>', methods=['DELETE'])
@login_required()
def employees_delete(id):
    e = Employee.query.get_or_404(id)
    db.session.delete(e)
    db.session.commit()
    return jsonify({'msg':'deleted'})

# ---- Attendance ----
@api_bp.route('/attendance', methods=['POST'])
@login_required()
def attendance_checkin():
    data = request.json or {}
    emp_id = data.get('employee_id')
    dt = data.get('date') or date.today().isoformat()
    att = Attendance(employee_id=emp_id, date=date.fromisoformat(dt), check_in=datetime.utcnow(), notes=data.get('notes'))
    db.session.add(att)
    db.session.commit()
    return jsonify({'msg':'checked_in','id':att.id})

@api_bp.route('/attendance/checkout', methods=['POST'])
@login_required()
def attendance_checkout():
    data = request.json or {}
    emp_id = data.get('employee_id')
    dt = data.get('date') or date.today().isoformat()
    att = Attendance.query.filter_by(employee_id=emp_id, date=date.fromisoformat(dt)).first()
    if not att:
        return jsonify({'msg':'attendance record not found'}), 404
    att.check_out = datetime.utcnow()
    db.session.commit()
    return jsonify({'msg':'checked_out'})

# ---- Payroll adjustments (manual) ----
@api_bp.route('/payroll/adjust', methods=['POST'])
@login_required(role='hr')
def payroll_adjust():
    data = request.json or {}
    adj = PayrollAdjustment(
        employee_id=data.get('employee_id'),
        period_start=date.fromisoformat(data.get('period_start')),
        period_end=date.fromisoformat(data.get('period_end')),
        amount=float(data.get('amount')),
        reason=data.get('reason')
    )
    db.session.add(adj)
    db.session.commit()
    return jsonify({'msg':'adjustment_added','id':adj.id})

# ---- Reports ----
@api_bp.route('/report/attendance_summary', methods=['GET'])
@login_required()
def report_attendance_summary():
    start = request.args.get('start')
    end = request.args.get('end')
    if not start or not end:
        return jsonify({'msg':'provide start and end YYYY-MM-DD'}), 400
    s = date.fromisoformat(start); e = date.fromisoformat(end)
    q = db.session.query(Attendance.employee_id, db.func.count(Attendance.id)).filter(Attendance.date>=s, Attendance.date<=e).group_by(Attendance.employee_id).all()
    data = []
    for eid, cnt in q:
        emp = Employee.query.get(eid)
        data.append({'employee_id':eid, 'name':f"{emp.first_name} {emp.last_name or ''}".strip(), 'attendance_count':cnt})
    return jsonify(data)

@api_bp.route('/report/payroll', methods=['GET'])
@login_required()
def report_payroll():
    start = request.args.get('start'); end = request.args.get('end')
    if not start or not end:
        return jsonify({'msg':'provide start and end YYYY-MM-DD'}), 400
    s = date.fromisoformat(start); e = date.fromisoformat(end)
    employees = Employee.query.all()
    rows = []
    for emp in employees:
        days_present = Attendance.query.filter(Attendance.employee_id==emp.id, Attendance.date>=s, Attendance.date<=e, Attendance.check_in!=None).count()
        if emp.wage_type == 'daily':
            gross = days_present * emp.wage_amount
        else:
            days_in_range = (e - s).days + 1
            gross = emp.wage_amount * (days_in_range / 30.0)
        # apply adjustments
        adjustments = PayrollAdjustment.query.filter(PayrollAdjustment.employee_id==emp.id, PayrollAdjustment.period_start>=s, PayrollAdjustment.period_end<=e).all()
        adj_total = sum([a.amount for a in adjustments])
        rows.append({'employee_id':emp.id,'name':f"{emp.first_name} {emp.last_name or ''}".strip(),'days_present':days_present,'gross':round(gross+adj_total,2),'adjustments':adj_total})
    return jsonify(rows)

# ---- DB download (for demo) ----
@api_bp.route('/admin/download_db', methods=['GET'])
@login_required(role='admin')
def download_db():
    path = current_app.config.get('SQLALCHEMY_DATABASE_URI').replace('sqlite:///','')
    return send_file(path, as_attachment=True)
