import os
from dotenv import load_dotenv
import requests
from rich import print


load_dotenv(dotenv_path='.env')
virustotal_api_key = os.getenv('VIRUSTOTAL_API')
abuseipdb_api_key = os.getenv('ABUSEIPDB_API')


abuse_url = 'https://api.abuseipdb.com/api/v2/check'

querystring = {
    'ipAddress': '78.62.199.128',
    'maxAgeInDays': '90',
    'verbose': '',
}

headers = {
    'Accept': 'text/plain',
    #'Accept': 'application/json',
    'Key': abuseipdb_api_key
}

response = requests.request(method='GET', url=abuse_url, headers=headers, params=querystring)
print(response.text)



# Formatted output
#decodedResponse = json.loads(response.text)

#url = f"https://www.virustotal.com/{virustotal_api_key}/v3/ip_addresses/192.168.1.226"
#out = requests.get(url)

#print(out.text)
# "78.62.199.128"
# "192.168.1.226"
