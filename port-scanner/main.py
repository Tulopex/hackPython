import socket
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

def scan_port(ip, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(1)
        result = sock.connect_ex((ip, port))
        return port if result == 0 else None

def scan_ports(ip, port_range, max_workers=100):
    open_ports = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(scan_port, ip, port): port for port in range(*port_range)}
        for future in tqdm(as_completed(futures), total=len(futures), desc="Сканирование портов", unit="port"):
            port = future.result()
            if port:
                open_ports.append(port)
    return open_ports

ip = '127.0.0.1'
port_range = (1, 1024)
open_ports = scan_ports(ip, port_range)

print(f"Открытые порты на {ip}: {open_ports}")
