import os
import sys
import json
import base64
import urllib.request

HOST = "127.0.0.1"
PORT = 8332
PATH_ID = "04/04/00/00"
PAYLOAD_FILE = "kernel_tx.dat"

def get_auth():
    username = "Cornbread78"
    password = "26a78aea33835e4d74654ce25e3e8b51a0706d8e55353f92b98c73f7ec33f416"
    return base64.b64encode(f"{username}:{password}".encode("utf-8")).decode("utf-8")

def rpc_call(method, params=[]):
    auth_encoded = get_auth()
    payload = {
        "jsonrpc": "1.0",
        "id": "alpha_robust_wallet",
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
            raise Exception(f"RPC Error {res['error']['code']}: {res['error']['message']}")
        return res["result"]

def main():
    print("==================================================")
    print("   ALPHA ROOT KERNEL - ROBUST WALLET DISPATCH     ")
    print(f"   Path Vector: {PATH_ID}                        ")
    print("==================================================")

    if not os.path.exists(PAYLOAD_FILE):
        print(f"[!] Error: {PAYLOAD_FILE} missing from workspace.")
        sys.exit(1)

    with open(PAYLOAD_FILE, "rb") as f:
        payload_data = f.read()

    print(f"[+] Loaded payload size: {len(payload_data)} bytes")

    try:
        # Ensure wallet is loaded
        print("[*] Checking node wallet status...")
        wallets = rpc_call("listwallets", [])
        if not wallets:
            print("[*] No active wallets loaded. Attempting to load default wallet...")
            try:
                rpc_call("loadwallet", [""])
            except Exception:
                # Try loading standard wallet name if empty string fails
                try:
                    rpc_call("loadwallet", ["wallet"])
                except Exception as ex:
                    print(f"[!] Warning on wallet load: {ex}")

        print("[*] Querying node wallet for unspent transaction outputs (UTXOs)...")
        unspents = rpc_call("listunspent", [1, 9999999])
        if not unspents:
            print("[!] Error: No funded UTXOs available in the node wallet.")
            print("[*] Please ensure your node wallet has confirmed funds to cover transaction fees.")
            sys.exit(1)

        utxo = unspents[0]
        print(f"[+] Found UTXO: {utxo['txid']}:{utxo['vout']} (Amount: {utxo['amount']} BTC)")

        # Prepare OP_RETURN payload (max standard 80 bytes for single OP_RETURN relay)
        data_segment = payload_data[:80]
        data_hex = data_segment.hex()
        push_len = format(len(data_segment), '02x')
        op_return_script = f"6a{push_len}{data_hex}"

        inputs = [{"txid": utxo["txid"], "vout": utxo["vout"]}]
        
        fee = 0.00002000
        change_amount = utxo["amount"] - fee
        if change_amount <= 0:
            print("[!] Error: UTXO amount too small to cover transaction fee.")
            sys.exit(1)

        change_address = rpc_call("getrawchangeaddress", [])

        outputs = {
            op_return_script: 0.0,
            change_address: round(change_amount, 8)
        }

        print("[*] Creating raw transaction...")
        raw_tx = rpc_call("createrawtransaction", [inputs, outputs])

        print("[*] Signing raw transaction with wallet keys...")
        signed_res = rpc_call("signrawtransactionwithwallet", [raw_tx])
        if not signed_res.get("complete"):
            print("[!] Error: Transaction signing incomplete.")
            sys.exit(1)

        signed_hex = signed_res["hex"]

        print("[*] Broadcasting signed transaction to live Bitcoin node...")
        txid = rpc_call("sendrawtransaction", [signed_hex])

        print("[+] ==========================================")
        print(f"[+] TRANSACTION BROADCASTED SUCCESSFULLY!")
        print(f"[+] Transaction ID (TXID): {txid}")
        print(f"[+] PATH VECTOR {PATH_ID} ANCHORED VIA CONSENSUS.")
        print("[+] ==========================================")

    except Exception as e:
        print(f"[!] Broadcast Error: {e}")

if __name__ == "__main__":
    main()
