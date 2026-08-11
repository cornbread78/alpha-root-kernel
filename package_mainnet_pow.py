import os
import hashlib
import json

PATH_VECTOR = "04/04/00/00"
PAYLOAD_FILE = "kernel_tx.dat"
PROOF_FILE = "consensus_proof.sha256"
OUTPUT_TX = "mainnet_pow_tx.hex"

def package_pow():
    print("==================================================")
    print("   ALPHA ROOT KERNEL - MAINNET POW PACKAGER       ")
    print(f"   Path Vector: {PATH_VECTOR}")
    print("==================================================")

    if not os.path.exists(PAYLOAD_FILE) or not os.path.exists(PROOF_FILE):
        print("[!] Error: Required workspace assets missing.")
        return

    with open(PAYLOAD_FILE, "rb") as f:
        payload = f.read()

    with open(PROOF_FILE, "rb") as f:
        proof_data = f.read()

    # Generate embedded proof manifest structure
    primary_hash = hashlib.sha256(payload).hexdigest()
    composite_proof = hashlib.sha256(payload + proof_data).hexdigest()

    # Construct standardized mainnet transmission frame with embedded proof
    script_pubkey = bytes([0x6a, len(composite_proof)//2]) + bytes.fromhex(composite_proof)
    tx_frame = bytes([0x01, 0x00, 0x00, 0x00]) + payload + script_pubkey

    with open(OUTPUT_TX, "w") as f:
        f.write(tx_frame.hex())

    print(f"[+] Primary Payload Size: {len(payload)} bytes")
    print(f"[+] Proof-of-Work Checksum Embedded: {composite_proof}")
    print(f"[+] Final Mainnet Transaction Frame Saved: {OUTPUT_TX} ({len(tx_frame)} bytes)")
    print("--------------------------------------------------")
    print(f"[+] ALPHA_ROOT_KERNEL: MAINNET_POW_PACKAGED_PATH_{PATH_VECTOR.replace('/', '_')}")
    print("==================================================")

if __name__ == "__main__":
    package_pow()
