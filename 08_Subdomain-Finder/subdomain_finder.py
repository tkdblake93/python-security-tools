# subdomain_finder.py
# Multithreaded subdomain finder using DNS resolution & HTTP checks

import argparse
import datetime
import socket
from concurrent.futures import ThreadPoolExecutor
import requests

# -------------------------------------------------------------------
# Argument Parsing (Exercises 25 & 28)
# -------------------------------------------------------------------
parser = argparse.ArgumentParser(description="Multithreaded Subdomain Finder")
parser.add_argument("-d", "--domain", required=False, help="Target domain (e.g. example.com)")
parser.add_argument("-w", "--wordlist", required=False, help="Path to wordlist file")
parser.add_argument("-t", "--threads", type=int, default=20, help="Number of concurrent threads (default: 20)")
parser.add_argument("-o", "--output", required=False, help="Custom output report filename")
args = parser.parse_args()

# Fallback to interactive prompts if arguments aren't supplied via CLI
domain = args.domain.strip() if args.domain else input("Enter target domain (e.g. example.com): ").strip()
wordfile = args.wordlist.strip() if args.wordlist else input("Path to wordlist file: ").strip()

try:
    with open(wordfile, "r") as f:
        wordlist = {line.strip() for line in f if line.strip()}
except FileNotFoundError:
    print(f"Error: Wordlist file '{wordfile}' not found.")
    raise SystemExit

found = []

# -------------------------------------------------------------------
# Helper Functions (Exercise 26)
# -------------------------------------------------------------------
def check_http(subdomain):
    """Checks HTTP and HTTPS endpoints for status codes."""
    for protocol in ["http", "https"]:
        try:
            url = f"{protocol}://{subdomain}"
            response = requests.get(url, timeout=3)
            return response.status_code
        except requests.RequestException:
            continue
    return "N/A"

def process_subdomain(name):
    """Performs DNS lookup and HTTP status check for a given wordlist entry."""
    subdomain = f"{name}.{domain}"
    try:
        ip = socket.gethostbyname(subdomain)
        status = check_http(subdomain)
        return subdomain, ip, status
    except socket.gaierror:
        return None

# -------------------------------------------------------------------
# Threaded Execution (Exercise 25)
# -------------------------------------------------------------------
print(f"Starting scan on {domain} using {args.threads} threads...\n")

with ThreadPoolExecutor(max_workers=args.threads) as executor:
    results = executor.map(process_subdomain, wordlist)

    for result in results:
        if result:
            subdomain, ip, status = result
            found.append((subdomain, ip, status))
            print(f"FOUND: {subdomain} -> {ip} [HTTP Status: {status}]")

# -------------------------------------------------------------------
# Sorting & Output Generation (Exercises 27 & 28)
# -------------------------------------------------------------------
# Exercise 27: Sort alphabetically by subdomain string (first item in tuple)
found.sort(key=lambda item: item[0])

# Exercise 28: Determine output filename
report_name = args.output if args.output else f"subdomains_{domain}.txt"

with open(report_name, "w") as report:
    report.write(f"Subdomain report for {domain}\n")
    report.write(f"Generated: {datetime.datetime.now()}\n")
    report.write("=" * 50 + "\n")
    for subdomain, ip, status in found:
        report.write(f"{subdomain} -> {ip} -> HTTP: {status}\n")

print(f"\nDone. Found {len(found)} subdomains. Report saved as '{report_name}'.")