import os
import json
import base64
import requests

RPC_HOST = "127.0.0.1"
RPC_PORT = 8332
RPC_URL = f"http://{RPC_HOST}:{RPC_PORT}"
RPC_USER = "Cornbread78"
RPC_PASS = "26a78aea33835e4d74654ce25e3e8b51a0706d8e55353f92b98c73f7ec33f416"
PATH_VECTOR = "04/04/00/00"

def rpc_call(method, params=[]):
    headers = {'content-type': 'application/json'}
    payload = {
        "method": method,
        "params": params,
        "jsonrpc": "2.0",
        "id": "alpha_compliant_broadcast"
    }
    response = requests.post(RPC_URL, data=json.dumps(payload), headers=headers, auth=(RPC_USER, RPC_PASS), timeout=15)
    return response.status_code, response.json()

def main():
    print("==================================================")
    print("   ALPHA ROOT KERNEL - COMPLIANT TX DISPATCH      ")
    print(f"   Path Vector: {PATH_VECTOR}")
    print("==================================================")

    # Load workspace payload if available, else fallback to standard carrier string
    payload_file = "kernel_tx.dat"
    if os.path.exists(payload_file):
        with open(payload_file, "rb") as f:
            raw_data = f.read()
        print(f"[+] Loaded workspace payload: {len(raw_data)} bytes")
    else:
        raw_data = b"come home"
        print(f"[+] Using default payload carrier bytes")

    # Constructing a valid raw transaction hex frame with an OP_RETURN output script
    # Format: Version (4) | In-Count (1) | Outpoint (36) | ScriptSigLen (1) | ScriptSig (0) | Sequence (4) 
    #         | Out-Count (1) | Value (8) | ScriptLen (1) | OP_RETURN + Data | Locktime (4)
    
    op_return_data = b"\x6a" + bytes([len(raw_data)]) + raw_data
    script_len = bytes([len(op_return_data)])

    # Constructing standard transaction frame shell for decoder compliance
    tx_hex = (
        "01000000" +                               # Version 1
        "01" +                                     # Input count: 1
        "00"*32 + "00000000" +                     # Previous outpoint (Null txid + index)
        "00" +                                     # Empty scriptSig
        "ffffffff" +                               # Sequence
        "01" +                                     # Output count: 1
        "0000000000000000" +                       # Value: 0 Satoshis
        script_len.hex() +                         # Script length
        op_return_data.hex() +                     # OP_RETURN payload script
        "00000000"                                 # Locktime
    )

    print(f"[+] Constructed compliant transaction hex ({len(tx_hex)//2} bytes)")
    print(f"[*] Dispatching transaction to node daemon via RPC...")

    status, result = rpc_call("decoderawtransaction", [tx_hex])
    print(f"[+] Decoder Response Status: {status}")
    print(f"[+] Decoder Result:\n{json.dumps(result, indent=2)}")

if __name__ == "__main__":
    main()
