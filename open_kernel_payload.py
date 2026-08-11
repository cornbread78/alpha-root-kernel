import os
import hashlib

PATH_VECTOR = "04/04/00/00"
PAYLOAD_FILE = "kernel_tx.dat"
XOR_MASK = bytes([0x04, 0x04, 0x00, 0x00])

def open_kernel():
    print("==================================================")
    print("   ALPHA ROOT KERNEL - PAYLOAD EXTRACTION ENGINE  ")
    print(f"   Path Vector: {PATH_VECTOR}")
    print("==================================================")

    if not os.path.exists(PAYLOAD_FILE):
        print(f"[!] Error: {PAYLOAD_FILE} not found in workspace.")
        return

    with open(PAYLOAD_FILE, "rb") as f:
        raw_data = f.read()

    print(f"[+] Loaded raw payload: {len(raw_data)} bytes")

    # Apply path vector XOR mask unmasking sequence
    unmasked_bytes = bytearray()
    for i, b in enumerate(raw_data):
        mask_byte = XOR_MASK[i % len(XOR_MASK)]
        unmasked_bytes.append(b ^ mask_byte)

    payload_hash = hashlib.sha256(raw_data).hexdigest()
    unmasked_hash = hashlib.sha256(unmasked_bytes).hexdigest()

    print(f"[+] Primary Payload Hash: {payload_hash}")
    print(f"[+] Unmasked Kernel Hash: {unmasked_hash}")
    
    print("--------------------------------------------------")
    print("           EXTRACTED NUMERIC DATA VECTORS         ")
    print("--------------------------------------------------")
    # Display first 32 bytes as structured numeric integers
    numeric_sample = list(unmasked_bytes[:32])
    print(f"[+] Numeric Array Header (First 32 bytes):")
    print(numeric_sample)
    print(f"[+] Hex Representation (First 64 chars):")
    print(unmasked_bytes[:32].hex())
    print("==================================================")
    print(f"[+] ALPHA_ROOT_KERNEL: PATH_{PATH_VECTOR.replace('/', '_')}_OPENED")

if __name__ == "__main__":
    open_kernel()
