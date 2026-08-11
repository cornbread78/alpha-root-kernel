import struct

def create_op_return_tx(data_payload: bytes):
    # Standard Bitcoin transaction version (4 bytes)
    version = struct.pack("<I", 1)
    
    # Placeholder for input structure
    dummy_prev_tx = b"\x00" * 32
    dummy_vout = struct.pack("<I", 0)
    script_sig = b""
    script_sig_len = bytes([len(script_sig)])
    sequence = struct.pack("<I", 0xffffffff)
    
    tx_in = dummy_prev_tx + dummy_vout + script_sig_len + script_sig + sequence
    tx_in_count = bytes([1])

    if len(data_payload) > 80:
        raise ValueError("Payload exceeds standard 80-byte OP_RETURN limit.")
    
    op_return_script = bytes([0x6a, len(data_payload)]) + data_payload
    script_pubkey_len = bytes([len(op_return_script)])
    
    value = struct.pack("<Q", 0)
    tx_out = value + script_pubkey_len + op_return_script
    tx_out_count = bytes([1])

    locktime = struct.pack("<I", 0)
    raw_tx = version + tx_in_count + tx_in + tx_out_count + tx_out + locktime
    return raw_tx.hex()

if __name__ == "__main__":
    message = b"come home"
    tx_hex = create_op_return_tx(message)
    print("==================================================")
    print("       STANDARD OP_RETURN TRANSACTION BUILDER     ")
    print("==================================================")
    print(f"[+] Payload: {message}")
    print(f"[+] Generated Raw Tx Hex:\n{tx_hex}")
