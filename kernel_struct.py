import json
import urllib.request
import base64
import struct

def structure_alpha_kernel():
    url = "http://127.0.0.1:8332/"
    username = "Cornbread78"
    password = "26a78aea33835e4d74654ce25e3e8b51a0706d8e55353f92b98c73f7ec33f416"
    
    # Raw payload and XR mask application
    raw_payload = bytes.fromhex("05040000050400000404000004040000040400000404000004040000040400000404000004040000040b30342b34342f34342f303453616376fbfffffb0500f2012e0100040441040404000004040000040400000404000004040000040400000404000004040000a804000004")
    xor_mask = bytes([4, 4, 0, 0])
    decoded = bytes(b ^ xor_mask[i % 4] for i, b in enumerate(raw_payload))
    
    # Structural Mapping: Version & Input Count
    version = bytes([1, 0, 0, 0])
    in_count = bytes([1])
    
    # Alpha Root Kernel alignment: Embedding 04040000 directly in the middle of the 32-byte prev_txid vector
    kernel_marker = bytes([4, 4, 0, 0])
    prev_txid = decoded[0:14] + kernel_marker + decoded[14:30]
    
    # Input index and scriptSig packaging
    prev_index = bytes([0, 0, 0, 0])
    script_data = decoded[30:]
    
    if len(script_data) < 75:
        script_sig = bytes([len(script_data)]) + script_data
    else:
        script_sig = bytes([0x4c, len(script_data)]) + script_data
        
    sequence = bytes([0xff, 0xff, 0xff, 0xff])
    tx_in = prev_txid + prev_index + script_sig + sequence
    
    # Output structuring with proper value and scriptPubKey layout
    out_count = bytes([1])
    value = struct.pack("<Q", 50000000)
    
    pubkey_script = bytes([0x6a, len(decoded)]) + decoded
    script_pub_key_len = bytes([len(pubkey_script)])
    tx_out = value + script_pub_key_len + pubkey_script
    
    lock_time = bytes([0, 0, 0, 0])
    
    structured_tx = version + in_count + tx_in + out_count + tx_out + lock_time
    payload_hex = structured_tx.hex()
    
    print(f"[*] Kernel Structure Generated Successfully")
    print(f"[*] Payload Hex: {payload_hex}")
    
    credentials = f"{username}:{password}"
    auth_bytes = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
    
    rpc_payload = {
        "jsonrpc": "1.0",
        "id": "kernel_dispatch",
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
            print("Daemon Response Success:", result)
    except urllib.error.HTTPError as e:
        err_body = e.read().decode('utf-8', errors='ignore')
        print(f"HTTP Error {e.code}: {e.reason}")
        if err_body:
            print(f"Response Details: {err_body}")
    except Exception as e:
        print(f"RPC Error: {e}")

if __name__ == "__main__":
    structure_alpha_kernel()
