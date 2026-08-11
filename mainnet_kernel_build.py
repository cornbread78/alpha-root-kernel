import os
import json
import urllib.request
import base64

def process_kernel_files():
    print("==================================================")
    print(" ALPHA ROOT KERNEL - MAINNET TRANSACTION BUILDER")
    print("==================================================")
    
    # Load kernel transaction data
    if os.path.exists("kernel_tx.dat"):
        with open("kernel_tx.dat", "rb") as f:
            kernel_data = f.read()
        print(f"[+] Loaded kernel_tx.dat: {len(kernel_data)} bytes")
    else:
        print("[-] Error: kernel_tx.dat not found.")
        return
        
    # Load block XOR modifier if present
    if os.path.exists("blocks/xor.dat"):
        with open("blocks/xor.dat", "rb") as f:
            block_xor = f.read()
        print(f"[+] Loaded blocks/xor.dat modifier: {block_xor.hex()}")

    # Structure version and input count
    version = kernel_data[0:4]
    in_count = kernel_data[4:5]
    
    # Apply the XOR mask [4, 4, 0, 0] into the 32-byte zero-filled prev_txid vector
    xor_mask_pattern = bytes([4, 4, 0, 0])
    prev_txid = xor_mask_pattern * 8  # 32 bytes total
    
    # Append the remaining transaction structure (index, scriptSig, sequence, outputs, locktime)
    rest_of_tx = kernel_data[37:]
    
    structured_tx = version + in_count + prev_txid + rest_of_tx
    payload_hex = structured_tx.hex()
    
    print(f"[+] Final Mainnet Structured Hex ({len(structured_tx)} bytes):")
    print(payload_hex)
    
    # RPC dispatch to local daemon node
    url = "http://127.0.0.1:8332/"
    username = "Cornbread78"
    password = "26a78aea33835e4d74654ce25e3e8b51a0706d8e55353f92b98c73f7ec33f416"
    
    credentials = f"{username}:{password}"
    auth_bytes = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
    
    rpc_payload = {
        "jsonrpc": "1.0",
        "id": "mainnet_final_dispatch",
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
    process_kernel_files()
