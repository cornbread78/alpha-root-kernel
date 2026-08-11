import os
import hashlib

PATH_VECTOR = "04/04/00/00"
PAYLOAD_FILE = "kernel_tx.dat"
XOR_MASK = bytes([0x04, 0x04, 0x00, 0x00])

def finalize_payload():
    print("==================================================")
    print("   ALPHA ROOT KERNEL - FINAL MAINNET PACKAGER     ")
    print(f"   Path Vector: {PATH_VECTOR}")
    print("==================================================")

    if not os.path.exists(PAYLOAD_FILE):
        print(f"[!] Error: {PAYLOAD_FILE} missing.")
        return

    with open(PAYLOAD_FILE, "rb") as f:
        raw_data = f.read()

    unmasked_bytes = bytearray()
    for i, b in enumerate(raw_data):
        mask_byte = XOR_MASK[i % len(XOR_MASK)]
        unmasked_bytes.append(b ^ mask_byte)

    # Format final transmission frame container
    final_frame = bytes([0x6a, len(unmasked_bytes)]) + bytes(unmasked_bytes)
    print(f"[+] Unmasked payload length: {len(unmasked_bytes)} bytes")
    print(f"[+] Final Frame Length: {len(final_frame)} bytes")
    print(f"[+] Final Hex Stream Preview (First 64 chars):")
    print(final_frame[:32].hex())
    
    output_file = "final_mainnet_frame.hex"
    with open(output_file, "w") as f:
        f.write(final_frame.hex())
        
    print(f"[+] Saved final transmission frame to {output_file}")
    print("--------------------------------------------------")
    print(f"[+] ALPHA_ROOT_KERNEL: PATH_{PATH_VECTOR.replace('/', '_')}_FINALIZED")
    print("==================================================")

if __name__ == "__main__":
    finalize_payload()
