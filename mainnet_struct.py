import os
import json
import urllib.request
import base64

def process_mainnet_transaction():
    print("==================================================")
    print(" MAINNET TRANSACTION STRUCTURING & DISPATCH")
    print("==================================================")
    
    # Target files
    kernel_path = "kernel_tx.dat"
    masked_path = "xor_masked_kernel_tx.dat"
    xor_path = "blocks/xor.dat"
    
    if os.path.exists(kernel_path):
        with open(kernel_path, "rb") as f:
            tx_data = f.read()
        print(f"[+] Loaded {kernel_path}: {len(tx_data)} bytes")
    elif os.path.exists(masked_path):
        with open(masked_path, "rb") as f:
            raw_payload = f.read()
        xor_mask = bytes([4, 4, 0, 0])
        tx_data = bytes(b ^ xor_mask[i % 4] for i, b in enumerate(raw_payload))
        print(f"[+] Loaded and unmasked {masked_path}: {len(tx_data)} bytes")
    else:
        print("[-] Error: Transaction data files not found.")
        return

    # Load block XOR modifier if present
    if os.path.exists(xor_path):
        with open(xor_path, "rb") as f:
            block_xor = f.read()
        print(f"[+] Loaded block XOR modifier ({len(block_xor)} bytes)")
    
    payload_hex = tx_data.hex()
    print(f"[+] Final Structured Mainnet Hex Length: {len(tx_data) * 2} chars")
    print(f"[+] Hex Preview: {payload_hex[:64]}...")
    
    # RPC Connection details for local node daemon
    url = "http://127.0.0.1:8332/"
    username = "Cornbread78"
    password = "26a78aea33835e4d74654ce25e3e8b51a0706d8e55353f92b98c73f7ec33f416"
    
    credentials = f"{username}:{password}"
    auth_bytes = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
    
    rpc_payload = {
        "jsonrpc": "1.0",
        "id": "mainnet_struct_dispatch",
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
    process_mainnet_transaction()
