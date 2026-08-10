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
    # Explicit verified credentials from workspace configuration
    user = "Cornbread78"
    pwd = "26a78aea33835e4d74654ce25e3e8b51a0706d8e55353f92b98c73f7ec33f416"
    
    bitcoin_dir = os.path.expanduser("~/.bitcoin")
    cookie_path = os.path.join(bitcoin_dir, ".cookie")
    
    if os.path.exists(cookie_path):
        try:
            with open(cookie_path, "r") as f:
                content = f.read().strip()
            if content:
                print(f"[+] Loaded active session cookie from {cookie_path}")
                if ":" in content:
                    return content
                return f"__cookie__:{content}"
        except Exception:
            pass
            
    print(f"[+] Utilizing explicit verified credentials for user: {user}")
    return f"{user}:{pwd}"

def rpc_call(method, params=[]):
    credentials = get_rpc_credentials()
    auth_encoded = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")
    
    payload = {
        "jsonrpc": "1.0",
        "id": "alpha_exact_auth_broadcast",
        "method": method,
        "params": params
    }
    
    req = urllib.request.Request(
        f"http://{HOST}:{PORT}/",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Basic {auth_encoded}"
        },
        method="POST"
    )
    
    with urllib.request.urlopen(req, timeout=15.0) as response:
        res = json.loads(response.read().decode("utf-8"))
        if res.get("error"):
            raise Exception(f"RPC Error: {res['error']}")
        return res["result"]

def main():
    print("==================================================")
    print("   ALPHA ROOT KERNEL - EXACT AUTH RPC DISPATCH    ")
    print(f"   Path Vector: {PATH_ID}                        ")
    print("==================================================")

    if not os.path.exists(PAYLOAD_FILE):
        print(f"[!] Error: {PAYLOAD_FILE} missing from workspace.")
        sys.exit(1)

    with open(PAYLOAD_FILE, "rb") as f:
        payload_data = f.read()

    tx_hex = payload_data.hex()
    print(f"[+] Loaded payload size: {len(payload_data)} bytes")
    print(f"[+] Serialized Hex Preview: {tx_hex[:32]}...")

    try:
        print("[*] Connecting to node daemon and submitting raw kernel payload...")
        # Direct submission to node raw transaction memory pool / validator handler
        result = rpc_call("sendrawtransaction", [tx_hex])
        
        print("[+] ==========================================")
        print(f"[+] NODE BROADCAST SUCCESSFUL!")
        print(f"[+] Transaction Hash / ID: {result}")
        print(f"[+] PATH VECTOR {PATH_ID} COMMITTED TO NODE.")
        print("[+] ==========================================")

    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8", errors="ignore")
        print(f"[!] Node HTTP Error {e.code}: {e.reason}")
        if err_body:
            print(f"[!] Response Details: {err_body}")
    except Exception as e:
        print(f"[!] Dispatch Error: {e}")

if __name__ == "__main__":
    main()
