import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("BINANCE_API_KEY")
BASE_URL = os.getenv("BINANCE_BASE_URL")

# Test endpoint: Get exchange info
url = f"{BASE_URL}/fapi/v1/exchangeInfo"
headers = {"X-MBX-APIKEY": API_KEY}

resp = requests.get(url, headers=headers)
print(resp.json())  # Should print symbol info for BTCUSDT, etc.

