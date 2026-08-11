import os
import json
import urllib.request
import base64

def selective_xor_dispatch():
    print("==================================================")
    print(" SELECTIVE XOR KERNEL TRANSACTION BUILDER")
    print("==================================================")
    
    kernel_path = "kernel_tx.dat"
    xor_key = bytes.fromhex("d923edcf24bbc601")
    
    if os.path.exists(kernel_path):
        with open(kernel_path, "rb") as f:
            raw_data = f.read()
    else:
        print("[-] Error: kernel_tx.dat not found.")
        return

    # Preserve transaction header (Version: 4 bytes, Input Count: 1 byte)
    header = raw_data[:5]
    body = raw_data[5:]
    
    # Apply XOR key only to the transaction body
    decoded_body = bytes(b ^ xor_key[i % len(xor_key)] for i, b in enumerate(body))
    structured_tx = header + decoded_body
    payload_hex = structured_tx.hex()
    
    print(f"[+] Preserved Header: {header.hex()}")
    print(f"[+] Structured Hex Length: {len(structured_tx) * 2} chars")
    
    url = "http://127.0.0.1:8332/"
    username = "Cornbread78"
    password = "26a78aea33835e4d74654ce25e3e8b51a0706d8e55353f92b98c73f7ec33f416"
    
    credentials = f"{username}:{password}"
    auth_bytes = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
    
    rpc_payload = {
        "jsonrpc": "1.0",
        "id": "selective_dispatch",
        "method": "sendrawtransaction",
        "params": [payload_hex]
    }
    
    data = json.dumps(rpc_payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={
        'Content-Type': 'application/json',
        'Authorization': f'Basic {auth_bytes}'
    })
    
    try:
        with urllib.request.urlopen(req) as response:
            result = response.read().decode('utf-8')
            print("[+] Daemon Response Success:", result)
    except urllib.error.HTTPError as e:
        err_body = e.read().decode('utf-8', errors='ignore')
        print(f"[-] HTTP Error {e.code}: {e.reason}")
        if err_body:
            print(f"[-] Response Details: {err_body}")
    except Exception as e:
        print(f"[-] RPC Error: {e}")

if __name__ == "__main__":
    selective_xor_dispatch()
