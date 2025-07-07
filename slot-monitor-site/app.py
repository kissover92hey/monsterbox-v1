from flask import Flask, jsonify, render_template
import os

from config import Config
from models import db, Transaction
from auth import auth_bp
from routes.game import game_bp
from routes.admin import admin_bp
from routes.user import user_bp


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{Config.DATABASE_URI}"
app.config['SECRET_KEY'] = Config.SECRET_KEY
app.config['API_TOKEN'] = Config.API_TOKEN
app.config['BRAND_NAME'] = Config.BRAND_NAME
app.config['DEFAULT_LANGUAGE'] = Config.DEFAULT_LANGUAGE

db.init_app(app)


@app.context_processor
def inject_config():
    return {
        'brand': app.config.get('BRAND_NAME'),
        'default_lang': app.config.get('DEFAULT_LANGUAGE'),
    }


@app.before_first_request
def init_db():
    db.create_all()


app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(game_bp, url_prefix='/api')
app.register_blueprint(admin_bp, url_prefix='/api/admin')
app.register_blueprint(user_bp, url_prefix='/api/user')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login')
def login_page():
    """Render dedicated login page."""
    return render_template('login.html')


@app.route('/admin')
def admin_page():
    """Render simple admin dashboard page."""
    return render_template('admin.html')


@app.route('/api/logs')
def api_logs():
    log_file = Config.LOG_FILE
    if not os.path.exists(log_file):
        return jsonify([])
    with open(log_file, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]
    return jsonify(lines)


@app.route('/api/transactions')
def api_transactions():
    transactions = Transaction.query.order_by(Transaction.timestamp.desc()).limit(100).all()
    rows = [
        {
            'id': t.id,
            'user_id': t.user_id,
            'amount': t.amount,
            'type': t.type,
            'timestamp': t.timestamp.isoformat()
        }
        for t in transactions
    ]
    return jsonify(rows)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
