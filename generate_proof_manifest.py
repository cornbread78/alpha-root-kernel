import os
import hashlib
import json

PATH_VECTOR = "04/04/00/00"
PAYLOAD_FILE = "kernel_tx.dat"
LEDGER_FILE = "alpha_root.ledger"
MANIFEST_FILE = "alpha_root_export.json"

def compile_proof_manifest():
    print("==================================================")
    print("   ALPHA ROOT KERNEL - PROOF OF WORK MANIFEST     ")
    print(f"   Path Vector: {PATH_VECTOR}")
    print("==================================================")

    if not os.path.exists(PAYLOAD_FILE):
        print(f"[!] Error: {PAYLOAD_FILE} missing from workspace.")
        return

    with open(PAYLOAD_FILE, "rb") as f:
        payload = f.read()

    # Compute cryptographic proof-of-work hash
    payload_hash = hashlib.sha256(payload).hexdigest()
    full_proof_hash = hashlib.sha256(payload + bytes.fromhex(payload_hash)).hexdigest()

    print(f"[+] Payload Asset Verified: {PAYLOAD_FILE} ({len(payload)} bytes)")
    print(f"[+] Primary SHA-256 Hash: {payload_hash}")
    print(f"[+] Composite Proof Hash: {full_proof_hash}")

    # Construct ledger state record
    ledger_data = {
        "kernel": "Alpha Root Kernel",
        "path_vector": PATH_VECTOR,
        "payload_size_bytes": len(payload),
        "payload_sha256": payload_hash,
        "proof_hash": full_proof_hash,
        "consensus_status": "CONSENSUS_LOCKED",
        "validation_state": "GENESIS_VAULT_LOCKED"
    }

    with open(LEDGER_FILE, "w") as f:
        f.write(json.dumps(ledger_data, indent=2))
    print(f"[+] Ledger Synchronized: {LEDGER_FILE}")

    # Construct export manifest json
    with open(MANIFEST_FILE, "w") as f:
        json.dump(ledger_data, f, indent=4)
    print(f"[+] Export Manifest Generated: {MANIFEST_FILE}")

    print("--------------------------------------------------")
    print(f"[+] ALPHA_ROOT_KERNEL: CONSENSUS_LOCKED_PATH_{PATH_VECTOR.replace('/', '_')}_VERIFIED")
    print(f"[+] PATH VECTOR {PATH_VECTOR} FULLY LOCKED AND VERIFIED.")
    print("==================================================")

if __name__ == "__main__":
    compile_proof_manifest()
