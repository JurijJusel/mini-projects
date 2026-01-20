from __future__ import annotations
from typing import Any, List, Optional
from pydantic import BaseModel, Field


class IpIdentity(BaseModel):
    ipAddress: str
    ipVersion: int
    isPublic: bool


class Network(BaseModel):
    isp: str
    domain: str
    hostnames: List[str]
    usageType: str


class Geolocation(BaseModel):
    countryCode: str
    countryName: str


class Reputation(BaseModel):
    abuseConfidenceScore: int
    isWhitelisted: Any
    isTor: bool


class History(BaseModel):
    totalReports: int
    numDistinctUsers: int
    lastReportedAt: Any
    reports: List


class AbuseModel(BaseModel):
    ip_identity: IpIdentity = Field(..., alias='ip-identity')
    network: Network
    geolocation: Geolocation
    reputation: Reputation
    abuse_history: History = Field(..., alias='abuse-history')



# Input data example from AbuseIPDB API
"""
{
    'data': {
        'ipAddress': '78.62.199.128',
        'isPublic': True,
        'ipVersion': 4,
        'isWhitelisted': None,
        'abuseConfidenceScore': 0,
        'countryCode': 'LT',
        'usageType': 'Fixed Line ISP',
        'isp': 'Telia Lietuva, AB',
        'domain': 'telia.lt',
        'hostnames': ['78-62-199-128.static.zebra.lt'],
        'isTor': False,
        'countryName': 'Lithuania',
        'totalReports': 0,
        'numDistinctUsers': 0,
        'lastReportedAt': None,
        'reports': []
    }
}
"""

# model output from AbuseModel
"""
{
    "ip-identity": {
        "ipAddress": "78.62.199.128",
        "ipVersion": 4,
        "isPublic": true
    },
    "network": {
        "isp": "Telia Lietuva, AB",
        "domain": "telia.lt",
        "hostnames": ["78-62-199-128.static.zebra.lt"],
        "usageType": "Fixed Line ISP"
    },
    "geolocation": {
        "countryCode": "LT",
        "countryName": "Lithuania"
    },
    "reputation": {
        "abuseConfidenceScore": 0,
        "isWhitelisted": null,
        "isTor": false
    },
    "abuse-history": {
        "totalReports": 0,
        "numDistinctUsers": 0,
        "lastReportedAt": null,
        "reports": []
    }
}
"""
