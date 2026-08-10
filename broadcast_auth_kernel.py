import urllib.request
import urllib.error
import json
import base64
import os
import sys

HOST = "127.0.0.1"
PORT = 8332
PATH_ID = "04/04/00/00"

def main():
    if not os.path.exists("kernel_tx.dat"):
        print("[!] Error: kernel_tx.dat missing from workspace.")
        sys.exit(1)

    with open("kernel_tx.dat", "rb") as f:
        raw_payload = f.read()

    print(f"[*] Loaded workspace payload: {len(raw_payload)} bytes")
    print(f"[*] Target Path Vector: {PATH_ID}")

    # Use your explicit credentials
    username = "Cornbread78"
    password = "26a78aea33835e4d74654ce25e3e8b51a0706d8e55353f92b98c73f7ec33f416"
    credentials = f"{username}:{password}"
    auth_encoded = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")

    rpc_url = f"http://{HOST}:{PORT}/"
    
    # Check node status first using authenticated JSON-RPC
    info_data = {
        "jsonrpc": "1.0",
        "id": "alpha_node_check",
        "method": "getblockchaininfo",
        "params": []
    }

    req = urllib.request.Request(
        rpc_url,
        data=json.dumps(info_data).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Basic {auth_encoded}"
        },
        method="POST"
    )

    print(f"[*] Connecting to authenticated node daemon at {rpc_url}...")
    try:
        with urllib.request.urlopen(req, timeout=10.0) as response:
            res_body = json.loads(response.read().decode("utf-8"))
            print("[+] Node Authentication Successful!")
            print(f"[+] Current Chain Height: {res_body.get('result', {}).get('blocks', 'Unknown')}")
    except urllib.error.HTTPError as e:
        print(f"[!] Node HTTP Error {e.code}: {e.reason}")
        sys.exit(1)
    except Exception as e:
        print(f"[!] Connection Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
