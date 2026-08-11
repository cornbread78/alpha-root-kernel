import http.client
import json
import base64
import os
import sys

# Standard Bitcoin Core Node JSON-RPC Configuration
RPC_HOST = "127.0.0.1"
RPC_PORT = 8332
RPC_USER = "rpcuser"
RPC_PASSWORD = "rpcpassword"
FRAME_FILE = "final_mainnet_frame.hex"
PATH_VECTOR = "04/04/00/00"

def submit_to_node():
    print("==================================================")
    print("   ALPHA ROOT KERNEL - NODE JSON-RPC SUBMISSION   ")
    print(f"   Target RPC: {RPC_HOST}:{RPC_PORT}")
    print(f"   Path Vector: {PATH_VECTOR}")
    print("==================================================")

    if not os.path.exists(FRAME_FILE):
        print(f"[!] Error: {FRAME_FILE} missing. Run the packager first.")
        sys.exit(1)

    with open(FRAME_FILE, "r") as f:
        tx_hex = f.read().strip()

    print(f"[+] Loaded transmission hex ({len(tx_hex)//2} bytes)")

    auth_str = f"{RPC_USER}:{RPC_PASSWORD}"
    encoded_auth = base64.b64encode(auth_str.encode()).decode()

    headers = {
        "Authorization": f"Basic {encoded_auth}",
        "Content-Type": "application/json"
    }

    payload = {
        "jsonrpc": "1.0",
        "id": "alpha_kernel_broadcast",
        "method": "sendrawtransaction",
        "params": [tx_hex]
    }

    try:
        conn = http.client.HTTPConnection(RPC_HOST, RPC_PORT, timeout=15)
        conn.request("POST", "/", json.dumps(payload), headers)
        response = conn.getresponse()
        data = response.read().decode()
        conn.close()

        result = json.loads(data)
        print("--------------------------------------------------")
        print("             NODE RPC RESPONSE                    ")
        print("--------------------------------------------------")
        
        if result.get("error") is not None:
            print(f"[!] Node Rejection: {result['error']}")
        else:
            txid = result.get("result")
            print(f"[+] SUCCESS: Transaction Accepted by Node!")
            print(f"[+] Transaction ID (TxID): {txid}")
            
    except Exception as e:
        print(f"[!] RPC Connection Exception: {e}")
    print("==================================================")

if __name__ == "__main__":
    submit_to_node()
