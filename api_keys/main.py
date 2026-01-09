import os
from pathlib import Path
from dotenv import load_dotenv
import requests
from rich import print


load_dotenv(dotenv_path=Path(__file__).parent / '.env')
abuseipdb_api_key = os.getenv('ABUSEIPDB_API')


abuse_url = 'https://api.abuseipdb.com/api/v2/check'

querystring = {
    'ipAddress': '78.62.199.128',
    'maxAgeInDays': '90',
    'verbose': '',
}

headers = {
    'Accept': 'text/plain',
    'Accept': 'application/json',
    'Key': abuseipdb_api_key
}

response = requests.request(method='GET', url=abuse_url, headers=headers, params=querystring)
print(response.text)



# "78.62.199.128"
# "192.168.1.226"
