import json, config
from flask import Flask, request, jsonify, render_template
from binance.client import Client
import requests


app = Flask(__name__)


client = Client()

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
