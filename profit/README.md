# Crypto Profit Calculator

A simple Python command-line tool that calculates how much profit
(and percent change) you would have made if you bought a cryptocurrency one year ago.
It uses **[CoinGecko’s public API](https://www.coingecko.com/en/api)**
to fetch historical price data — no API key required!

---

## Features

- Fetches real crypto price history using the CoinGecko API
- Calculates profit/loss and percent change over 1 year
- Supports multiple coins (BTC, ETH, XRP, etc.)
- Easy command-line interface (`python3 main.py --btc`)
- Defaults to Bitcoin if no coin is provided

---

##  Requirements

- Python 3.8 or higher
- Internet connection

---

## Installation
## Install dependencies:

```bash
pip install -r requirements.txt
```

if uv:
```bash
uv pip install -r pyproject.toml

---

##  Requirements ## Run with a specific coin:
```bash
python3 main.py --btc
python3 main.py --xrp
python3 main.py --eth
```

## Example Output:
Using coin api_id: ripple
Price one year ago: 0.4942 USD
Price now: 2.0893 USD
Profit per year: 1.595 USD
Percent change: 323.04 %

---

## License
This project is licensed under the MIT License.
You are free to use, modify, and distribute this script.
