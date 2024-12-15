import json
import whois
import logging
from datetime import datetime

# ANSI color codes
GREEN = "\033[92m"
RESET = "\033[0m"

def setup_logger():
    """Set up a logger to log messages with a simple format."""
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

def load_json_file(filename):
    """Load and return JSON data from a file."""
    with open(filename, 'r') as f:
        return json.load(f)

def check_domain(domain):
    """
    Check domain availability and expiration date using python-whois.
    
    Returns:
       (is_available, expiration_date)
       
    - is_available: True if the domain seems available, False if registered.
    - expiration_date: A datetime object or None if unavailable.
    """
    try:
        w = whois.whois(domain)
        
        # If 'domain_name' is missing or None, it might indicate the domain is available.
        if not w or (isinstance(w.domain_name, list) and not w.domain_name) or (w.domain_name is None):
            return True, None  # Domain likely available

        # If domain_name is present, it's likely registered.
        # Try to get expiration_date.
        expiration_date = w.expiration_date
        # expiration_date might be a single datetime or a list of datetimes
        if isinstance(expiration_date, list) and expiration_date:
            expiration_date = expiration_date[0]  # Take the first expiration date

        return False, expiration_date
    except whois.parser.PywhoisError:
        # This error is often raised when the domain is not found.
        return True, None
    except Exception:
        # Any other exceptions, assume domain is not available (or unknown)
        return False, None

def main():
    logger = setup_logger()

    # Load domains and extensions
    domains_data = load_json_file('domains.json')
    extensions_data = load_json_file('extensions.json')
    
    domains = domains_data.get('domains', [])
    extensions = extensions_data.get('extensions', [])

    # Combine domains and extensions
    full_domains = [f"{d}.{ext}" for d in domains for ext in extensions]

    # Check each domain
    for d in full_domains:
        is_available, expiration_date = check_domain(d)
        if is_available:
            logger.info(f"{GREEN}{d}: AVAILABLE{RESET}")
        else:
            if expiration_date:
                # Format expiration date nicely
                formatted_date = expiration_date.strftime("%Y-%m-%d") if isinstance(expiration_date, datetime) else str(expiration_date)
                logger.info(f"{d}: REGISTERED (Expires on {formatted_date})")
            else:
                logger.info(f"{d}: REGISTERED (Expiration date not found)")

if __name__ == "__main__":
    main()
