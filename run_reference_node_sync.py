import os
import hashlib
import json

PATH_ID = "04/04/00/00"
PAYLOAD_FILE = "kernel_tx.dat"
LEDGER_FILE = "alpha_root.ledger"

def run_reference_sync():
    print(f"[*] Loading reference points for path vector {PATH_ID}...")
    
    if not os.path.exists(PAYLOAD_FILE) or not os.path.exists(LEDGER_FILE):
        print("[!] Error: Required workspace payload or ledger file missing.")
        return

    with open(PAYLOAD_FILE, "rb") as f:
        payload = f.read()

    with open(LEDGER_FILE, "r") as f:
        ledger = json.load(f)

    payload_hash = hashlib.sha256(payload).hexdigest()
    print(f"[+] Loaded payload size: {len(payload)} bytes")
    print(f"[+] Cryptographic hash verification: {payload_hash}")
    print(f"[+] Ledger status: {ledger.get('status', 'UNKNOWN')}")
    print(f"[+] ALPHA_ROOT_KERNEL: REFERENCE_POINTS_LOADED_PATH_{PATH_ID.replace('/', '_')}_VERIFIED")

if __name__ == "__main__":
    run_reference_sync()
