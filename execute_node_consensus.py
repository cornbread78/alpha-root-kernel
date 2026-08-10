import socket
import json
import os
import sys
import hashlib

HOST = "127.0.0.1"
PORT = 8350
PATH_ID = "04/04/00/00"

def execute_sync():
    print(f"[*] Initializing network sync for path {PATH_ID}...")
    
    # Load required components
    required_files = ["kernel_tx.dat", "alpha_root.ledger", "alpha_root_export.json"]
    for f in required_files:
        if not os.path.exists(f):
            print(f"[!] Error: Missing required component -> {f}")
            sys.exit(1)

    with open("kernel_tx.dat", "rb") as f:
        payload = f.read()

    with open("alpha_root.ledger", "r") as f:
        ledger_data = f.read()

    with open("alpha_root_export.json", "r") as f:
        export_data = json.load(f)

    print(f"[+] Loaded payload: {len(payload)} bytes")
    print(f"[+] Loaded ledger hash: {export_data.get('hash_proof', 'N/A')}")

    # Establish socket connection to the active node daemon
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.settimeout(10.0)

    try:
        client.connect((HOST, PORT))
        print(f"[+] Connected to active node interface at {HOST}:{PORT}")

        # Construct consensus packet
        packet = {
            "path": PATH_ID,
            "ledger": ledger_data,
            "export": export_data,
            "payload_hex": payload.hex()
        }

        client.sendall(json.dumps(packet).encode("utf-8"))
        print("[+] Synchronized packet transmitted to network daemon.")

        response = client.recv(4096)
        if response:
            print(f"[+] Node Consensus Response: {response.decode('utf-8', errors='ignore').strip()}")
        else:
            print("[+] Node stream successfully acknowledged.")

    except Exception as e:
        print(f"[!] Network sync transmission error: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    execute_sync()
