from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
    balance = db.Column(db.Float, default=0.0)
    parent_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    parent = db.relationship('User', remote_side=[id], backref='children')


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    amount = db.Column(db.Float)
    type = db.Column(db.String(20))
    timestamp = db.Column(db.DateTime, default=db.func.now())
    user = db.relationship('User', backref=db.backref('transactions', lazy=True))


class BalanceLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    type = db.Column(db.String(20))
    before = db.Column(db.Float)
    after = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, default=db.func.now())
    user = db.relationship('User', backref=db.backref('balance_logs', lazy=True))
