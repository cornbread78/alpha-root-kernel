import urllib.request
import urllib.error
import json
import base64
import os
import sys

HOST = "127.0.0.1"
PORT = 8332
PATH_ID = "04/04/00/00"

def get_auth():
    # 1. Check for cookie files in standard Bitcoin data dirs
    cookie_locations = [
        os.path.expanduser("~/.bitcoin/.cookie"),
        os.path.expanduser("~/.bitcoin/regtest/.cookie"),
        os.path.expanduser("~/.bitcoin/testnet3/.cookie"),
        os.path.expanduser("~/.bitcoin/signet/.cookie"),
    ]
    for path in cookie_locations:
        if os.path.exists(path):
            try:
                with open(path, "r") as f:
                    content = f.read().strip()
                    if content:
                        print(f"[+] Loaded authentication cookie from {path}")
                        return content # format is usually username:password or just password depending on setup
            except Exception:
                continue

    # 2. Check bitcoin.conf with robust parsing
    conf_path = os.path.expanduser("~/.bitcoin/bitcoin.conf")
    if os.path.exists(conf_path):
        try:
            user, pwd = "", ""
            with open(conf_path, "r") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    if "=" in line:
                        key, val = line.split("=", 1)
                        key = key.strip().lower()
                        val = val.strip().strip('"\'')
                        if key == "rpcuser":
                            user = val
                        elif key == "rpcpassword":
                            pwd = val
            if user and pwd:
                print("[+] Extracted rpcuser/rpcpassword from bitcoin.conf")
                return f"{user}:{pwd}"
        except Exception as e:
            print(f"[!] Error reading bitcoin.conf: {e}")

    # 3. Fallback default credentials
    return "rpcuser:rpcpassword"

def main():
    if not os.path.exists("kernel_tx.dat"):
        print("[!] Error: kernel_tx.dat missing from workspace.")
        sys.exit(1)

    with open("kernel_tx.dat", "rb") as f:
        raw_payload = f.read()

    hex_payload = raw_payload.hex()
    print(f"[*] Loaded workspace payload: {len(raw_payload)} bytes")
    print(f"[*] Target Path Vector: {PATH_ID}")

    auth_str = get_auth()
    auth_encoded = base64.b64encode(auth_str.encode("utf-8")).decode("utf-8")

    rpc_url = f"http://{HOST}:{PORT}/"
    rpc_data = {
        "jsonrpc": "1.0",
        "id": "workspace_consensus_sync",
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
            print("[+] Node Daemon Response:")
            print(res_body)
            print(f"[+] PATH VECTOR {PATH_ID} COMMITTED TO NODE DAEMON SUCCESSFULLY.")
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
