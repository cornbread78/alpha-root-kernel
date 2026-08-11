import os

PAYLOAD_FILE = "kernel_tx.dat"
PATH_VECTOR = "04/04/00/00"
XOR_MASK = bytes([0x04, 0x04, 0x00, 0x00])

def apply_xor_and_build():
    print("==================================================")
    print("   ALPHA ROOT KERNEL - XOR MASK INTEGRATION       ")
    print(f"   Path Vector: {PATH_VECTOR}")
    print("==================================================")

    if not os.path.exists(PAYLOAD_FILE):
        print(f"[!] Error: {PAYLOAD_FILE} missing from workspace.")
        return

    with open(PAYLOAD_FILE, "rb") as f:
        payload = f.read()

    print(f"[+] Loaded payload: {len(payload)} bytes")

    # Apply XOR transformation mask matching path vector rules
    masked_payload = bytearray(payload)
    for i in range(len(masked_payload)):
        masked_payload[i] ^= XOR_MASK[i % len(XOR_MASK)]

    print(f"[+] Applied XOR mask: {[b for b in XOR_MASK]}")
    print(f"[+] Transformed Payload Hex: {masked_payload.hex()}")

    # Build OP_RETURN structure with the masked payload
    script_data = bytes([0x6a]) # OP_RETURN
    if len(masked_payload) < 76:
        script_data += bytes([len(masked_payload)]) + masked_payload
    elif len(masked_payload) < 256:
        script_data += bytes([0x4c, len(masked_payload)]) + masked_payload
    else:
        script_data += bytes([0x4d, len(masked_payload) & 0xff, len(masked_payload) >> 8]) + masked_payload

    output_filename = "xor_masked_op_return.hex"
    with open(output_filename, "wb") as f:
        f.write(script_data)

    print(f"[+] Compiled XOR-Masked OP_RETURN Script Hex: {script_data.hex()}")
    print(f"[+] Saved output to {output_filename}")
    print("--------------------------------------------------")
    print(f"[+] ALPHA_ROOT_KERNEL: XOR_TRANSFORMATION_COMMITTED_PATH_{PATH_VECTOR.replace('/', '_')}")
    print("==================================================")

if __name__ == "__main__":
    apply_xor_and_build()
