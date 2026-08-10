import socket
import json
import os
import sys

HOST = "127.0.0.1"
PORT = 8332  # Standard local node RPC / daemon port or 8350 for custom sync
PATH_ID = "04/04/00/00"

def bridge_payload():
    if not os.path.exists("kernel_tx.dat"):
        print("[!] Error: kernel_tx.dat missing from workspace.")
        sys.exit(1)

    with open("kernel_tx.dat", "rb") as f:
        raw_payload = f.read()

    print(f"[*] Loaded workspace payload: {len(raw_payload)} bytes")
    print(f"[*] Target Path Vector: {PATH_ID}")
    print(f"[*] Establishing bridge to local node daemon at {HOST}:{PORT}...")

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(10.0)

    try:
        s.connect((HOST, PORT))
        # Construct and send node RPC / sync command packet
        rpc_request = {
            "jsonrpc": "1.0",
            "id": "alpha_sync",
            "method": "sendrawtransaction",
            "params": [raw_payload.hex()]
        }
        s.sendall(json.dumps(rpc_request).encode("utf-8") + b"\n")
        
        response = s.recv(4096)
        if response:
            print("[+] Node Daemon Response:")
            print(response.decode("utf-8", errors="ignore"))
        else:
            print("[+] Payload transmitted to node daemon interface.")
    except Exception as e:
        print(f"[!] Node bridge error: {e}")
    finally:
        s.close()

if __name__ == "__main__":
    bridge_payload()
