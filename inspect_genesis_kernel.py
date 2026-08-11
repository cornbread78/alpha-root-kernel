import requests
import json

url = 'http://127.0.0.1:8332/'
auth = ('Cornbread78', '26a78aea33835e4d74654ce25e3e8b51a0706d8e55353f92b98c73f7ec33f416')
headers = {'content-type': 'application/json'}

print("[*] Querying local Bitcoin node for Genesis Block (Height 0)...")

# 1. Fetch Genesis Block Hash
payload_hash = {
    'jsonrpc': '1.0',
    'id': 'genesis_hash',
    'method': 'getblockhash',
    'params': [0]
}

try:
    res = requests.post(url, data=json.dumps(payload_hash), headers=headers, auth=auth, timeout=5).json()
    genesis_hash = res.get('result')
    print(f"[+] Genesis Block Hash: {genesis_hash}")

    # 2. Fetch Genesis Block Header
    payload_header = {
        'jsonrpc': '1.0',
        'id': 'genesis_header',
        'method': 'getblockheader',
        'params': [genesis_hash]
    }
    header_res = requests.post(url, data=json.dumps(payload_header), headers=headers, auth=auth, timeout=5).json()
    header_data = header_res.get('result')

    print("\n--- Genesis Block Header Fields ---")
    for key, value in header_data.items():
        print(f"  {key}: {value}")

    # 3. Apply Alpha Root Kernel XOR Mask Transformation
    xor_mask = [0x04, 0x04, 0x00, 0x00]
    hash_bytes = bytes.fromhex(genesis_hash)
    masked_bytes = bytearray(hash_bytes)
    for i in range(len(masked_bytes)):
        masked_bytes[i] ^= xor_mask[i % len(xor_mask)]

    print("\n--- Alpha Root Kernel Transformation ---")
    print(f"  Path Vector: 04/04/00/00")
    print(f"  XOR Mask: {xor_mask}")
    print(f"  Transformed Genesis Hash: {masked_bytes.hex()}")

except Exception as e:
    print(f"[!] Error communicating with node RPC: {e}")
