import os
import hashlib

def extract_utxo_from_kernel():
    filename = "kernel_tx.dat"
    print("==================================================")
    print("   ALPHA ROOT KERNEL - UTXO EXTRACTOR SCRIPT      ")
    print("==================================================")

    if not os.path.exists(filename):
        print(f"[!] Error: {filename} not found in workspace.")
        return

    with open(filename, "rb") as f:
        raw_tx = f.read()

    print(f"[+] Total Payload Size: {len(raw_tx)} bytes")

    # Parse transaction structure layout
    version = raw_tx[0:4]
    in_count = raw_tx[4:5]
    prev_txid = raw_tx[5:37]
    prev_vout = raw_tx[37:41]

    tx_hash = hashlib.sha256(raw_tx).hexdigest()

    print(f"[+] Transaction Version: {version.hex()}")
    print(f"[+] Input Count: {in_count[0]}")
    print(f"[+] UTXO Source Prev TXID: {prev_txid.hex()}")
    print(f"[+] UTXO Source VOUT Index: {int.from_bytes(prev_vout, 'little')}")
    print(f"[+] Transaction SHA-256 Hash: {tx_hash}")
    print("--------------------------------------------------")
    print("[+] ALPHA_ROOT_KERNEL: UTXO_EXTRACTION_SUCCESS")
    print("==================================================")

if __name__ == "__main__":
    extract_utxo_from_kernel()
