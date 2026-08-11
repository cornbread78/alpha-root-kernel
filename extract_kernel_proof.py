import os
import hashlib

def extract_proof():
    filename = "kernel_tx.dat"
    print("==================================================")
    print(" ALPHA ROOT KERNEL - PROOF EXTRACTION PIPELINE")
    print(" Path Vector: 04/04/00/00")
    print("==================================================")

    if not os.path.exists(filename):
        print(f"[!] Error: {filename} missing from local workspace.")
        return

    with open(filename, "rb") as f:
        raw_bytes = f.read()

    xor_mask = bytes([4, 4, 0, 0])
    decoded_stream = bytearray(b ^ xor_mask[i % len(xor_mask)] for i, b in enumerate(raw_bytes))
    
    proof_hash = hashlib.sha256(decoded_stream).hexdigest()
    proof_segment = decoded_stream[:32]

    print(f"[+] Loaded workspace payload: {len(raw_bytes)} bytes")
    print(f"[+] Extracted Proof Segment Hex: {proof_segment.hex()}")
    print(f"[+] Computed Workspace Proof Hash: {proof_hash}")
    print("==================================================")
    print("[+] STATUS: PROOF VECTOR ISOLATED AND PARSED")
    print("==================================================")

if __name__ == "__main__":
    extract_proof()
