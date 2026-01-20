import os
from pathlib import Path
import requests
from ip_list import ip_addresses
from abuseip_model import AbuseModel
from rich import print

from dotenv import load_dotenv
load_dotenv(dotenv_path=Path(__file__).parent / '.env')


def get_info_from_ip(ip_address, api_key_abuse, abuse_url):
    """
    Check IP address using AbuseIPDB API
    Args:
        ip_address: IP address to check
        api_key_abuse: API key for AbuseIPDB
        abuse_url: AbuseIPDB API URL
     Returns:
        dict: Results from API for the IP address or None if error occurs
    """
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
        data = response.json()
        return data

    except requests.exceptions.RequestException as e:
        print(f"Error checking IP {ip_address}: {e}")
        return None


def transform_to_abuse_model(data: dict) -> AbuseModel:
    """
    Transform AbuseIPDB API response to structured AbuseModel from
        def get_info_from_ip()
    Args:
        data: Full API response with 'data' key
    Returns:
        AbuseModel: Structured data or None if transformation fails
    """
    try:
        api_data = data['data']

        structured_data = {
            "ip-identity": {
                "ipAddress": api_data['ipAddress'],
                "ipVersion": api_data['ipVersion'],
                "isPublic": api_data['isPublic']
            },
            "network": {
                "isp": api_data['isp'],
                "domain": api_data['domain'],
                "hostnames": api_data['hostnames'],
                "usageType": api_data['usageType']
            },
            "geolocation": {
                "countryCode": api_data['countryCode'],
                "countryName": api_data['countryName']
            },
            "reputation": {
                "abuseConfidenceScore": api_data['abuseConfidenceScore'],
                "isWhitelisted": api_data['isWhitelisted'],
                "isTor": api_data['isTor']
            },
            "abuse-history": {
                "totalReports": api_data['totalReports'],
                "numDistinctUsers": api_data['numDistinctUsers'],
                "lastReportedAt": api_data['lastReportedAt'],
                "reports": api_data['reports']
            }
        }

        return AbuseModel(**structured_data)

    except Exception as e:
        ip_addr = data.get('data', {}).get('ipAddress', 'Unknown')
        print(f"Error transforming data for IP {ip_addr}: {e}")
        return None


def get_info_from_ips_list(ip_list, api_key_abuse, abuse_url):
    """
    Check multiple IP addresses using AbuseIPDB API
    Args:
        ip_list: List of IP addresses to check
        api_key_abuse: API key for AbuseIPDB
        abuse_url: AbuseIPDB API URL
    Returns:
        list: List of structured data for each successfully processed IP address
    """
    collected_data = []

    for ip_address in ip_list:
        first_data = get_info_from_ip(ip_address, api_key_abuse, abuse_url)

        if first_data is None:
            continue

        abuse_data = transform_to_abuse_model(first_data)

        if abuse_data is None:
            continue

        collected_data.append(abuse_data.model_dump(by_alias=True))

    return collected_data


def check_abuseipdb_key(api_key, abuse_url):
    """
    Validate AbuseIPDB API key by making a test request.
    Args:
        api_key (str): AbuseIPDB API key from environment variables.
        abuse_url (str): AbuseIPDB API endpoint URL.
    Returns:
        bool: True if API key is valid, False otherwise.
    Raises:
        None: All exceptions are caught and handled internally.
    Example:
        api_key = os.getenv('ABUSEIPDB_API')
        abuse_url = 'https://api.abuseipdb.com/api/v2/check'
        is_valid = check_abuseipdb_key(api_key, abuse_url)
    """
    try:
        if not api_key:
            print("AbuseIPDB API key not found in environment variables")
            return False

        # Simple validation with a test request
        headers = {
            'Key': api_key,
            'Accept': 'application/json',
        }

        querystring = {
            'ipAddress': '8.8.8.8',
            'maxAgeInDays': '90',
            'verbose': '',
        }

        response = requests.get(url=abuse_url, headers=headers, params=querystring, timeout=10)

        if response.status_code == 401:
            print("AbuseIPDB API key is invalid or expired")
            return False
        elif response.status_code == 504:
            print("AbuseIPDB API timeout - server not responding")
            return False
        elif response.status_code != 200:
            print(f"AbuseIPDB API returned status code: {response.status_code}")
            return False

        return True

    except requests.exceptions.Timeout:
        print("Request to AbuseIPDB API timed out")
        return False
    except requests.exceptions.RequestException as e:
        print(f"Failed to validate AbuseIPDB API: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False


if __name__ == "__main__":
    api_key = os.getenv('ABUSEIPDB_API')
    abuse_api_url = 'https://api.abuseipdb.com/api/v2/check'
    abuse_api_key_check = check_abuseipdb_key(api_key, abuse_api_url)

    if abuse_api_key_check:
        results_list = get_info_from_ips_list(ip_addresses, api_key, abuse_url=abuse_api_url)
        print(results_list)
    else:
        print("AbuseIPDB API key is not valid. Please check your '.env' file.")
