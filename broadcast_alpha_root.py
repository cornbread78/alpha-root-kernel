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

    hex_payload = raw_payload.hex()
    print(f"[*] Opened Alpha Root Kernel payload: {len(raw_payload)} bytes")
    print(f"[*] Target Path Vector: {PATH_ID}")

    # Explicit user credentials
    username = "Cornbread78"
    password = "26a78aea33835e4d74654ce25e3e8b51a0706d8e55353f92b98c73f7ec33f416"
    credentials = f"{username}:{password}"
    
    auth_encoded = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")

    rpc_url = f"http://{HOST}:{PORT}/"
    rpc_data = {
        "jsonrpc": "1.0",
        "id": "alpha_root_broadcast",
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

    print(f"[*] Broadcasting Alpha Root Kernel to node daemon at {rpc_url}...")
    try:
        with urllib.request.urlopen(req, timeout=10.0) as response:
            res_body = response.read().decode("utf-8")
            print("[+] Node Daemon Response:")
            print(res_body)
            print(f"[+] ALPHA ROOT KERNEL PATH VECTOR {PATH_ID} BROADCASTED SUCCESSFULLY.")
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
