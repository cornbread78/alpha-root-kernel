import os
import sys
import json
import base64
import urllib.request

HOST = "127.0.0.1"
PORT = 8332
PATH_ID = "04/04/00/00"
PAYLOAD_FILE = "kernel_tx.dat"

def get_credentials():
    bitcoin_dir = os.path.expanduser("~/.bitcoin")
    cookie_path = os.path.join(bitcoin_dir, ".cookie")
    
    # Check for active cookie file first (default Bitcoin Core auth)
    if os.path.exists(cookie_path):
        print(f"[+] Utilizing active session cookie from {cookie_path}")
        with open(cookie_path, "r") as f:
            cookie_content = f.read().strip()
        if ":" in cookie_content:
            return cookie_content
        else:
            return f"__cookie__:{cookie_content}"
            
    # Fallback to bitcoin.conf parsing
    conf_path = os.path.join(bitcoin_dir, "bitcoin.conf")
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
    return f"{user}:{pwd}"

def main():
    if not os.path.exists(PAYLOAD_FILE):
        print(f"[!] Error: {PAYLOAD_FILE} missing from workspace.")
        sys.exit(1)

    with open(PAYLOAD_FILE, "rb") as f:
        payload_data = f.read()

    tx_hex = payload_data.hex()
    print(f"[*] Loaded workspace payload: {len(payload_data)} bytes")
    print(f"[*] Target Path Vector: {PATH_ID}")

    credentials = get_credentials()
    auth_encoded = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")

    rpc_url = f"http://{HOST}:{PORT}/"
    rpc_payload = {
        "jsonrpc": "1.0",
        "id": "alpha_root_robust_broadcast",
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
