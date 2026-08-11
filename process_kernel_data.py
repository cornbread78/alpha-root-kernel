import os
import hashlib

def process_kernel_data():
    filename = "kernel_tx.dat"
    path_vector = "04/04/00/00"
    
    if not os.path.exists(filename):
        print(f"[!] Error: {filename} not found in workspace.")
        return

    with open(filename, "rb") as f:
        raw_data = f.read()

    xor_mask = bytes([4, 4, 0, 0])
    processed_data = bytearray(b ^ xor_mask[i % len(xor_mask)] for i, b in enumerate(raw_data))
    
    print("==================================================")
    print(" ALPHA ROOT KERNEL - DATA PROCESSING PIPELINE")
    print(f" Path Vector: {path_vector}")
    print("==================================================")
    print(f"[+] Loaded Bytes: {len(raw_data)}")
    print(f"[+] Applied XOR Mask: {[4, 4, 0, 0]}")
    print(f"[+] Processed Payload Hex: {processed_data.hex()}")
    print(f"[+] SHA-256 Checksum: {hashlib.sha256(processed_data).hexdigest()}")
    print("==================================================s")

if __name__ == "__main__":
    process_kernel_data()
