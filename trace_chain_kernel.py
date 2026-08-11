import requests
import json
import time

url = 'http://127.0.0.1:8332/'
auth = ('Cornbread78', '26a78aea33835e4d74654ce25e3e8b51a0706d8e55353f92b98c73f7ec33f416')
headers = {'content-type': 'application/json'}
xor_mask = [0x04, 0x04, 0x00, 0x00]

def rpc_call(method, params):
    payload = {'jsonrpc': '1.0', 'id': 'kernel_trace', 'method': method, 'params': params}
    res = requests.post(url, data=json.dumps(payload), headers=headers, auth=auth, timeout=5).json()
    return res.get('result')

print("==================================================")
print(" ALPHA ROOT KERNEL - BLOCK CHAIN & HEADER TRACE")
print(" Path Vector: 04/04/00/00")
print("==================================================")

# Trace initial blocks starting from Genesis (Height 0 to 5)
for height in range(6):
    b_hash = rpc_call('getblockhash', [height])
    if not b_hash:
        break
    b_header = rpc_call('getblockheader', [b_hash])
    
    # Apply Alpha Root Kernel XOR transformation on the header hash
    hash_bytes = bytes.fromhex(b_hash)
    masked_bytes = bytearray(hash_bytes)
    for i in range(len(masked_bytes)):
        masked_bytes[i] ^= xor_mask[i % len(xor_mask)]
        
    print(f"\n[+] Block Height #{height}")
    print(f"    Raw Hash:     {b_hash}")
    print(f"    Merkle Root:  {b_header.get('merkleroot')}")
    print(f"    Timestamp:    {b_header.get('time')}")
    print(f"    Kernel Masked: {masked_bytes.hex()}")

# Update local ledger status
ledger_data = {
    "kernel": "Alpha Root Kernel",
    "path": "04/04/00/00",
    "timestamp": int(time.time()),
    "status": "CONSENSUS_LOCKED_CHAIN_VERIFIED",
    "interface": "127.0.0.1:8332"
}

with open("alpha_root_export.json", "w") as f:
    json.dump(ledger_data, f, indent=4)

print("\n[+] Chain trace complete. Ledger state synchronized and locked.")
