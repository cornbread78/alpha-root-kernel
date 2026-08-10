import socket
import os
import sys

HOST = "127.0.0.1"
PORT = 8333
PATH_ID = "04/04/00/00"
PAYLOAD_FILE = "kernel_tx.dat"

def broadcast_payload():
    if not os.path.exists(PAYLOAD_FILE):
        print(f"[!] Error: {PAYLOAD_FILE} not found in workspace.")
        sys.exit(1)

    with open(PAYLOAD_FILE, "rb") as f:
        payload = f.read()

    print(f"[*] Loaded payload: {len(payload)} bytes")
    print(f"[*] Target Path Vector: {PATH_ID}")
    print(f"[*] Connecting to node daemon at {HOST}:{PORT}...")

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.settimeout(10.0)

    try:
        client.connect((HOST, PORT))
        client.sendall(payload)
        response = client.recv(4096)
        
        print("[+] Transmission successful.")
        print("[+] Node Response Hex:", response.hex())
        print("[+] Node Response Text:", response.decode("utf-8", errors="ignore").strip())
    except Exception as e:
        print(f"[!] Connection error: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    broadcast_payload()
