# sniffer.py
# Live packet sniffer with protocol labelling, BPF filtering, PCAP saving, and IP alerts

import argparse
from collections import defaultdict
import datetime
from scapy.all import ICMP, IP, TCP, UDP, sniff, wrpcap

PORT_LABELS = {
    21: "FTP",
    22: "SSH",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    443: "HTTPS",
    3306: "MySQL",
    8080: "HTTP-Alt",
}

COUNTS = {"TCP": 0, "UDP": 0, "ICMP": 0, "Other": 0}
# Exercise 30: Tracking packets per source IP
IP_COUNTS = defaultdict(int)

# Exercise 32: List to store packet objects for PCAP export
CAPTURED_PACKETS = []

LOGFILE = "capture.txt"
PCAPFILE = "capture.pcap"
PACKET_MAX = 50


def label_port(port):
    return PORT_LABELS.get(port, "Unknown")


def handle_packet(packet):
    # Exercise 32: Store full packet object for PCAP export
    CAPTURED_PACKETS.append(packet)

    if IP not in packet:
        return

    src = packet[IP].src
    dst = packet[IP].dst
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Exercise 30: Increment count for source IP
    IP_COUNTS[src] += 1

    if TCP in packet:
        proto = "TCP"
        sport = packet[TCP].sport
        dport = packet[TCP].dport
    elif UDP in packet:
        proto = "UDP"
        sport = packet[UDP].sport
        dport = packet[UDP].dport
    elif ICMP in packet:
        proto = "ICMP"
        sport = "-"
        dport = "-"
    else:
        proto = "Other"
        sport = "-"
        dport = "-"

    COUNTS[proto] += 1
    service = label_port(dport) if isinstance(dport, int) else "-"
    line = f"{timestamp} {proto} {src}:{sport} -> {dst}:{dport} ({service})"
    print(line)

    with open(LOGFILE, "a") as f:
        f.write(line + "\n")


def main():
    # Exercise 29: Add --filter argument
    parser = argparse.ArgumentParser(description="Live Python Packet Sniffer")
    parser.add_argument(
        "--filter",
        type=str,
        default="",
        help="BPF filter string (e.g. 'tcp port 80')",
    )
    args = parser.parse_args()

    print(f"Capturing {PACKET_MAX} packets. Press Ctrl+C to stop.")
    if args.filter:
        print(f"Applying BPF filter: '{args.filter}'")

    # Pass filter argument into Scapy's sniff()
    sniff(
        prn=handle_packet,
        count=PACKET_MAX,
        store=False,
        filter=args.filter if args.filter else None,
    )

    print("\n--- Summary ---")
    print("Protocol Counts:")
    for proto, count in COUNTS.items():
        print(f"  {proto}: {count}")

    # Exercise 30 & 31: Print top 5 source IPs and flag > 15 packets
    print("\nTop 5 Source IPs:")
    sorted_ips = sorted(IP_COUNTS.items(), key=lambda x: x[1], reverse=True)[
        :5
    ]

    for ip, count in sorted_ips:
        # Exercise 31: Alert check
        alert = " [SUSPICIOUS TRAFFIC]" if count > 15 else ""
        print(f"  {ip}: {count} packets{alert}")

    # Exercise 32: Save to PCAP file
    if CAPTURED_PACKETS:
        wrpcap(PCAPFILE, CAPTURED_PACKETS)
        print(f"\nSaved raw capture to {PCAPFILE} (Openable in Wireshark)")


if __name__ == "__main__":
    main()