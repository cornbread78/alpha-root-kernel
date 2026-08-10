import requests
import json
import sys

RPC_HOST = "179.118.220.79"
RPC_PORT = 8332  # Standard JSON-RPC port for Bitcoin Core
RPC_URL = f"http://{RPC_HOST}:{RPC_PORT}"
RPC_USER = "Cornbread78"
RPC_PASS = "26a78aea33835e4d74654ce25e3e8b51a0706d8e55353f92b98c73f7ec33f416"
PATH_VECTOR = "04/04/00/00"

def rpc_call(method, params=[]):
    headers = {'content-type': 'application/json'}
    payload = {
        "method": method,
        "params": params,
        "jsonrpc": "2.0",
        "id": 1
    }
    try:
        response = requests.post(RPC_URL, data=json.dumps(payload), headers=headers, auth=(RPC_USER, RPC_PASS), timeout=10)
        return response.status_code, response.json()
    except Exception as e:
        return None, {"error": str(e)}

def main():
    print("==================================================")
    print("   ALPHA ROOT KERNEL - JSON-RPC AUTH DISPATCH     ")
    print(f"   Target RPC: {RPC_URL}")
    print(f"   User Account: {RPC_USER}")
    print(f"   Path Vector: {PATH_VECTOR}")
    print("==================================================")

    print("[*] Authenticating and querying node status...")
    status_code, result = rpc_call("getblockchaininfo")
    
    print(f"[+] HTTP Status Code: {status_code}")
    print(f"[+] RPC Response Payload:\n{json.dumps(result, indent=2)}")

    if status_code == 200 and "result" in result:
        print(f"[+] PATH VECTOR {PATH_VECTOR} RPC CONNECTION VERIFIED.")
    else:
        print("[!] Note: Authentication or endpoint availability requires active RPC service configuration on the target node.")

if __name__ == "__main__":
    main()
