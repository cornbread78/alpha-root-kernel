import subprocess
import os

def submit_to_local_node():
    rpc_user = "Cornbread78"
    rpc_pass = "26a78aea33835e4d74654ce25e3e8b51a0706d8e55353f92b98c73f7ec33f416"
    
    # Correctly read file bytes and convert to hex
    if os.path.exists("kernel_tx.dat"):
        with open("kernel_tx.dat", "rb") as f:
            tx_hex = f.read().hex()
    else:
        tx_hex = "0100000001000000000000000000000000000000000000000000000000000000000000000000000000ffffffff0100000000000000000b6a09636f6d6520686f6d6500000000"

    print("==================================================")
    print(" BITCOIN CORE - LOCAL NODE RPC DISPATCH")
    print("==================================================")
    print(f"[*] Submitting raw payload to local daemon (Mainnet)...")

    cmd = [
        "bitcoin-cli",
        f"-rpcuser={rpc_user}",
        f"-rpcpassword={rpc_pass}",
        "sendrawtransaction",
        tx_hex
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print("[+] Node Acceptance Response:")
        print(result.stdout.strip())
    except subprocess.CalledProcessError as e:
        print("[!] Node Rejection Error:")
        print(e.stderr.strip())

if __name__ == "__main__":
    submit_to_local_node()
