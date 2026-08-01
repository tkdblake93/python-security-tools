# scanner.py
# Port scanner with service labels, timing, and file output

import socket
import time

#target = "127.0.0.1" # change this to your target
target = "scanme.nmap.org"
start_port = 1
end_port = 1024
output_file = "scan_results.txt"

port_labels = {
    21: "FTP",
    22: "SSH",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    1433: "MSSQL",
    3306: "MySQL",
    5432: "PostgreSQL",
    6379: "Redis",
    8080: "HTTP-Alt",
    27017: "MongoDB"
}

print(f"Scanning {target} ...")
start_time = time.time()
open_ports = 0
found_ports = []

for port in range(start_port, end_port + 1):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)
        result = s.connect_ex((target, port))

        if result == 0:
            label = port_labels.get(port, "Unknown")
            print(f"Port {port} --- OPEN ({label})")
            open_ports += 1
            found_ports.append((port, label))

        s.close()

    except KeyboardInterrupt:
        print("\nScan stopped.")
        break
    except Exception:
        pass

duration = round(time.time() - start_time, 2)
print(f"\nDone. {open_ports} open port(s). Time: {duration}s")

with open(output_file, "w") as f:
    f.write(f"Scan {target}\n")
    f.write("=" * 40 + "\n")
    for port, label in found_ports:
        f.write(f"Port {port} OPEN ({label})\n")
    f.write(f"\nTotal: {open_ports} open | Time: {duration}s\n")

print(f"Results saved: {output_file}")

