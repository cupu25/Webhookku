import json, config
from flask import Flask, request, jsonify, render_template
from binance.cm_futures import CMFutures
from binance.lib.utils import config_logging
from binance.error import ClientError
from binance.client import Client
from binance.enums import *
import ssl
import requests


app = Flask(__name__)


API_KEY = 'DV5uON51MNenChwzxHywR03HBWyT2ncWCVxljs3cdS6WvveTqmaiZyqTqdOi2I7f'
API_SECRET = 'TkJUUld24MAtobhuJT9jReFW8wkXoPq5E14D8k14rCLg2S5eB8CrodfNJRguokbO'
client = Client(API_KEY, API_SECRET)

def order(symbol, side, quantity):
    try:
        order = client.futures_create_order(symbol=symbol, side=side, type='MARKET', quantity=quantity)
    except Exception as e:
        print("an exception occured - {}".format(e))
        return False

    return order

@app.route('/')
def welcome():
    return render_template('index.html')

@app.route('/webhook', methods=['POST'])
def webhook():
    #print(request.data)
    data = json.loads(request.data)
    
    if data[3] != config.WEBHOOK_PASSPHRASE:
        return {
            "code": "error",
            "message": "Nice try, invalid passphrase"
        }

    symbol = data[0].upper()
    side = data[1].upper()
    quantity = data[2]
   
    order_response = order(symbol, side, quantity)
    if order_response:
        return {
            "code": "success",
            "message": "order executed"
        }
    else:
        print("order failed")

        return {
            "code": "error",
            "message": "order failed"
        }
