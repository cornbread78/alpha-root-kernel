import socket
import os
import sys

def execute_home_dispatch():
    print("==================================================")
    print("   ALPHA ROOT KERNEL - HOME DIRECTORY DISPATCH     ")
    print("   Path Vector: 04/04/00/00                       ")
    print("==================================================")
    
    target_host = "179.118.220.79"
    target_port = 8333
    payload_file = "kernel_tx.dat"
    
    if not os.path.exists(payload_file):
        with open(payload_file, "wb") as f:
            f.write(b"ALPHA_ROOT_KERNEL_PAYLOAD_04040000")
        print(f"[+] Initialized default payload buffer: {payload_file}")

    with open(payload_file, "rb") as f:
        data = f.read()

    print(f"[+] Loaded payload: {len(data)} bytes")
    print(f"[*] Connecting to target node {target_host}:{target_port}...")

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(10.0)
        s.connect((target_host, target_port))
        s.sendall(data)
        print("[+] Transmission broadcasted successfully to external node.")
        response = s.recv(1024)
        if response:
            print(f"[+] Acknowledgment Hex: {response.hex()}")
        s.close()
        print("[+] PATH VECTOR 04/04/00/00 TRANSACTION COMMITTED.")
    except Exception as e:
        print(f"[!] Network Error: {e}")

if __name__ == "__main__":
    execute_home_dispatch()
