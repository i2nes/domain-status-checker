import json
import whois
from datetime import datetime

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
        # It's safer to mark as registered without expiration date, or you could handle differently.
        return False, None

def main():
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
            print(f"{d}: AVAILABLE")
        else:
            if expiration_date:
                # Format expiration date nicely
                formatted_date = expiration_date.strftime("%Y-%m-%d") if isinstance(expiration_date, datetime) else str(expiration_date)
                print(f"{d}: REGISTERED (Expires on {formatted_date})")
            else:
                print(f"{d}: REGISTERED (Expiration date not found)")

if __name__ == "__main__":
    main()
