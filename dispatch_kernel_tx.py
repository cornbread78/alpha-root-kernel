import json
import urllib.request
import base64

def run():
    url = "http://127.0.0.1:8332/"
    username = "Cornbread78"
    password = "26a78aea33835e4d74654ce25e3e8b51a0706d8e55353f92b98c73f7ec33f416"
    
    # Raw payload bytes
    raw_payload = bytes.fromhex("05040000050400000404000004040000040400000404000004040000040400000404000004040000040b30342b34342f34342f303453616376fbfffffb0500f2012e0100040441040404000004040000040400000404000004040000040400000404000004040000a804000004")
    
    # Apply XOR mask [4, 4, 0, 0] to the buffer as per Alpha Root Kernel path vector 04/04/00/00
    xor_mask = bytes([4, 4, 0, 0])
    masked_payload = bytes(b ^ xor_mask[i % 4] for i, b in enumerate(raw_payload))
    
    # Construct structured transaction layout incorporating the masked payload
    version = b"\x01\x00\x00\x00"
    tx_in_count = b"\x01"
    
    if len(masked_payload) < 75:
        script_sig = bytes([len(masked_payload)]) + masked_payload
    else:
        script_sig = b"\x4c" + bytes([len(masked_payload)]) + masked_payload
        
    prev_txid = b"\x00" * 32
    prev_index = b"\xff\xff\xff\xff"
    script_sig_len = bytes([len(script_sig)])
    sequence = b"\xff\xff\xff\xff"
    
    tx_in = prev_txid + prev_index + script_sig_len + script_sig + sequence
    
    tx_out_count = b"\x01"
    value = b"\x00\x00\x00\x00\x00\x00\x00\x00"
    
    # OP_RETURN output script embedding the masked payload
    if len(masked_payload) <= 75:
        script_pub_key = b"\x6a" + bytes([len(masked_payload)]) + masked_payload
    elif len(masked_payload) <= 255:
        script_pub_key = b"\x6a\x4c" + bytes([len(masked_payload)]) + masked_payload
    else:
        script_pub_key = b"\x6a\x4d" + bytes([len(masked_payload) & 0xff, len(masked_payload) >> 8]) + masked_payload
        
    script_pub_key_len = bytes([len(script_pub_key)])
    tx_out = value + script_pub_key_len + script_pub_key
    
    lock_time = b"\x00\x00\x00\x00"
    
    compliant_tx = version + tx_in_count + tx_in + tx_out_count + tx_out + lock_time
    payload_hex = compliant_tx.hex()
    
    print(f"[+] Compliant Kernel Transaction Hex: {payload_hex}")
    
    credentials = f"{username}:{password}"
    auth_bytes = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
    
    rpc_payload = {
        "jsonrpc": "1.0",
        "id": "node_dispatch",
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
            print("Daemon Response:", result)
    except urllib.error.HTTPError as e:
        err_body = e.read().decode('utf-8', errors='ignore')
        print(f"HTTP Error {e.code}: {e.reason}")
        if err_body:
            print(f"Response Details: {err_body}")
    except Exception as e:
        print(f"RPC Error: {e}")

if __name__ == "__main__":
    run()
