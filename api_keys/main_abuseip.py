import os
from pathlib import Path
from dotenv import load_dotenv
import requests
from rich import print
from ip_list import ip_addresses

load_dotenv(dotenv_path=Path(__file__).parent / '.env')
abuseipdb_api_key = os.getenv('ABUSEIPDB_API')

abuse_api_url = 'https://api.abuseipdb.com/api/v2/check'


def get_info_from_ip(ip_addresses, api_key_abuse, abuse_url):
    """
    Check IP addresses using AbuseIPDB API
    Args:
        ip_addresses: List of IP addresses to check
    Returns:
        list: Results from API for each IP address
    """
    collected_data = []

    for ip_address in ip_addresses:
        try:
            querystring = {
                'ipAddress': ip_address,
                'maxAgeInDays': '90',
                'verbose': '',
            }

            headers = {
                'Accept': 'application/json',
                'Key': api_key_abuse
            }

            response = requests.get(url=abuse_url, headers=headers, params=querystring)
            response.raise_for_status()

            collected_data.append({**response.json()})

        except requests.exceptions.RequestException as e:
            print(f"Error checking IP {ip_address}: {e}")
            collected_data.append({
                'ip': ip_address,
                'error': str(e)
            })

    return collected_data


if __name__ == "__main__":
    results = get_info_from_ip(ip_addresses, abuseipdb_api_key, abuse_url=abuse_api_url)
    print(results)
