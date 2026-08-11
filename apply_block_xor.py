import os
import json
import urllib.request
import base64

def decode_with_block_xor():
    print("==================================================")
    print(" ALPHA ROOT KERNEL - BLOCK XOR DECODER & DISPATCH")
    print("==================================================")
    
    xor_path = "blocks/xor.dat"
    kernel_path = "kernel_tx.dat"
    
    if os.path.exists(xor_path):
        with open(xor_path, "rb") as f:
            xor_key = f.read()
        print(f"[+] Loaded XOR Key: {xor_key.hex()}")
    else:
        xor_key = bytes.fromhex("d923edcf24bbc601")
        print(f"[+] Using Default XOR Key: {xor_key.hex()}")
        
    if os.path.exists(kernel_path):
        with open(kernel_path, "rb") as f:
            raw_data = f.read()
        print(f"[+] Loaded {kernel_path}: {len(raw_data)} bytes")
    else:
        print("[-] Error: kernel_tx.dat not found.")
        return

    # Apply repeating 8-byte block XOR key
    decoded_data = bytes(b ^ xor_key[i % len(xor_key)] for i, b in enumerate(raw_data))
    payload_hex = decoded_data.hex()
    
    print(f"[+] Decoded Payload Hex Length: {len(decoded_data) * 2} chars")
    print(f"[+] Hex Preview: {payload_hex[:64]}...")
    
    # RPC Connection details
    url = "http://127.0.0.1:8332/"
    username = "Cornbread78"
    password = "26a78aea33835e4d74654ce25e3e8b51a0706d8e55353f92b98c73f7ec33f416"
    
    credentials = f"{username}:{password}"
    auth_bytes = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
    
    rpc_payload = {
        "jsonrpc": "1.0",
        "id": "block_xor_dispatch",
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
    decode_with_block_xor()
