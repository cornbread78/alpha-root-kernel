import os

def build_transaction():
    print("==================================================")
    print(" ALPHA ROOT KERNEL - OP_RETURN BUILDER")
    print(" Path Vector: 04/04/00/00")
    print("==================================================")

    path_vector = "04/04/00/00"
    xor_mask = [0x04, 0x04, 0x00, 0x00]
    
    # Load kernel payload or default to 'come home'
    if os.path.exists("kernel_tx.dat"):
        with open("kernel_tx.dat", "rb") as f:
            payload = f.read()
        print(f"[+] Loaded kernel_tx.dat: {len(payload)} bytes")
    else:
        payload = b"come home"
        print(f"[+] Using default payload message: 'come home'")

    # Apply XOR mask transformation matching path vector rules
    masked_payload = bytearray(payload)
    for i in range(len(masked_payload)):
        masked_payload[i] ^= xor_mask[i % len(xor_mask)]

    # Construct OP_RETURN script container (OP_RETURN = 0x6a)
    data_len = len(masked_payload)
    if data_len < 75:
        push_opcode = bytes([data_len])
    elif data_len < 256:
        push_opcode = b'\x4c' + bytes([data_len])
    else:
        push_opcode = b'\x4d' + data_len.to_bytes(2, 'little')

    op_return_script = b'\x6a' + push_opcode + bytes(masked_payload)
    script_hex = op_return_script.hex()

    print(f"[+] Transformed Payload Hex: {masked_payload.hex()}")
    print(f"[+] Compiled OP_RETURN Script Hex: {script_hex}")

    # Output to file for node processing
    with open("op_return_payload.hex", "w") as f:
        f.write(script_hex)
    print("[+] Saved OP_RETURN output to op_return_payload.hex")

if __name__ == "__main__":
    build_transaction()
