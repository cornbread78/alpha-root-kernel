import urllib.request
import urllib.error
import json
import base64
import os
import sys

HOST = "127.0.0.1"
PORT = 8332
PATH_ID = "04/04/00/00"

def get_cookie_auth():
    cookie_paths = [
        os.path.expanduser("~/.bitcoin/.cookie"),
        os.path.expanduser("~/.bitcoin/regtest/.cookie"),
        os.path.expanduser("~/.bitcoin/testnet3/.cookie"),
        os.path.expanduser("~/.rugpull/.cookie"),
    ]
    for path in cookie_paths:
        if os.path.exists(path):
            with open(path, "r") as f:
                return f.read().strip()
    return None

def main():
    if not os.path.exists("kernel_tx.dat"):
        print("[!] Error: kernel_tx.dat not found in workspace.")
        sys.exit(1)

    with open("kernel_tx.dat", "rb") as f:
        raw_payload = f.read()

    hex_payload = raw_payload.hex()
    print(f"[*] Loaded payload: {len(raw_payload)} bytes")
    print(f"[*] Target Path Vector: {PATH_ID}")

    credentials = get_cookie_auth()
    if credentials:
        print("[+] Detected local node authentication cookie.")
    else:
        print("[*] Using standard local credentials.")
        credentials = "rpcuser:rpcpassword"

    auth_encoded = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")

    rpc_url = f"http://{HOST}:{PORT}/"
    rpc_data = {
        "jsonrpc": "1.0",
        "id": "alpha_root_sync",
        "method": "sendrawtransaction",
        "params": [hex_payload]
    }

    req_body = json.dumps(rpc_data).encode("utf-8")
    
    req = urllib.request.Request(
        rpc_url,
        data=req_body,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Basic {auth_encoded}"
        },
        method="POST"
    )

    print(f"[*] Dispatching transaction payload to node daemon at {rpc_url}...")
    try:
        with urllib.request.urlopen(req, timeout=10.0) as response:
            res_body = response.read().decode("utf-8")
            print("[+] Node Daemon RPC Response:")
            print(res_body)
            print(f"[+] PATH VECTOR {PATH_ID} TRANSMITTED TO NODE DAEMON SUCCESSFULLY.")
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
