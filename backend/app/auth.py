from functools import wraps
from flask import request, jsonify, current_app
import jwt
from datetime import datetime, timedelta
from .models import User

def generate_token(user):
    payload = {
        'sub': user.id,
        'username': user.username,
        'role': user.role,
        'exp': datetime.utcnow() + timedelta(days=current_app.config.get('JWT_EXP_DAYS',7))
    }
    token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')
    return token

def decode_token(token):
    try:
        payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        return payload
    except Exception as e:
        return None

def login_required(role=None):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            auth = request.headers.get('Authorization', None)
            if not auth or not auth.startswith('Bearer '):
                return jsonify({'msg':'Missing or invalid authorization header'}), 401
            token = auth.split(' ',1)[1]
            payload = decode_token(token)
            if not payload:
                return jsonify({'msg':'Invalid or expired token'}), 401
            # attach user info to request context
            request.user = payload
            if role and payload.get('role') != role and payload.get('role') != 'admin':
                return jsonify({'msg':'Insufficient role'}), 403
            return f(*args, **kwargs)
        return wrapped
    return decorator
