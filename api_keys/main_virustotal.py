from pathlib import Path
import os
from dotenv import load_dotenv
import requests
from rich import print

load_dotenv(dotenv_path=Path(__file__).parent / '.env')
virustotal_api_key = os.getenv('VIRUSTOTAL_API')


API_KEY = virustotal_api_key  # iš https://www.virustotal.com/gui/my-apikey
IP_ADDRESS = "78.62.199.128"


def check_ip_virustotal(ip: str):
    """
    Tikrina IP reputaciją per VirusTotal API.
    """
    url = f"https://www.virustotal.com/api/v3/ip_addresses/{ip}"
    headers = {
        "x-apikey": API_KEY
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        # Naudingi laukeliai iš API
        analysis = data.get('data', {}).get('attributes', {}).get('last_analysis_stats', {})
        reputation = data.get('data', {}).get('attributes', {}).get('reputation', None)
        attributes = data.get('data', {}).get('attributes', {})

        print(f"✅ Visa info apie IP: {ip}\\n")
        for key, value in attributes.items():
            print(f"{key}: {value}\\n")

        # return attributes
        return {
            'ip': ip,
            'reputation': reputation,
            'last_analysis_stats': analysis
        }

    except requests.exceptions.RequestException as e:
        print(f"[ERROR] VirusTotal IP tikrinimas nepavyko: {e}")
        return {"error": str(e)}

# Pavyzdys:
if __name__ == "__main__":
    ip_data = check_ip_virustotal(IP_ADDRESS)
    print(ip_data)
