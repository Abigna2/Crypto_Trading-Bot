import os
import time
import hmac
import hashlib
from urllib.parse import urlencode
import requests
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Mock mode toggle for safe submission
MOCK = os.getenv("BOT_MOCK_MODE", "True").lower() == "true"

API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_API_SECRET").encode() if os.getenv("BINANCE_API_SECRET") else b"dummysecret"
BASE_URL = os.getenv("BINANCE_BASE_URL", "https://testnet.binancefuture.com")
LOG_FILE = os.getenv("BOT_LOG_FILE", "basic_bot.log")

print("=== Crypto Trading Bot ===")
print("MOCK MODE:", MOCK)
print("BASE_URL:", BASE_URL)
print("API_KEY:", (API_KEY[:5] + "...") if API_KEY else "None")
print("API_SECRET length:", len(API_SECRET))

# Logging
logging.basicConfig(filename=LOG_FILE, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

class BasicBot:
    def __init__(self, api_key, api_secret, base_url):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({"X-MBX-APIKEY": api_key})

    def _sign_payload(self, payload):
        payload['timestamp'] = int(time.time() * 1000)
        query_string = urlencode(payload, doseq=True)
        signature = hmac.new(self.api_secret, query_string.encode(), hashlib.sha256).hexdigest()
        return f"{query_string}&signature={signature}"

    def _signed_request(self, method, endpoint, payload=None):
        payload = payload or {}
        full_query = self._sign_payload(payload)
        url = f"{self.base_url}{endpoint}?{full_query}"
        try:
            if MOCK:
                logger.info(f"[MOCK] POST request to {endpoint} with payload {payload}")
                print(f"[MOCK] POST request to {endpoint} with payload {payload}")
                mock_response = {
                    'symbol': payload.get('symbol', 'N/A'),
                    'orderId': 123456,
                    'status': 'FILLED',
                    'side': payload.get('side', 'BUY'),
                    'type': payload.get('type', 'MARKET'),
                    'price': payload.get('price', '30000'),
                    'origQty': payload.get('quantity', 0),
                    'executedQty': payload.get('quantity', 0)
                }
                logger.info(f"[MOCK RESPONSE]: {mock_response}")
                print(f"[MOCK RESPONSE]: {mock_response}")
                return mock_response
            else:
                if method.upper() == "POST":
                    resp = self.session.post(url)
                else:
                    resp = self.session.get(url)
                resp.raise_for_status()
                data = resp.json()
                logger.info(f"Request: {url} Response: {data}")
                print("Response:", data)
                return data
        except Exception as e:
            print(f"Error: {e}")
            logger.error(f"Error: {e}")
            return None

    # Order functions
    def place_market_order(self, symbol, side, quantity):
        payload = {"symbol": symbol.upper(), "side": side.upper(), "type": "MARKET", "quantity": quantity}
        return self._signed_request("POST", "/fapi/v1/order", payload)

    def place_limit_order(self, symbol, side, quantity, price):
        payload = {
            "symbol": symbol.upper(),
            "side": side.upper(),
            "type": "LIMIT",
            "timeInForce": "GTC",
            "quantity": quantity,
            "price": price
        }
        return self._signed_request("POST", "/fapi/v1/order", payload)

    def place_stop_limit_order(self, symbol, side, quantity, stop_price, price):
        payload = {
            "symbol": symbol.upper(),
            "side": side.upper(),
            "type": "STOP_MARKET",
            "quantity": quantity,
            "stopPrice": stop_price,
            "price": price
        }
        return self._signed_request("POST", "/fapi/v1/order", payload)


# ===== Menu-driven CLI =====
if __name__ == "__main__":
    bot = BasicBot(API_KEY, API_SECRET, BASE_URL)
    
    while True:
        print("\n=== Menu ===")
        print("1. Market Order")
        print("2. Limit Order")
        print("3. Stop-Limit Order")
        print("4. Exit")
        choice = input("Enter choice (1-4): ").strip()
        
        if choice == "4":
            print("Exiting...")
            break
        elif choice not in {"1","2","3"}:
            print("Invalid choice. Try again.")
            continue
        
        symbol = input("Enter symbol (e.g., BTCUSDT): ").strip().upper()
        side = input("Enter side (BUY/SELL): ").strip().upper()
        quantity = float(input("Enter quantity: ").strip())
        
        if choice == "1":
            res = bot.place_market_order(symbol, side, quantity)
        elif choice == "2":
            price = float(input("Enter limit price: ").strip())
            res = bot.place_limit_order(symbol, side, quantity, price)
        else:
            stop_price = float(input("Enter stop price: ").strip())
            price = float(input("Enter limit price: ").strip())
            res = bot.place_stop_limit_order(symbol, side, quantity, stop_price, price)
        
        if res is None:
            print("Order failed. Check log for details.")
        else:
            print(f"Order executed: {res['status']} | ID: {res['orderId']}")
