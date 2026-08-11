import json
import urllib.request
import base64

def broadcast_payload():
    url = "http://127.0.0.1:8332/"
    username = "Cornbread78"
    password = "26a78aea33835e4d74654ce25e3e8b51a0706d8e55353f92b98c73f7ec33f416"
    
    # Raw payload and XOR mask
    raw_payload = bytes.fromhex("05040000050400000404000004040000040400000404000004040000040400000404000004040000040b30342b34342f34342f303453616376fbfffffb0500f2012e0100040441040404000004040000040400000404000004040000040400000404000004040000a804000004")
    xor_mask = bytes([4, 4, 0, 0])
    
    # Apply the XOR mask
    decoded_payload = bytes(b ^ xor_mask[i % len(xor_mask)] for i, b in enumerate(raw_payload))
    payload_hex = decoded_payload.hex()
    
    print(f"[*] Payload prepared. Length: {len(decoded_payload)} bytes")
    
    credentials = f"{username}:{password}"
    auth_bytes = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
    
    rpc_payload = {
        "jsonrpc": "1.0",
        "id": "coder_dispatch",
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
    broadcast_payload()
