from flask import Blueprint, request, jsonify, current_app

from models import db, User, Transaction, BalanceLog
from api_client import get_balance as api_get_balance, place_bet as api_place_bet, send_win as api_send_win


game_bp = Blueprint('game', __name__)


def _update_balance(user, change, log_type):
    before = user.balance
    user.balance = before + change
    log = BalanceLog(user_id=user.id, type=log_type, before=before, after=user.balance)
    db.session.add(log)


@game_bp.route('/balance')
def balance():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'error': 'missing user_id'}), 400
    api_resp = api_get_balance(user_id)
    user = User.query.get(user_id)
    local = user.balance if user else None
    return jsonify({'api': api_resp, 'local': local})


@game_bp.route('/bet', methods=['POST'])
def bet():
    data = request.get_json() or {}
    user_id = data.get('user_id')
    amount = data.get('amount')
    if not user_id or amount is None:
        return jsonify({'error': 'missing fields'}), 400
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'user not found'}), 404
    api_resp = api_place_bet(user_id, amount)
    tx = Transaction(user_id=user_id, amount=amount, type='bet')
    db.session.add(tx)
    _update_balance(user, -amount, 'bet')
    # rebate for parent
    if user.parent:
        percent = current_app.config.get('REBATE_PERCENTAGE', 0)
        rebate = amount * percent
        parent_tx = Transaction(user_id=user.parent.id, amount=rebate, type='rebate')
        db.session.add(parent_tx)
        _update_balance(user.parent, rebate, 'rebate')
    db.session.commit()
    return jsonify(api_resp)


@game_bp.route('/win', methods=['POST'])
def win():
    data = request.get_json() or {}
    user_id = data.get('user_id')
    amount = data.get('amount')
    if not user_id or amount is None:
        return jsonify({'error': 'missing fields'}), 400
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'user not found'}), 404
    api_resp = api_send_win(user_id, amount)
    tx = Transaction(user_id=user_id, amount=amount, type='win')
    db.session.add(tx)
    _update_balance(user, amount, 'win')
    db.session.commit()
    return jsonify(api_resp)
