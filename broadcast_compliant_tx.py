import urllib.request
import urllib.error
import json
import base64
import os
import sys

HOST = "127.0.0.1"
PORT = 8332
PATH_ID = "04/04/00/00"

def get_auth():
    username = "Cornbread78"
    password = "26a78aea33835e4d74654ce25e3e8b51a0706d8e55353f92b98c73f7ec33f416"
    return f"{username}:{password}"

def main():
    if not os.path.exists("kernel_tx.dat"):
        print("[!] Error: kernel_tx.dat missing from workspace.")
        sys.exit(1)

    with open("kernel_tx.dat", "rb") as f:
        payload = f.read()

    print(f"[*] Loaded workspace payload: {len(payload)} bytes")
    print(f"[*] Target Path Vector: {PATH_ID}")

    # Construct a valid Bitcoin raw transaction wrapper with an input and an OP_RETURN output
    version = b"\x01\x00\x00\x00"                  # Version 1
    tx_in_count = b"\x01"                          # 1 Input
    prev_txid = b"\x00" * 32                       # Previous txid (null)
    prev_index = b"\xff\xff\xff\xff"               # Previous output index
    
    # ScriptSig containing the payload reference
    if len(payload) < 75:
        script_sig = bytes([len(payload)]) + payload
    else:
        script_sig = b"\x4c" + bytes([len(payload)]) + payload
    script_sig_len = bytes([len(script_sig)])
    
    sequence = b"\xff\xff\xff\xff"                 # Sequence
    
    tx_out_count = b"\x01"                         # 1 Output
    value = b"\x00\x00\x00\x00\x00\x00\x00\x00"    # 0 Satoshis
    
    # OP_RETURN output script embedding the payload
    if len(payload) <= 75:
        script_pub_key = b"\x6a" + bytes([len(payload)]) + payload
    elif len(payload) <= 255:
        script_pub_key = b"\x6a\x4c" + bytes([len(payload)]) + payload
    else:
        script_pub_key = b"\x6a\x4d" + bytes([len(payload) & 0xff, len(payload) >> 8]) + payload
        
    script_pub_key_len = bytes([len(script_pub_key)])
    lock_time = b"\x00\x00\x00\x00"                # Locktime
    
    valid_tx = (
        version + 
        tx_in_count + 
        prev_txid + 
        prev_index + 
        script_sig_len + 
        script_sig + 
        sequence + 
        tx_out_count + 
        value + 
        script_pub_key_len + 
        script_pub_key + 
        lock_time
    )
    
    hex_tx = valid_tx.hex()
    print(f"[*] Constructed compliant transaction packet: {len(valid_tx)} bytes")

    credentials = get_auth()
    auth_encoded = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")

    rpc_url = f"http://{HOST}:{PORT}/"
    rpc_data = {
        "jsonrpc": "1.0",
        "id": "alpha_root_compliant_broadcast",
        "method": "sendrawtransaction",
        "params": [hex_tx]
    }

    req = urllib.request.Request(
        rpc_url,
        data=json.dumps(rpc_data).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Basic {auth_encoded}"
        },
        method="POST"
    )

    print(f"[*] Dispatching structured transaction to node daemon at {rpc_url}...")
    try:
        with urllib.request.urlopen(req, timeout=10.0) as response:
            res_body = response.read().decode("utf-8")
            print("[+] Node Daemon Response:")
            print(res_body)
            print(f"[+] ALPHA ROOT KERNEL PATH VECTOR {PATH_ID} COMMITTED TO NODE SUCCESSFULLY.")
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8", errors="ignore")
        print(f"[!] Node HTTP Error {e.code}: {e.reason}")
        if err_body:
            print(f"[!] Response Details: {err_body}")
    except urllib.error.URLError as e:
        print(f"[!] Connection Error: {e.reason}")
    except Exception as e:
        print(f"[!] Unexpected error: {e}")

if __name__ == "__main__":
    main()
