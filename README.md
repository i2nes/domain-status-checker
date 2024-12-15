# Domain Availability and Expiration Checker

This Python script checks if a given domain (or set of domains) is available and, if registered, retrieves its expiration date using the [`python-whois`](https://pypi.org/project/python-whois/) library.

## Features

- **Multiple Domain Extensions**: Easily combine a base domain name with multiple extensions.
- **JSON-Based Configuration**: Domains and extensions are sourced from `domains.json` and `extensions.json` for flexibility and ease of update.
- **Expiration Date Retrieval**: For registered domains, the script attempts to fetch the expiration date.
- **Availability Check**: Domains that are not found through WHOIS are deemed available.

## Requirements

- **Python 3.6+**
- [`python-whois`](https://pypi.org/project/python-whois/)
- A JSON file containing domain names (`domains.json`)
- A JSON file containing domain extensions (`extensions.json`)

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/i2nes/domain-status-checker.git
   cd domain-status-checker
   ```

2. **Install Dependencies**

   Use `pip` to install the required packages:
   ```bash
   pip install python-whois
   ```

## Usage

1. **Prepare Input Files**

   - `domains.json`:
     ```json
     {
       "domains": [
         "example",
         "testDomain"
       ]
     }
     ```

   - `extensions.json`:
     ```json
     {
       "extensions": [
         "com",
         "net"
       ]
     }
     ```

   Place these two files (`domains.json` and `extensions.json`) in the same directory as the script.

2. **Run the Script**

   Simply run:
   ```bash
   python check_domains.py
   ```

   The script will:
   - Load the domain base names and extensions.
   - Generate full domain names (e.g., `example.com`, `example.net`, `testDomain.com`, `testDomain.net`).
   - Query each domain’s WHOIS information.
   - Print availability and expiration status to the console.

## Example Output

For a domain like `example.com`, you might see:

- If available:  
  ```
  example.com: AVAILABLE
  ```

- If registered and expiration date is found:  
  ```
  example.com: REGISTERED (Expires on 2025-01-30)
  ```

- If registered but expiration date is not found:  
  ```
  example.com: REGISTERED (Expiration date not found)
  ```

## Error Handling

- If a domain query fails due to a WHOIS parsing error, the script will mark the domain as available.  
- If any other exception occurs (e.g., network issue), the script will handle it gracefully and report the domain as registered without an expiration date.
