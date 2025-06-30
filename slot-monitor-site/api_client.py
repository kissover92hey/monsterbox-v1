import requests
from flask import current_app

BASE_URL = 'https://example.com/api'


def send_request(endpoint, payload):
    headers = {'Authorization': f"Bearer {current_app.config['API_TOKEN']}"}
    resp = requests.post(f"{BASE_URL}/{endpoint}", json=payload, headers=headers, timeout=5)
    resp.raise_for_status()
    return resp.json()


def get_balance(user_id):
    return send_request('balance', {'user_id': user_id})


def place_bet(user_id, amount):
    return send_request('bet', {'user_id': user_id, 'amount': amount})


def send_win(user_id, amount):
    return send_request('win', {'user_id': user_id, 'amount': amount})
