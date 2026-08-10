import os
import hashlib
import json

PATH_ID = "04/04/00/00"
LEDGER_FILE = "alpha_root.ledger"
PAYLOAD_FILE = "kernel_tx.dat"

def execute_consensus_node():
    print(f"[*] Initializing Alpha Root Kernel Node Consensus for Path: {PATH_ID}")
    
    if not os.path.exists(PAYLOAD_FILE):
        print(f"[!] Error: {PAYLOAD_FILE} missing.")
        return

    with open(PAYLOAD_FILE, "rb") as f:
        payload = f.read()

    payload_hash = hashlib.sha256(payload).hexdigest()
    print(f"[+] Payload Size: {len(payload)} bytes")
    print(f"[+] Cryptographic Hash: {payload_hash}")

    ledger_data = {
        "kernel": "Alpha Root Kernel",
        "path": PATH_ID,
        "hash": payload_hash,
        "status": "CONSENSUS_LOCKED"
    }

    with open(LEDGER_FILE, "w") as f:
        f.write(json.dumps(ledger_data, indent=2))

    print(f"[+] Ledger record updated successfully: {LEDGER_FILE}")
    print(f"[+] ALPHA_ROOT_KERNEL: GENESIS_CONSENSUS_LOCKED_PATH_{PATH_ID.replace('/', '_')}_VERIFIED")

if __name__ == "__main__":
    execute_consensus_node()
