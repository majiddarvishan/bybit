import requests
import time
import hashlib
import hmac
import json

# Replace with your Bybit API Keys
api_key = 'insert_your_api_key'
api_secret = 'insert_your_api_secret'

# Create the authentication parameters
timestamp = str(int(time.time() * 1000))
sign_str = f"POST/api/v2/private/order/create{timestamp}"
signature = hmac.new(api_secret.encode(), sign_str.encode(), hashlib.sha256).hexdigest()

# Define the order parameters
symbol = 'BTCUSD' # Replace with your desired trading pair
side = 'Buy' # Buy or Sell
order_type = 'Limit' # Market or Limit
qty = 0.01 # Quantity
price = 50000 # Price

# Define the API endpoint and headers
endpoint = 'https://api.bybit.com/v2/private/order/create'
headers = {
    'Content-Type': 'application/json',
    'api-key': api_key,
    'timestamp': timestamp,
    'sign': signature
}

# Define the API request parameters
params = {
    'symbol': symbol,
    'side': side,
    'order_type': order_type,
    'qty': qty,
    'price': price
}

# Send the API request
response = requests.post(endpoint, params=json.dumps(params), headers=headers)

# Print the API response
print(response.text)
