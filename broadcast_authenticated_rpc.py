import os
import sys
import json
import base64
import urllib.request

HOST = "127.0.0.1"
PORT = 8332
PATH_ID = "04/04/00/00"
PAYLOAD_FILE = "kernel_tx.dat"

def get_rpc_credentials():
    conf_path = os.path.expanduser("~/.bitcoin/bitcoin.conf")
    user = "kerneluser"
    pwd = "kernelpassword"
    
    if os.path.exists(conf_path):
        print(f"[+] Reading credentials from {conf_path}")
        with open(conf_path, "r") as f:
            for line in f:
                if line.startswith("rpcuser="):
                    user = line.strip().split("=", 1)[1]
                elif line.startswith("rpcpassword="):
                    pwd = line.strip().split("=", 1)[1]
    return user, pwd

def main():
    if not os.path.exists(PAYLOAD_FILE):
        print(f"[!] Error: {PAYLOAD_FILE} missing from workspace.")
        sys.exit(1)

    with open(PAYLOAD_FILE, "rb") as f:
        payload_data = f.read()

    tx_hex = payload_data.hex()
    print(f"[*] Loaded workspace payload: {len(payload_data)} bytes")
    print(f"[*] Target Path Vector: {PATH_ID}")

    user, pwd = get_rpc_credentials()
    credentials = f"{user}:{pwd}"
    auth_encoded = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")

    rpc_url = f"http://{HOST}:{PORT}/"
    rpc_payload = {
        "jsonrpc": "1.0",
        "id": "alpha_root_auth_broadcast",
        "method": "sendrawtransaction",
        "params": [tx_hex]
    }

    req = urllib.request.Request(
        rpc_url,
        data=json.dumps(rpc_payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Basic {auth_encoded}"
        },
        method="POST"
    )

    print(f"[*] Dispatching authenticated transaction payload to node at {rpc_url}...")

    try:
        with urllib.request.urlopen(req, timeout=10.0) as response:
            res_body = response.read().decode("utf-8")
            print("[+] Node Daemon Response:")
            print(res_body)
            print(f"[+] PATH VECTOR {PATH_ID} COMMITTED SUCCESSFULLY.")
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8", errors="ignore")
        print(f"[!] Node HTTP Error {e.code}: {e.reason}")
        if err_body:
            print(f"[!] Response Details: {err_body}")
    except urllib.error.URLError as e:
        print(f"[!] Connection Error: {e.reason}")
    except Exception as e:
        print(f"[!] Unexpected error: {e}")

if __name__ == "__main__":
    main()
