# Crypto Profit Calculator

A simple Python command-line tool that calculates how much profit
(and percent change) you would have made if you bought a cryptocurrency one year ago.

It uses **[CoinGecko’s public API](https://www.coingecko.com/en/api)**
to fetch real historical price data — NO API KEY REQUIRED!

You can also optionally specify an investment amount (in USD)
to see how much profit you would have earned on that investment.

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

- if use uv:
```bash
uv pip install -r pyproject.toml
```
---

##  Requirements
## Run with only a specific coin:

```bash
python3 main.py --btc
python3 main.py --xrp
python3 main.py --eth
```
## Example Output of specific coin:

Using coin api_id: bitcoin
Price one year ago: 61649.936 USD
Price now: 95480.422 USD
Profit per year: 33830.486 USD
Percent change per year: 54.88 %

## Run with a specific coin and include an investment amount (in USD):

```bash
python3 main.py --btc --100
python3 main.py --xrp --50
python3 main.py --eth --10
```

## Example Output of specific coin and include an investment amount (in USD):

Using coin api_id: bitcoin
Price one year ago: 61649.936 USD
Price now: 95480.422 USD
Profit per year: 33830.486 USD
Percent change per year: 54.88 %
Preliminary yearly profit on an investment of 100.0 USD: 54.88 USD

---

## License
This project is licensed under the MIT License.
You are free to use, modify, and distribute this script.
