import json
import urllib.request
import base64
import struct

def build_injected_transaction():
    url = "http://127.0.0.1:8332/"
    username = "Cornbread78"
    password = "26a78aea33835e4d74654ce25e3e8b51a0706d8e55353f92b98c73f7ec33f416"
    
    # Version (4 bytes)
    version = bytes([1, 0, 0, 0])
    # Input count (1 byte)
    in_count = bytes([1])
    
    # Injecting the XOR mask pattern [4, 4, 0, 0] directly into the zero-filled prev_txid vector (32 bytes total)
    xor_pattern = bytes([4, 4, 0, 0])
    prev_txid = xor_pattern * 8  
    
    # Vout index (4 bytes)
    prev_index = bytes([0, 0, 0, 0])
    
    # ScriptSig payload
    script_data = bytes.fromhex("0f30342f30342f30302f303057616372")
    script_sig = bytes([len(script_data)]) + script_data
    
    # Sequence (4 bytes)
    sequence = bytes([0xff, 0xff, 0xff, 0xff])
    tx_in = prev_txid + prev_index + script_sig + sequence
    
    # Output structuring
    out_count = bytes([1])
    value = struct.pack("<Q", 50000000)
    
    data_payload = bytes.fromhex("05040000050400000404000004040000040400000404000004040000040400000404000004040000040b30342b34342f34342f303453616376fbfffffb0500f2012e0100040441040404000004040000040400000404000004040000040400000404000004040000a804000004")
    pubkey_script = bytes([0x6a, len(data_payload)]) + data_payload
    script_pub_key_len = bytes([len(pubkey_script)])
    tx_out = value + script_pub_key_len + pubkey_script
    
    lock_time = bytes([0, 0, 0, 0])
    
    structured_tx = version + in_count + tx_in + out_count + tx_out + lock_time
    payload_hex = structured_tx.hex()
    
    print(f"[*] Injected XOR Mask Transaction Hex Generated:")
    print(payload_hex)
    
    credentials = f"{username}:{password}"
    auth_bytes = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
    
    rpc_payload = {
        "jsonrpc": "1.0",
        "id": "injected_dispatch",
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
    build_injected_transaction()
