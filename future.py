# https://bybit-exchange.github.io/docs/v5/intro
# https://bybit-exchange.github.io/docs/api-explorer/v5/trade/create-order

import requests
import json
import time
import hmac
import hashlib
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')
RECV_WINDOW = '20000'

def generate_signature(secret, method, endpoint, time_stamp, data):
    if data is None:
        data = ""
    else:
        data = json.dumps(data)
    # signature_payload = f"{method}{endpoint}{expires}{data}"
    signature_payload = f"{time_stamp}{API_KEY}{RECV_WINDOW}{data}"
    # signature_payload= str(time_stamp) + endpoint + str(20000) + data
    return hmac.new(secret.encode(), signature_payload.encode(), hashlib.sha256).hexdigest()

# Set the API endpoint
ENDPOINT = "https://api.bybit.com"

# Set the API version
VERSION = "/v5"

# Set the HTTP request headers
# HEADERS = {
#     "Content-Type": "application/json",
#     "Accept": "application/json",
#     "Referer": "https://www.bybit.com/",
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
# }

HEADERS = {
  'X-BAPI-API-KEY': API_KEY,
  'X-BAPI-RECV-WINDOW': RECV_WINDOW,
  'Content-Type': 'application/json',
  'Accept': 'application/json'
}

# Define the function for sending HTTP request
def send_request(method, endpoint, params=None, data=None):
    # Set the API url
    url = ENDPOINT + VERSION + endpoint

    # Add the timestamp parameter
    # expires = int(time.time()*1000) + 60000

    time_stamp=str(int(time.time() * 10 ** 3))

    params = params or {}
    params["api_key"] = API_KEY
    params["timestamp"] = time_stamp

    # Generate the signature
    signature = generate_signature(API_SECRET, method, VERSION+endpoint, time_stamp, data)

    # Add the signature to the request headers
    headers = dict(HEADERS)
    headers["X-BAPI-SIGN"] = signature
    headers["X-BAPI-TIMESTAMP"] = time_stamp # str(int(time.time() * 1000))

    # Build the HTTP request
    req = requests.Request(method, url, headers=headers, params=params, json=data)
    prepped = req.prepare()

    # Send the HTTP request
    session = requests.Session()
    res = session.send(prepped)
    return res.json()

# Examples of HTTP requests
# Get the current BTCUSD price
payload = {'category': 'linear',
            'symbol': 'BTCUSD'
          }

price = send_request("GET", "/market/tickers", payload)
print(f"The current BTCUSD price: {price['result']['list'][0]['lastPrice']}")

# Get the user's wallet balance
# balance = send_request("GET", "/private/wallet/balance")
# print(f"The user's wallet balance: {balance['result'][0]['wallet_balance']}")

# Place a limit buy order for BTCUSD perpetual contract
payload = {
  "category": "linear",
  "symbol": "BTCUSDT",
  "isLeverage": 0,
  "side": "Buy",
  "orderType": "Market",
  "qty": "1",
  "price": "1000",
  "triggerPrice": None,
  "triggerDirection": None,
  "triggerBy": None,
  "orderFilter": None,
  "orderIv": None,
  "timeInForce": "GTC",
  "positionIdx": 1,  #0=one-way mode, 1=buy-hedge-mode, 2=sell-hedge-mode
  "orderLinkId": "test-xx1",
  "takeProfit": None,
  "stopLoss": None,
  "tpTriggerBy": None,
  "slTriggerBy": None,
  "reduceOnly": False,
  "closeOnTrigger": False,
  "mmp": None
}

order = send_request("POST", "/order/create", data=payload)
print(f"Order successfully placed: {json.dumps(order, indent=4)}")

# Cancel the order
# if order["ret_code"] == 0:
#     cancel = send_request("POST", "/private/order/cancel", data={
#         "order_id": order["result"]["order_id"],
#         "symbol": order["result"]["symbol"],
#     })
#     print(f"Order successfully canceled: {json.dumps(cancel, indent=4)}")
