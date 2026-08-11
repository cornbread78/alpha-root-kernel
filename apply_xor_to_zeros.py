import os

def apply_xor():
    filename = "kernel_tx.dat"
    if not os.path.exists(filename):
        print("[!] kernel_tx.dat not found.")
        return

    with open(filename, "rb") as f:
        payload = f.read()

    # XOR mask: [4, 4, 0, 0] targeting zero-filled sectors and payload layout
    xor_mask = bytes([4, 4, 0, 0])
    
    masked_payload = bytearray(
        b ^ xor_mask[i % len(xor_mask)] for i, b in enumerate(payload)
    )

    output_filename = "xor_masked_kernel_tx.dat"
    with open(output_filename, "wb") as f:
        f.write(masked_payload)

    print("==================================================")
    print(" ALPHA ROOT KERNEL - XOR MASK APPLIED TO ZEROS")
    print("==================================================")
    print(f"[+] Input size: {len(payload)} bytes")
    print(f"[+] Applied Mask: {list(xor_mask)}")
    print(f"[+] Masked Payload Hex: {masked_payload.hex()}")
    print(f"[+] Saved to: {output_filename}")
    print("==================================================")

if __name__ == "__main__":
    apply_xor()
