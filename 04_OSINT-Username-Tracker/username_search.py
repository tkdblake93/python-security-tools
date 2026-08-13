import datetime
import requests
import time  # Added for Exercise 12

# --- Configuration Variables ---
username = input("Enter a username to search: ").strip()
found_only = True  # Added for Exercise 10 (True = hide NOT FOUND lines, False = show all)

sites = [
    "https://github.com/",
    "https://reddit.com/u/",
    "https://x.com/",
    "https://instagram.com/",
    "https://linkedin.com/in/",
    "https://medium.com/@",
    "https://dev.to/",
    "https://api.bitbucket.org/2.0/repositories/",
    "https://facebook.com/",
    "https://interpals.net/",
    "https://youtube.com/@",
]

report_name = f"osint_report_{username}.txt"

# Start the timer right before the loop (Exercise 12)
start_time = time.time()

with open(report_name, "w", encoding="utf-8") as report:
    report.write(f"OSINT Username Report: {username}\n")
    report.write(f"Generated: {datetime.datetime.now()}\n")
    report.write("=" * 50 + "\n")

    for site in sites:
        url = site + username
        
        # We print this so we know the script is actively working in the background
        if not found_only:
            print(f"Checking {url}...")

        # Initialize status variables
        is_found = False
        result = ""

        try:
            # Note: Adding a basic User-Agent headers dictionary is highly recommended 
            # here so major sites like Instagram or LinkedIn don't block the request.
            headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64)"}
            response = requests.get(url, headers=headers, timeout=5)
            
            if response.status_code == 200:
                result = f"FOUND: {url}"
                is_found = True
            elif response.status_code == 404:
                result = f"Not found: {url}"
            else:
                result = f"Unknown ({response.status_code}): {url}"
        except requests.RequestException as error:
            result = f"Error checking {url}: {error}"

        # Exercise 10 Logic: 
        # Print and save the result if it was found, OR if found_only mode is disabled.
        if is_found or not found_only:
            print(result)
            report.write(result + "\n")

    # Stop the timer after the loop finishes (Exercise 12)
    end_time = time.time()
    total_time = round(end_time - start_time, 2)

    # Append the timing metrics to the bottom of the report file
    report.write("=" * 50 + "\n")
    report.write(f"Scan Completed in: {total_time} seconds\n")

print("-" * 50)
print(f"Scan Completed in: {total_time} seconds")
print(f"Report saved as {report_name}")