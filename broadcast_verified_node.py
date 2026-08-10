import urllib.request
import json
import base64
import os
import sys

HOST = "127.0.0.1"
PORT = 8332
PATH_ID = "04/04/00/00"
PAYLOAD_FILE = "kernel_tx.dat"

def get_auth():
    # Exact verified credentials for your node daemon
    username = "Cornbread78"
    password = "26a78aea33835e4d74654ce25e3e8b51a0706d8e55353f92b98c73f7ec33f416"
    return f"{username}:{password}"

def main():
    print("==================================================")
    print("   ALPHA ROOT KERNEL - VERIFIED NODE DISPATCH     ")
    print(f"   Path Vector: {PATH_ID}                        ")
    print("==================================================")

    if not os.path.exists(PAYLOAD_FILE):
        print(f"[!] Error: {PAYLOAD_FILE} missing from workspace.")
        sys.exit(1)

    with open(PAYLOAD_FILE, "rb") as f:
        payload_data = f.read()

    tx_hex = payload_data.hex()
    print(f"[+] Loaded payload size: {len(payload_data)} bytes")
    print(f"[+] Authenticating with verified profile: Cornbread78")

    credentials = get_auth()
    auth_encoded = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")
    rpc_url = f"http://{HOST}:{PORT}/"

    # Step 1: Verify authentication with blockchain info
    info_payload = {
        "jsonrpc": "1.0",
        "id": "alpha_info",
        "method": "getblockchaininfo",
        "params": []
    }

    req = urllib.request.Request(
        rpc_url,
        data=json.dumps(info_payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Basic {auth_encoded}"
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=10.0) as response:
            res = json.loads(response.read().decode("utf-8"))
            print(f"[+] Node Authentication Successful!")
            print(f"[+] Active Chain Height: {res['result']['blocks']}")
    except Exception as e:
        print(f"[!] Authentication Failed: {e}")
        return

    # Step 2: Submit raw transaction payload to node daemon
    broadcast_payload = {
        "jsonrpc": "1.0",
        "id": "alpha_broadcast",
        "method": "sendrawtransaction",
        "params": [tx_hex]
    }

    req_bc = urllib.request.Request(
        rpc_url,
        data=json.dumps(broadcast_payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Basic {auth_encoded}"
        },
        method="POST"
    )

    print(f"[*] Dispatching raw kernel transmission to node RPC...")
    try:
        with urllib.request.urlopen(req_bc, timeout=10.0) as response:
            res = json.loads(response.read().decode("utf-8"))
            print("[+] Node Response Received:")
            print(json.dumps(res, indent=2))
            print(f"[+] PATH VECTOR {PATH_ID} COMMITTED TO NODE.")
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8", errors="ignore")
        print(f"[!] Node HTTP Error {e.code}: {e.reason}")
        if err_body:
            print(f"[!] Response Details: {err_body}")
    except Exception as e:
        print(f"[!] Dispatch Error: {e}")

if __name__ == "__main__":
    main()
