import os
import requests
from pathlib import Path
from typing import Optional, List, Dict
from virustotal_model import VirusTotalIP
from ip_list import ip_addresses
from rich import print

from dotenv import load_dotenv
load_dotenv(dotenv_path=Path(__file__).parent / '.env')


def check_virustotal_key(api_key: str) -> bool:
    """Validate VirusTotal API key by making a test request."""
    try:
        if not api_key:
            print("VirusTotal API key not found in environment variables")
            return False

        url = "https://www.virustotal.com/api/v3/ip_addresses/8.8.8.8"
        headers = {
            'x-apikey': api_key,
            'Accept': 'application/json',
        }

        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code == 401:
            print("VirusTotal API key is invalid or expired")
            return False
        elif response.status_code != 200:
            print(f"VirusTotal API returned status code: {response.status_code}")
            return False

        return True

    except Exception as e:
        print(f"Failed to validate VirusTotal API: {e}")
        return False


def check_ip_virustotal(ip: str, api_key: str) -> Optional[VirusTotalIP]:
    """Check IP reputation via VirusTotal API v3."""
    url = f"https://www.virustotal.com/api/v3/ip_addresses/{ip}"
    headers = {
        "x-apikey": api_key,
        "Accept": "application/json"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        data = response.json()
        attributes = data.get('data', {}).get('attributes', {})

        if not attributes:
            print(f"[WARNING] No data returned for IP: {ip}")
            return None

        # Paruošiam duomenis Pydantic modeliui
        vt_data = {
            'ip': ip,
            'reputation': attributes.get('reputation', 0),
            'last_analysis_stats': attributes.get('last_analysis_stats', {}),
            'last_analysis_results': attributes.get('last_analysis_results', {}),
            'network': attributes.get('network'),
            'country': attributes.get('country'),
            'continent': attributes.get('continent'),
            'asn': attributes.get('asn'),
            'as_owner': attributes.get('as_owner'),
            'regional_internet_registry': attributes.get('regional_internet_registry'),
            'whois': attributes.get('whois'),
            'whois_date': attributes.get('whois_date'),
            'last_analysis_date': attributes.get('last_analysis_date'),
            'last_modification_date': attributes.get('last_modification_date'),
            'total_votes': attributes.get('total_votes', {'harmless': 0, 'malicious': 0}),
            'tags': attributes.get('tags', [])
        }

        # Sukuriam Pydantic modelį
        return VirusTotalIP(**vt_data)

    except Exception as e:
        print(f"[ERROR] Failed to check IP {ip}: {e}")
        return None


def get_virustotal_info_from_ips_list(ip_list: List[str], api_key: str) -> List[Dict]:
    """
    Check multiple IP addresses using VirusTotal API.
    Args:
        ip_list: List of IP addresses to check
        api_key: API key for VirusTotal
    Returns:
        list: List of VirusTotalIP models converted to dictionaries
    """
    collected_data = []

    for ip_address in ip_list:
        vt_result = check_ip_virustotal(ip_address, api_key)

        if vt_result is None:
            continue

        collected_data.append(vt_result.model_dump(exclude_none=True))

    return collected_data


if __name__ == "__main__":
    virustotal_api_key = os.getenv('VIRUSTOTAL_API')

    vt_api_key_check = check_virustotal_key(virustotal_api_key)

    if vt_api_key_check:
        results = get_virustotal_info_from_ips_list(ip_addresses, virustotal_api_key)
        print(results)
    else:
        print("VirusTotal API key is not valid. Please check your '.env' file.")

