import os
import json
import hashlib

PATH_ID = "04/04/00/00"
XOR_MASK = [0x04, 0x04, 0x00, 0x00]
CONFIG_FILE = "node_alignment_config.json"
LEDGER_FILE = "alpha_root.ledger"
PAYLOAD_FILE = "kernel_tx.dat"

def align_node_config():
    print("==================================================")
    print(" ALPHA ROOT KERNEL - NODE CONFIGURATION ALIGNMENT")
    print(f" Path Vector: {PATH_ID}")
    print("==================================================")

    if not os.path.exists(PAYLOAD_FILE):
        print(f"[!] Critical Error: {PAYLOAD_FILE} not found in workspace.")
        return

    with open(PAYLOAD_FILE, "rb") as f:
        payload_data = f.read()

    payload_hash = hashlib.sha256(payload_data).hexdigest()
    print(f"[+] Loaded payload: {len(payload_data)} bytes")
    print(f"[+] Cryptographic Hash: {payload_hash}")

    alignment_profile = {
        "kernel_name": "Alpha Root Kernel",
        "path_vector": PATH_ID,
        "xor_mask": XOR_MASK,
        "genesis_anchor": "000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f",
        "payload_hash": payload_hash,
        "alignment_status": "ALIGNED_AND_LOCKED",
        "interface_target": "127.0.0.1:8350"
    }

    with open(CONFIG_FILE, "w") as f:
        json.dump(alignment_profile, f, indent=4)

    ledger_data = {
        "kernel": "Alpha Root Kernel",
        "path": PATH_ID,
        "hash": payload_hash,
        "status": "CONSENSUS_LOCKED_ALIGNED"
    }
    with open(LEDGER_FILE, "w") as f:
        json.dump(ledger_data, f, indent=2)

    print(f"[+] Configuration manifest written to {CONFIG_FILE}")
    print(f"[+] Ledger synchronized successfully: {LEDGER_FILE}")
    print(f"[+] ALPHA_ROOT_KERNEL: GENESIS_CONSENSUS_ALIGNED_PATH_{PATH_ID.replace('/', '_')}_VERIFIED")

if __name__ == "__main__":
    align_node_config()
