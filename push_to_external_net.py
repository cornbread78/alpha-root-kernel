import socket
import os
import sys

# Designated external target node endpoint (Non-loopback)
EXTERNAL_HOST = "179.118.220.79"
EXTERNAL_PORT = 8333
PATH_ID = "04/04/00/00"
PAYLOAD_FILE = "kernel_tx.dat"

def push_external():
    print(f"[*] Initializing external network push for path {PATH_ID}...")
    
    if not os.path.exists(PAYLOAD_FILE):
        print(f"[!] Error: {PAYLOAD_FILE} missing from workspace.")
        sys.exit(1)

    with open(PAYLOAD_FILE, "rb") as f:
        payload = f.read()

    print(f"[+] Loaded payload: {len(payload)} bytes")
    print(f"[+] Routing completely away from localhost (127.0.0.1)")
    print(f"[+] Connecting to external target node at {EXTERNAL_HOST}:{EXTERNAL_PORT}...")

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.settimeout(15.0)

    try:
        client.connect((EXTERNAL_HOST, EXTERNAL_PORT))
        client.sendall(payload)
        response = client.recv(4096)
        
        print("[+] External network transmission committed successfully.")
        print("[+] Remote Node Response Hex:", response.hex())
        print(f"[+] PATH VECTOR {PATH_ID} OFF-LOOPBACK BROADCAST COMPLETE.")
    except Exception as e:
        print(f"[!] External network routing error: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    push_external()
