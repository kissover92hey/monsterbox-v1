from flask import Blueprint, request, jsonify

from models import db, User, Transaction, BalanceLog

user_bp = Blueprint('user', __name__)


def _update_balance(user, change, log_type):
    before = user.balance
    user.balance = before + change
    log = BalanceLog(user_id=user.id, type=log_type, before=before, after=user.balance)
    db.session.add(log)


@user_bp.route('/recharge', methods=['POST'])
def recharge():
    data = request.get_json() or {}
    user_id = data.get('user_id')
    amount = data.get('amount')
    if not user_id or amount is None:
        return jsonify({'error': 'missing fields'}), 400
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'user not found'}), 404
    tx = Transaction(user_id=user_id, amount=amount, type='recharge')
    db.session.add(tx)
    _update_balance(user, amount, 'recharge')
    db.session.commit()
    return jsonify({'status': 'ok', 'balance': user.balance})


@user_bp.route('/transactions')
def user_transactions():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'error': 'missing user_id'}), 400
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'user not found'}), 404
    txs = [
        {
            'id': t.id,
            'amount': t.amount,
            'type': t.type,
            'timestamp': t.timestamp.isoformat(),
        }
        for t in user.transactions
    ]
    return jsonify({'balance': user.balance, 'transactions': txs})
