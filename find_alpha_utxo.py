import os
import hashlib

PAYLOAD_FILE = "kernel_tx.dat"
PATH_VECTOR = "04/04/00/00"

def locate_alpha_utxo():
    print("==================================================")
    print("   ALPHA ROOT KERNEL - UTXO & SOURCE SCANNER      ")
    print(f"   Path Vector: {PATH_VECTOR}")
    print("==================================================")

    if not os.path.exists(PAYLOAD_FILE):
        print(f"[!] Error: {PAYLOAD_FILE} missing from workspace.")
        return

    with open(PAYLOAD_FILE, "rb") as f:
        raw_data = f.read()

    print(f"[+] Loaded payload file: {len(raw_data)} bytes")
    
    # Parse transaction structure components
    version = raw_data[0:4]
    in_count = raw_data[4:5]
    prev_tx = raw_data[5:37]
    prev_idx = raw_data[37:41]
    
    # Compute proof hash
    payload_hash = hashlib.sha256(raw_data).hexdigest()

    print(f"[+] Transaction Version (Hex): {version.hex()}")
    print(f"[+] Input Count: {in_count[0]}")
    print(f"[+] Referenced Prev TX (UTXO Source ID): {prev_tx.hex()}")
    print(f"[+] Output Index Reference: {int.from_bytes(prev_idx, 'little')}")
    print(f"[+] Computed Kernel Payload Hash: {payload_hash}")
    print("--------------------------------------------------")
    print(f"[+] ALPHA_ROOT_KERNEL: UTXO_LOCATED_PATH_{PATH_VECTOR.replace('/', '_')}")
    print("==================================================")

if __name__ == "__main__":
    locate_alpha_utxo()
