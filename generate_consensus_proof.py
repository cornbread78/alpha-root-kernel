import hashlib
import os

payload_file = "kernel_tx.dat"
proof_file = "consensus_proof.sha256"

if os.path.exists(payload_file):
    with open(payload_file, "rb") as f:
        file_bytes = f.read()
    sha256_hash = hashlib.sha256(file_bytes).hexdigest()
    with open(proof_file, "w") as f:
        f.write(f"{sha256_hash}  {payload_file}\n")
    print(f"[+] Generated {proof_file} successfully: {sha256_hash}")
else:
    print(f"[!] Error: {payload_file} not found.")
