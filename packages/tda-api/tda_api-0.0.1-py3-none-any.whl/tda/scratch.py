import datetime
import json

import client
from client import Client


def print_json(obj, stack=None):
    if stack is None:
        stack = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            stack.append('"{}"'.format(k))
            print_json(v, stack)
            stack.pop()
    elif isinstance(obj, list):
        for idx in range(len(obj)):
            stack.append(idx)
            print_json(obj[idx], stack)
            stack.pop()
    else:
        if isinstance(obj, str):
            fmt_obj = '"{}"'.format(obj)
        else:
            fmt_obj = obj
        print(''.join('[{}]'.format(k) for k in stack), fmt_obj)


if __name__ == '__main__':
    token_path = '/Volumes/alexgolectest/token.json'
    api_key = 'X5MUWQRRG9SMBQROM8I8FYAESQNJKHNP@AMER.OAUTHAP'
    redirect_uri = 'https://localhost:10169'
    try:
        c = client.client_from_token_file(token_path, api_key)
    except FileNotFoundError:
        from selenium import webdriver
        with webdriver.Chrome() as driver:
            c = client.client_from_login_flow(
                driver, api_key, redirect_uri, token_path)

    account_id = 498824686
    order = {
        'orderType': 'MARKET',
        'session': 'NORMAL',
        'duration': 'DAY',
        'orderStrategyType': 'SINGLE',
        'orderLegCollection': [{
            'instruction': 'Buy',
            'quantity': 15,
            'instrument': {
                    'symbol': 'AAPL',
                    'assetType': 'EQUITY'
            }
        }]
    }

    resp = c.get_quote('AAPL')
    assert resp.ok
    print_json(resp.json())

