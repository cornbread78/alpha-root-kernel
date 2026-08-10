import socket
import json
import os
import sys

# Change these variables to your target external node IP and port
EXTERNAL_HOST = "127.0.0.1"  # Replace with target node IP if broadcasting publicly
EXTERNAL_PORT = 8333        # Standard P2P port or target node port
PATH_ID = "04/04/00/00"

def broadcast_payload():
    release_path = "deployed_release/kernel_tx.dat"
    if not os.path.exists(release_path):
        print(f"[!] Error: Deployed component missing at {release_path}")
        sys.exit(1)

    with open(release_path, "rb") as f:
        payload = f.read()

    print(f"[*] Loaded deployment payload: {len(payload)} bytes")
    print(f"[*] Target Path Vector: {PATH_ID}")
    print(f"[*] Opening external socket connection to {EXTERNAL_HOST}:{EXTERNAL_PORT}...")

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(10.0)

    try:
        s.connect((EXTERNAL_HOST, EXTERNAL_PORT))
        s.sendall(payload)
        
        print("[+] Raw transaction stream successfully transmitted to external target.")
        
        # Attempt to receive response or acknowledgment stream
        try:
            response = s.recv(4096)
            if response:
                print(f"[+] External Node Response: {response.hex()}")
            else:
                print("[+] Connection acknowledged by remote endpoint.")
        except socket.timeout:
            print("[+] Transmission complete (remote node did not return an immediate response stream).")

    except Exception as e:
        print(f"[!] External transmission error: {e}")
    finally:
        s.close()

if __name__ == "__main__":
    broadcast_payload()
