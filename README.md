# Crypto Trading Bot – Binance Futures Testnet

## Overview
This is a **Python-based trading bot** for Binance Futures Testnet (USDT-M).  
It supports **Market, Limit, and Stop-Limit orders** with **buy/sell sides** and a simple CLI interface.  

The bot is designed for **educational and testing purposes** and includes a **mock mode** to safely simulate orders without using real funds.

---

## Features
- Place **Market orders**
- Place **Limit orders**
- Place **Stop-Limit orders**
- Menu-driven **CLI interface**
- **Logging** of requests, responses, and errors
- **Mock mode** for safe testing

---

## Setup Instructions

1. **Clone the repository** or download the project folder.

2. **Create a virtual environment** and activate it:
   ```bash
   python -m venv venv
   .\venv\Scripts\Activate   # Windows
   source venv/bin/activate  # Linux/Mac
3. Install dependencies
    pip install -r requirements.txt
4. Configure environment variables

Copy .env.example to .env

Fill in your Binance Testnet API keys

BINANCE_API_KEY=your_testnet_api_key
BINANCE_API_SECRET=your_testnet_api_secret
BINANCE_BASE_URL=https://testnet.binancefuture.com
BOT_LOG_FILE=basic_bot.log
BOT_MOCK_MODE=True   # Set to False only if using real Testnet keys

5. Run the bot:
   python basic_bot.py

6. Tech Stack

Python 3.11.2

requests – for HTTP API calls

python-dotenv – for environment variables

Binance Futures Testnet REST API
