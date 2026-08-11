import os
import hashlib
import json

PAYLOAD_FILE = "kernel_tx.dat"
XOR_MASK = [4, 4, 0, 0]
REPORT_FILE = "kernel_inspection_report.json"

def main():
    print("==================================================")
    print("   ALPHA ROOT KERNEL - WORKSPACE DATA INSPECTION  ")
    print("   Path Vector: 04/04/00/00                       ")
    print("==================================================\n")

    if not os.path.exists(PAYLOAD_FILE):
        print(f"[!] Error: {PAYLOAD_FILE} not found in workspace.")
        return

    with open(PAYLOAD_FILE, "rb") as f:
        raw_data = f.read()

    print(f"[+] Loaded {PAYLOAD_FILE}: {len(raw_data)} bytes")

    # Apply XOR mask transformation
    unmasked_data = bytearray(
        b ^ XOR_MASK[i % len(XOR_MASK)] for i, b in enumerate(raw_data)
    )

    raw_hex = raw_data.hex()
    unmasked_hex = unmasked_data.hex()

    # Compute SHA-256 cryptographic hashes
    raw_hash = hashlib.sha256(raw_data).hexdigest()
    masked_hash = hashlib.sha256(unmasked_data).hexdigest()

    print(f"[+] Raw SHA-256 Hash:   {raw_hash}")
    print(f"[+] Masked SHA-256 Hash:  {masked_hash}")

    report = {
        "path_vector": "04/04/00/00",
        "payload_file": PAYLOAD_FILE,
        "size_bytes": len(raw_data),
        "xor_mask": XOR_MASK,
        "raw_sha256": raw_hash,
        "masked_sha256": masked_hash,
        "raw_hex_preview": raw_hex[:64],
        "unmasked_hex_preview": unmasked_hex[:64]
    }

    with open(REPORT_FILE, "w") as f:
        json.dump(report, f, indent=4)

    print(f"[+] Inspection report successfully written to {REPORT_FILE}")
    print("[+] WORKSPACE DATA INSPECTION COMMITTED.")

if __name__ == "__main__":
    main()
