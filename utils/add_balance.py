import requests

from utils.read_conf import read_conf


def add_balance(amount,user_id):
    url = "http://127.0.0.1:5050/add_balance"
    headers = {"Authorization": f'Bearer {read_conf("headers", "root_token")}'}
    json = {
        "amount": amount,
        "user_id": user_id
    }
    resp = requests.post(url, json=json, headers=headers)
    return resp