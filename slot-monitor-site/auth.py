from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import jwt
from functools import wraps

from models import db, User


auth_bp = Blueprint('auth', __name__)


def token_required(f):
    """Simple JWT token check for protected endpoints."""
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return jsonify({'error': 'missing token'}), 401
        token = auth_header.split(' ', 1)[1]
        try:
            payload = jwt.decode(
                token,
                current_app.config['SECRET_KEY'],
                algorithms=['HS256'],
            )
            request.user_id = payload['sub']
        except Exception:
            return jsonify({'error': 'invalid token'}), 401
        return f(*args, **kwargs)

    return wrapper


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'error': 'missing credentials'}), 400
    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'user exists'}), 400
    user = User(username=username, password=generate_password_hash(password))
    db.session.add(user)
    db.session.commit()
    return jsonify({'status': 'registered'})


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')
    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({'error': 'invalid credentials'}), 401
    payload = {
        'sub': user.id,
        'exp': datetime.utcnow() + timedelta(hours=2)
    }
    token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')
    return jsonify({'token': token})
