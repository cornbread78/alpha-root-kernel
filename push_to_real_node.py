import urllib.request
import urllib.error
import json
import base64
import os
import sys

HOST = "127.0.0.1"
PORT = 8332
PATH_ID = "04/04/00/00"

def get_auth_credentials():
    # Search standard Bitcoin Core data directories for the cookie file
    possible_paths = [
        os.path.expanduser("~/.bitcoin/.cookie"),
        os.path.expanduser("~/.bitcoin/regtest/.cookie"),
        os.path.expanduser("~/.bitcoin/testnet3/.cookie"),
        os.path.expanduser("~/.bitcoin/signet/.cookie"),
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            try:
                with open(path, "r") as f:
                    cookie = f.read().strip()
                    if cookie:
                        print(f"[+] Located node cookie at: {path}")
                        return cookie
            except Exception:
                continue

    # Fallback to checking bitcoin.conf if cookie is absent
    conf_path = os.path.expanduser("~/.bitcoin/bitcoin.conf")
    if os.path.exists(conf_path):
        try:
            with open(conf_path, "r") as f:
                user, pwd = "", ""
                for line in f:
                    if line.strip().startswith("rpcuser="):
                        user = line.strip().split("=")[1]
                    elif line.strip().startswith("rpcpassword="):
                        pwd = line.strip().split("=")[1]
                if user and pwd:
                    print(f"[+] Extracted credentials from bitcoin.conf")
                    return f"{user}:{pwd}"
        except Exception:
            pass

    return None

def main():
    if not os.path.exists("kernel_tx.dat"):
        print("[!] Error: kernel_tx.dat not found in workspace.")
        sys.exit(1)

    with open("kernel_tx.dat", "rb") as f:
        raw_payload = f.read()

    hex_payload = raw_payload.hex()
    print(f"[*] Loaded workspace payload: {len(raw_payload)} bytes")
    print(f"[*] Target Path Vector: {PATH_ID}")

    credentials = get_auth_credentials()
    if not credentials:
        print("[!] Error: Could not find active node cookie or configuration credentials.")
        print("[!] Ensure your local Bitcoin node daemon is running and accessible.")
        sys.exit(1)

    auth_encoded = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")

    rpc_url = f"http://{HOST}:{PORT}/"
    rpc_data = {
        "jsonrpc": "1.0",
        "id": "node_sync_bridge",
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
            print(f"[+] PATH VECTOR {PATH_ID} COMMITTED TO NODE DAEMON.")
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
