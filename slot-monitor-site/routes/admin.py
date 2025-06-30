from flask import Blueprint, jsonify

from models import db, User, Transaction
from auth import token_required

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/transactions')
@token_required
def transactions():
    txs = Transaction.query.order_by(Transaction.timestamp.desc()).limit(100).all()
    rows = [
        {
            'id': t.id,
            'user_id': t.user_id,
            'amount': t.amount,
            'type': t.type,
            'timestamp': t.timestamp.isoformat(),
        }
        for t in txs
    ]
    return jsonify(rows)


@admin_bp.route('/users')
@token_required
def users():
    users = User.query.all()
    rows = []
    for u in users:
        balance = sum(t.amount if t.type == 'win' else -t.amount for t in u.transactions)
        txs = [
            {
                'id': t.id,
                'amount': t.amount,
                'type': t.type,
                'timestamp': t.timestamp.isoformat(),
            }
            for t in u.transactions
        ]
        rows.append({'id': u.id, 'username': u.username, 'balance': balance, 'transactions': txs})
    return jsonify(rows)


@admin_bp.route('/stats')
@token_required
def stats():
    """Return daily profit and user count for the last 7 days."""
    from datetime import datetime, timedelta
    today = datetime.utcnow().date()
    data = []
    for i in range(7):
        day = today - timedelta(days=i)
        next_day = day + timedelta(days=1)
        bets = (
            Transaction.query.filter(
                Transaction.type == 'bet',
                Transaction.timestamp >= day,
                Transaction.timestamp < next_day,
            )
            .with_entities(db.func.sum(Transaction.amount))
            .scalar()
            or 0
        )
        wins = (
            Transaction.query.filter(
                Transaction.type == 'win',
                Transaction.timestamp >= day,
                Transaction.timestamp < next_day,
            )
            .with_entities(db.func.sum(Transaction.amount))
            .scalar()
            or 0
        )
        profit = wins - bets
        user_count = (
            User.query.filter(User.created_at < next_day).count()
        )
        data.append({'day': day.isoformat(), 'profit': profit, 'users': user_count})
    return jsonify(list(reversed(data)))
