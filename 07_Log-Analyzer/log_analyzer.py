import argparse
from collections import Counter
import re
import sys

# Define standard status codes to monitor
SUSPICIOUS_STATUS_CODES = {"400", "401", "403", "404", "500"}


def analyze_log(log_filename, threshold):
    ip_threat_counts = Counter()
    path_counts = Counter()

    # Regex pattern to extract IP, HTTP status, and path from common log formats
    log_pattern = re.compile(
        r'(?P<ip>\d{1,3}(?:\.\d{1,3}){3})\s+-\s+-\s+\[.*?\]\s+"[A-Z]+\s+(?P<path>\S+)\s+HTTP/.*?"\s+(?P<status>\d{3})'
    )

    try:
        with open(log_filename, "r") as file:
            for line in file:
                match = log_pattern.search(line)
                if match:
                    ip = match.group("ip")
                    path = match.group("path")
                    status = match.group("status")

                    # Track all requested paths
                    path_counts[path] += 1

                    # Track suspicious HTTP status responses per IP
                    if status in SUSPICIOUS_STATUS_CODES:
                        ip_threat_counts[ip] += 1

    except FileNotFoundError:
        print(f"Error: The file '{log_filename}' was not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading log file: {e}")
        sys.exit(1)

    # Display Top 10 Most Requested Paths (Exercise 23)
    print("\n=== TOP 10 MOST REQUESTED PATHS ===")
    if path_counts:
        for path, count in path_counts.most_common(10):
            print(f"{count:<8} {path}")
    else:
        print("No path request data found.")

    # Display Flagged IPs Exceeding Threshold (Exercise 21/22)
    print(f"\n=== FLAGGED IPS (THRESHOLD > {threshold}) ===")
    flagged_ips = {
        ip: count
        for ip, count in ip_threat_counts.items()
        if count >= threshold
    }

    if flagged_ips:
        for ip, count in sorted(
            flagged_ips.items(), key=lambda x: x[1], reverse=True
        ):
            print(f"IP: {ip:<15} | Suspicious Requests: {count}")
    else:
        print("No IPs exceeded the specified threshold.")

    # Write output to dynamic threat report
    report_filename = f"threat_report_{threshold}.txt"
    try:
        with open(report_filename, "w") as report:
            report.write(f"Threat Report (Threshold: {threshold})\n")
            report.write("=" * 40 + "\n\n")
            report.write("Top 10 Requested Paths:\n")
            for path, count in path_counts.most_common(10):
                report.write(f"{count:<8} {path}\n")

            report.write("\nFlagged IPs:\n")
            for ip, count in flagged_ips.items():
                report.write(f"{ip:<15} - {count} events\n")

        print(f"\nReport successfully saved to '{report_filename}'")
    except IOError as e:
        print(f"Failed to write report file: {e}")


def main():
    # Setup argparse for command-line execution (Exercise 24)
    parser = argparse.ArgumentParser(
        description="Analyze web server access logs for threat detection."
    )
    parser.add_argument(
        "log_file",
        help="Path to the HTTP log file to analyze",
    )
    parser.add_argument(
        "-t",
        "--threshold",
        type=int,
        default=10,
        help="Minimum suspicious requests threshold to flag an IP (default: 10)",
    )

    args = parser.parse_args()

    analyze_log(args.log_file, args.threshold)


if __name__ == "__main__":
    main()