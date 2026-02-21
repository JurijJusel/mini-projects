import socket


def clean_domain(domain: str) -> str:
    """
    Remove common URL components from domain string.
    Args:
        domain: Domain string to clean (e.g., 'https://www.google.com/')
    Returns:
        str: Cleaned domain name, or empty string if invalid
    Example:
        clean_domain("https://www.google.com/") -> 'google.com'
    """
    try:
        if domain is None:
            print("Warning: Domain is None")
            return ""

        if not isinstance(domain, str):
            print(f"Warning: Expected string, got {type(domain).__name__}")
            return ""

        domain = domain.strip().lower()

        if not domain:
            return ""

        domain = domain.replace('http://', '').replace('https://', '')

        if domain.startswith('www.'):
            domain = domain[4:]

        if '/' in domain:
            domain = domain.split('/')[0]

        domain = domain.rstrip('.')

        return domain

    except Exception as e:
        print(f"❌ Unexpected error cleaning domain '{domain}': {e}")
        return ""


def domain_to_ip(domain: str) -> str:
    """
    Resolve domain name to IP address.
    Args:
        domain: Domain name (e.g., 'google.com')
    Returns:
        str: IP address
    Example:
        ip = domain_to_ip('google.com')
        print(ip)  # '142.250.185.46'
    """
    try:
        domain = clean_domain(domain)
        print(f"Resolving domain: {domain}")

        ip_address = socket.gethostbyname(domain)
        return ip_address
    except socket.gaierror as e:
        print(f"Failed to resolve domain {domain}: {e}")
        return None

    except Exception as e:
        print(f"❌ Unexpected error resolving '{domain}': {e}")
        return None


if __name__ == "__main__":
    domain = "https://www.skelbiu.lt/skelbimai"
    ip = domain_to_ip(domain)
    print(f"{domain} → {ip}")

# https://www.skelbiu.lt/
# "https://www.google.com/"
# "https://www.example.com/path/to/page"
# "youtube.com/watch?v=123"
# "  WWW.SKELBIU.LT/skelbimai  "
# "https://api.github.com/users"
