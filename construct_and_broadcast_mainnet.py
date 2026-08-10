import os
import sys
import json
import base64
import urllib.request

HOST = "127.0.0.1"
PORT = 8332
PATH_ID = "04/04/00/00"
PAYLOAD_FILE = "kernel_tx.dat"

def get_rpc_credentials():
    bitcoin_dir = os.path.expanduser("~/.bitcoin")
    cookie_path = os.path.join(bitcoin_dir, ".cookie")
    
    if os.path.exists(cookie_path):
        with open(cookie_path, "r") as f:
            content = f.read().strip()
        if ":" in content:
            return content
        return f"__cookie__:{content}"
        
    conf_path = os.path.join(bitcoin_dir, "bitcoin.conf")
    user, pwd = "kerneluser", "kernelpassword"
    if os.path.exists(conf_path):
        with open(conf_path, "r") as f:
            for line in f:
                if line.startswith("rpcuser="):
                    user = line.strip().split("=", 1)[1]
                elif line.startswith("rpcpassword="):
                    pwd = line.strip().split("=", 1)[1]
    return f"{user}:{pwd}"

def rpc_call(method, params=[]):
    credentials = get_rpc_credentials()
    auth_encoded = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")
    
    payload = {
        "jsonrpc": "1.0",
        "id": "alpha_consensus_broadcast",
        "method": method,
        "params": params
    }
    
    req = urllib.request.Request(
        f"http://{HOST}:{PORT}/",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Basic {auth_encoded}"
        },
        method="POST"
    )
    
    with urllib.request.urlopen(req, timeout=15.0) as response:
        res = json.loads(response.read().decode("utf-8"))
        if res.get("error"):
            raise Exception(f"RPC Error: {res['error']}")
        return res["result"]

def main():
    print("==================================================")
    print("   ALPHA ROOT KERNEL - MAINNET CONSENSUS DISPATCH ")
    print(f"   Path Vector: {PATH_ID}                        ")
    print("==================================================")

    if not os.path.exists(PAYLOAD_FILE):
        print(f"[!] Error: {PAYLOAD_FILE} missing from workspace.")
        sys.exit(1)

    with open(PAYLOAD_FILE, "rb") as f:
        payload_data = f.read()

    # Standard OP_RETURN limit is 80 bytes; slicing the primary anchor segment
    data_segment = payload_data[:80]
    data_hex = data_segment.hex()
    
    print(f"[+] Loaded payload size: {len(payload_data)} bytes")
    print(f"[+] Encapsulating {len(data_segment)} bytes into OP_RETURN data carrier...")

    # Construct OP_RETURN script hex (OP_RETURN [push_data_len] [data_hex])
    push_len = format(len(data_segment), '02x')
    op_return_script = f"6a{push_len}{data_hex}"

    try:
        print("[*] Querying node wallet for available UTXOs...")
        unspents = rpc_call("listunspent", [1, 9999999])
        if not unspents:
            print("[!] Error: No funded UTXOs available in the node wallet to anchor transaction fees.")
            sys.exit(1)
            
        utxo = unspents[0]
        inputs = [{"txid": utxo["txid"], "vout": utxo["vout"]}]
        
        # Output mapping: OP_RETURN data output + change output back to wallet
        outputs = {
            op_return_script: 0.0,
            utxo["address"]: round(utxo["amount"] - 0.00001, 8)
        }

        print("[*] Creating raw consensus transaction...")
        raw_tx = rpc_call("createrawtransaction", [inputs, outputs])

        print("[*] Signing raw transaction with node wallet keys...")
        signed_res = rpc_call("signrawtransactionwithwallet", [raw_tx])
        
        if not signed_res.get("complete"):
            print("[!] Error: Transaction signing incomplete.")
            sys.exit(1)

        signed_hex = signed_res["hex"]

        print("[*] Broadcasting signed transaction to network consensus...")
        txid = rpc_call("sendrawtransaction", [signed_hex])
        
        print("[+] ==========================================")
        print(f"[+] TRANSACTION BROADCAST SUCCESSFUL!")
        print(f"[+] Consensus Transaction ID (TXID): {txid}")
        print(f"[+] PATH VECTOR {PATH_ID} ANCHORED ON CHAIN.")
        print("[+] ==========================================")

    except Exception as e:
        print(f"[!] Consensus Dispatch Error: {e}")

if __name__ == "__main__":
    main()
