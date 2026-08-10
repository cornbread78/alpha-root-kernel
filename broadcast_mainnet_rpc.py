import urllib.request
import json
import os
import sys

def broadcast_kernel():
    print("==================================================")
    print("   ALPHA ROOT KERNEL - MAINNET RPC DISPATCH       ")
    print("   Path Vector: 04/04/00/00                      ")
    print("==================================================")

    payload_file = "kernel_tx.dat"
    if not os.path.exists(payload_file):
        print(f"[!] Error: {payload_file} missing from workspace.")
        sys.exit(1)

    with open(payload_file, "rb") as f:
        raw_payload = f.read()

    tx_hex = raw_payload.hex()
    print(f"[+] Loaded payload size: {len(raw_payload)} bytes")
    print(f"[+] Serialized Hex Preview: {tx_hex[:32]}...")

    # Bitcoin Core JSON-RPC endpoint configuration
    rpc_host = "127.0.0.1"
    rpc_port = 8332
    rpc_url = f"http://{rpc_host}:{rpc_port}"

    rpc_payload = {
        "jsonrpc": "1.0",
        "id": "alpha_mainnet_broadcast",
        "method": "sendrawtransaction",
        "params": [tx_hex]
    }

    data = json.dumps(rpc_payload).encode('utf-8')
    req = urllib.request.Request(
        rpc_url, 
        data=data, 
        headers={'Content-Type': 'application/json'}
    )

    print(f"[*] Dispatching transaction hex to node RPC at {rpc_url}...")

    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            result = json.loads(response.read().decode('utf-8'))
            print("[+] Node RPC Response Received:")
            print(json.dumps(result, indent=2))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8', errors='ignore')
        print(f"[!] RPC HTTP Error {e.code}: {e.reason}")
        print(f"[!] Node Error Details: {error_body}")
    except Exception as e:
        print(f"[!] Connection Error: {e}")
        print("[*] Ensure your target node daemon has JSON-RPC enabled (server=1).")

if __name__ == "__main__":
    broadcast_kernel()
