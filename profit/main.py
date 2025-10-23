from constants import coins_list
from utils import time_stamp, time_stamp_minus_one_year
import requests
import sys


def get_coin_id(coin_arg: str) -> str:
    """
    Prompt the user to enter a cryptocurrency name or symbol and return its from
    constaants.py coins_list the corresponding from CoinGecko.

    Returns:
        str: The CoinGecko ID of the selected coin, or 'bitcoin' if not found.
    """
    coin_arg = coin_arg.lower()
    try:
        for coin in coins_list:
            if coin['name'].lower() == coin_arg or coin['symbol'].lower() == coin_arg:
                return coin['id'].lower()

        print(f"Coin '{coin_arg}' not found. Defaulting to Bitcoin.")
        return 'bitcoin'

    except Exception as e:
        print(f"An error occurred: {e}. Defaulting to Bitcoin.")
        return 'bitcoin'


def get_prices_at_timestamp(coin_id: str) -> dict:
    """
    Fetch historical market data for a given coin over the last year.

    Args:
        coin_id (str): CoinGecko coin ID (e.g., 'bitcoin', 'ripple', 'ethereum').

    Returns:
        dict: Parsed JSON data containing price history between the two timestamps.
        output: {'prices': [[1729641600000, 62379.86708703343], [1729728000000, 61857.31577287963],
        [1729814400000, 62996.90492256556], [1729900800000, 61649.93632490859],
        [1729987200000, 62050.376516974386], [1730073600000, 62938.34448352703]}
    """
    date_now = time_stamp()
    date_minus_one_year = time_stamp_minus_one_year()

    url = (
        f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart/range"
        f"?vs_currency=eur&from={date_minus_one_year}&to={date_now}"
    )

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from CoinGecko.com: {e}")
        return


def calculate_profit(data: dict) -> None:
    """
    Calculate and print profit and percent change based on price data.
    Args:
        data (dict): Dictionary containing price history with timestamps.
    """
    if not data or 'prices' not in data or len(data['prices']) < 2:
        print("Not enough price data to calculate profit.")
        return

    price_one_year_ago = data['prices'][0][1]
    price_now = data['prices'][-1][1]

    profit = round(price_now - price_one_year_ago, 3)
    percent_change = round((profit / price_one_year_ago) * 100, 2)

    print(f"Price one year ago: {price_one_year_ago:.3f} USD")
    print(f"Price now: {price_now:.3f} USD")
    print(f"Profit per year: {profit:.3f} USD")
    print(f"Percent change per year: {percent_change:.2f} %")


def main():
    coin_arg = 'btc'
    args = sys.argv[1:]
    for arg in args:
        if arg.startswith('--'):
            coin_arg = arg[2:]  # remove '--'
            break

    coin_id = get_coin_id(coin_arg)
    print(f"Using coin api_id: {coin_id}")

    data = get_prices_at_timestamp(coin_id)
    calculate_profit(data)


if __name__ == "__main__":
    main()
