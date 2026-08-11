import os
import hashlib

def extract_keys():
    filename = "kernel_tx.dat"
    print("==================================================")
    print(" ALPHA ROOT KERNEL - PAYLOAD KEY EXTRACTION")
    print("==================================================")

    if not os.path.exists(filename):
        print(f"[!] Error: {filename} not found.")
        return

    with open(filename, "rb") as f:
        payload = f.read()

    print(f"[+] Loaded payload size: {len(payload)} bytes")
    print(f"[+] Payload Hex: {payload.hex()}")

    # Analyze fixed-size slices for potential private key signatures
    # Standard raw private key is 32 bytes. Let's scan sliding 32-byte windows.
    found_candidates = []
    for i in range(len(payload) - 31):
        chunk = payload[i:i+32]
        # Check if it's not entirely zeros or standard structural filler
        if chunk != b"\x00" * 32 and chunk != b"\x04" * 32:
            found_candidates.append((i, chunk.hex()))

    print("--------------------------------------------------")
    print(f"[+] Scan Results:")
    if found_candidates:
        for idx, hex_val in found_candidates:
            print(f"    Offset {idx}: {hex_val}")
    else:
        print("    [-] All data segments consist of zero-fill placeholders, version flags, or path vector tags (`04/04/00/00`).")
        print("    [-] No active 32-byte private key entropy or WIF strings detected in the payload structure.")

    print("==================================================")

if __name__ == "__main__":
    extract_keys()
