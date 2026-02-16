from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Literal


class TotalVotes(BaseModel):
    """Community votes about IP address."""
    harmless: int = 0
    malicious: int = 0


class AnalysisStats(BaseModel):
    """Summary statistics from all security engines."""
    malicious: int = Field(ge=0, description="Number of malicious detections")
    suspicious: int = Field(ge=0, description="Number of suspicious detections")
    undetected: int = Field(ge=0, description="Number of undetected by scanners")
    harmless: int = Field(ge=0, description="Number of harmless detections")
    timeout: int = Field(ge=0, description="Number of timeouts")


class EngineResult(BaseModel):
    """Individual security engine scan result."""
    method: str = Field(description="Detection method (e.g., 'blacklist')")
    engine_name: str = Field(description="Name of the security engine")
    category: Literal['undetected', 'malicious', 'suspicious', 'harmless', 'timeout']
    result: str = Field(description="Scan result (e.g., 'unrated', 'clean', 'malicious')")


class VirusTotalIP(BaseModel):
    """
    Complete VirusTotal IP address analysis result.

    This model represents all data returned by VirusTotal API v3
    when analyzing an IP address for security threats.

    Attributes:
        ip: IP address that was analyzed
        reputation: Reputation score (typically -100 to 100, where negative is bad)
        last_analysis_stats: Summary of detection statistics
        last_analysis_results: Detailed results from each security engine
        network: IP network range (CIDR notation)
        country: Two-letter country code
        continent: Two-letter continent code
        asn: Autonomous System Number
        as_owner: Organization that owns the AS
        regional_internet_registry: RIR that manages this IP range
        whois: Complete WHOIS information
        whois_date: WHOIS data timestamp (Unix epoch)
        last_analysis_date: Last scan timestamp (Unix epoch)
        last_modification_date: Last data update timestamp (Unix epoch)
        total_votes: Community votes about this IP
        tags: Security tags applied to this IP
    """
    ip: str = Field(description="IP address")
    reputation: int = Field(description="Reputation score")
    last_analysis_stats: AnalysisStats
    last_analysis_results: Dict[str, EngineResult] = Field(
        default_factory=dict,
        description="Detailed results from each security engine"
    )

    # Network information
    network: Optional[str] = Field(None, description="Network range in CIDR notation")
    country: Optional[str] = Field(None, description="Country code (ISO 3166-1 alpha-2)")
    continent: Optional[str] = Field(None, description="Continent code")
    asn: Optional[int] = Field(None, description="Autonomous System Number")
    as_owner: Optional[str] = Field(None, description="AS owner organization name")
    regional_internet_registry: Optional[str] = Field(None, description="Regional Internet Registry")

    # WHOIS data
    whois: Optional[str] = Field(None, description="Complete WHOIS information")
    whois_date: Optional[int] = Field(None, description="WHOIS timestamp (Unix epoch)")

    # Analysis metadata
    last_analysis_date: Optional[int] = Field(None, description="Last analysis timestamp (Unix epoch)")
    last_modification_date: Optional[int] = Field(None, description="Last modification timestamp (Unix epoch)")

    # Community data
    total_votes: Optional[TotalVotes] = Field(None, description="Community votes")
    tags: Optional[List[str]] = Field(default_factory=list, description="Security tags")

    class Config:
            """Pydantic configuration."""
            json_schema_extra = {
                "example": {
                    "ip": "78.62.199.128",
                    "reputation": 0,
                    "last_analysis_stats": {
                        "malicious": 0,
                        "suspicious": 0,
                        "undetected": 93,
                        "harmless": 0,
                        "timeout": 0
                    },
                    "country": "LT",
                    "asn": 8764,
                    "as_owner": "Telia Lietuva, AB"
                }
            }

    def is_malicious(self) -> bool:
        """Check if IP is flagged as malicious by any engine."""
        return self.last_analysis_stats.malicious > 0

    def is_suspicious(self) -> bool:
        """Check if IP is flagged as suspicious by any engine."""
        return self.last_analysis_stats.suspicious > 0

    def is_clean(self) -> bool:
        """Check if IP has no malicious or suspicious detections."""
        return (self.last_analysis_stats.malicious == 0 and
                self.last_analysis_stats.suspicious == 0)

    def get_malicious_engines(self) -> List[str]:
        """Get list of engines that flagged this IP as malicious."""
        return [
            engine_name
            for engine_name, result in self.last_analysis_results.items()
            if result.category == 'malicious'
        ]

    def get_suspicious_engines(self) -> List[str]:
        """Get list of engines that flagged this IP as suspicious."""
        return [
            engine_name
            for engine_name, result in self.last_analysis_results.items()
            if result.category == 'suspicious'
        ]
