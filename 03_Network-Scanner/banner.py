# banner.py
# Grabs service banners to identfy software and version information

import socket

def grab_banner(ip, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        s.connect((ip, port))
        banner = s.recv(1024).decode("utf-8", errors="ignore").strip()
        s.close()
        return banner
    except Exception:
        return None

#target = "127.0.0.1"
target = "scanme.nmap.org"
ports_to_check = [21, 22, 25, 80, 110, 143]

for port in ports_to_check:
    print(f"Checking port {port}...")
    banner = grab_banner(target, port)

    if banner:
        print(f"Banner: {banner[:100]}")
    else:
        print("No banner received")
#example
