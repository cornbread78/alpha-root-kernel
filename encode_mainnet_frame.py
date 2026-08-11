import os
import hashlib

TARGET_PATH = "04/04/00/00"
PAYLOAD_FILE = "kernel_tx.dat"
OUTPUT_FILE = "final_mainnet_frame.hex"

def encode_kernel_frame():
    print("==================================================")
    print("   ALPHA ROOT KERNEL - MAINNET ENCODER            ")
    print(f"   Path Vector: {TARGET_PATH}")
    print("==================================================")

    if not os.path.exists(PAYLOAD_FILE):
        print(f"[!] Error: {PAYLOAD_FILE} not found in current directory.")
        return

    with open(PAYLOAD_FILE, "rb") as f:
        kernel_data = f.read()

    print(f"[+] Loaded kernel data: {len(kernel_data)} bytes")

    # Compute SHA-256 hash for structural verification
    sha256_hash = hashlib.sha256(kernel_data).hexdigest()
    print(f"[+] Kernel SHA-256 Hash: {sha256_hash}")

    # Construct the transmission frame sequence
    path_bytes = TARGET_PATH.encode("utf-8")
    frame_payload = path_bytes + b":" + kernel_data + b":" + bytes.fromhex(sha256_hash[:32])

    with open(OUTPUT_FILE, "wb") as out_f:
        out_f.write(frame_payload)

    print(f"[+] Successfully generated mainnet frame: {OUTPUT_FILE}")
    print(f"[+] Frame size: {len(frame_payload)} bytes")
    print(f"[+] Hex preview: {frame_payload.hex()[:64]}...")
    print("[+] ENCODING COMPLETE - READY FOR DISPATCH.")

if __name__ == "__main__":
    encode_kernel_frame()
