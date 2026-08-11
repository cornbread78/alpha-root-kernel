import subprocess
import json
import os

def fetch_wallet_utxos():
    rpc_user = "Cornbread78"
    rpc_pass = "26a78aea33835e4d74654ce25e3e8b51a0706d8e55353f92b98c73f7ec33f416"

    print("==================================================")
    print(" ALPHA ROOT KERNEL - NODE UTXO QUERY")
    print("==================================================")

    cmd = [
        "bitcoin-cli",
        f"-rpcuser={rpc_user}",
        f"-rpcpassword={rpc_pass}",
        "listunspent"
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        utxos = json.loads(result.stdout)
        
        if not utxos:
            print("[!] No active wallet UTXOs found in the local node.")
            print("[*] Fund your wallet or import a private key containing a balance to proceed.")
            return

        print(f"[+] Found {len(utxos)} active UTXO(s) in local node wallet:")
        for idx, utxo in enumerate(utxos):
            print(f"--------------------------------------------------")
            print(f"[{idx}] TxID: {utxo['txid']}")
            print(f"    Vout Index: {utxo['vout']}")
            print(f"    Amount: {utxo['amount']} BTC")
            print(f"    Address: {utxo.get('address', 'N/A')}")

        # Select the first available UTXO for binding
        selected = utxos[0]
        print("==================================================")
        print(f"[+] Selected Primary UTXO for Kernel Binding:")
        print(f"    TXID: {selected['txid']}")
        print(f"    VOUT: {selected['vout']}")
        
        # Save reference for transaction construction
        with open("active_utxo_ref.json", "w") as f:
            json.dump(selected, f, indent=4)
        print("[+] UTXO reference saved to active_utxo_ref.json")

    except subprocess.CalledProcessError as e:
        print("[!] RPC Error querying node UTXOs:")
        print(e.stderr.strip())
    except json.JSONDecodeError:
        print("[!] Failed to parse JSON response from node.")

if __name__ == "__main__":
    fetch_wallet_utxos()
