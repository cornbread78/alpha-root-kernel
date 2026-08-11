import struct

def build_op_return_block():
    print("==================================================")
    print(" OP_RETURN REVOLVING DOOR CONTAINER BUILDER")
    print("==================================================")
    
    derivation_path = "04/04/00/00"
    opening = "Open Sesame"
    core_entity = "Ali Baba"
    closure = "Close Sesame"
    
    full_phrase = f"{derivation_path} {opening} {core_entity} and {closure}"
    phrase_bytes = full_phrase.encode('utf-8')
    
    print(f"[+] Target Phrase : {full_phrase}")
    print(f"[+] Phrase Hex    : {phrase_bytes.hex()} ({len(phrase_bytes)} bytes)")
    
    # 1. Network Message Header (8 bytes)
    magic_bytes = bytes.fromhex("d9b4bef9")
    
    # 2. Transaction Components
    version = bytes.fromhex("01000000")
    in_count = bytes.fromhex("01")
    
    # prev_txid slot (32 bytes)
    prev_txid = phrase_bytes.ljust(32, b'\x00')[:32]
    
    # VOUT index (4 bytes)
    vout = bytes.fromhex("00000000")
    
    # scriptSig: Push-only clean data vector (1 byte length + 0x00)
    script_sig = bytes.fromhex("0100")
    
    # Sequence (4 bytes)
    sequence = bytes.fromhex("ffffffff")
    
    # Output Count (1 byte)
    out_count = bytes.fromhex("01")
    
    # Output Value: 0 satoshis for OP_RETURN payload output (8 bytes, little-endian)
    out_value = struct.pack("<Q", 0)
    
    # scriptPubKey: Standard OP_RETURN output carrying the full phrase payload (0x6a + push_len + phrase_bytes)
    op_return_prefix = bytes([0x6a, len(phrase_bytes)])
    script_pub_key_payload = op_return_prefix + phrase_bytes
    script_pub_key = bytes([len(script_pub_key_payload)]) + script_pub_key_payload
    
    # Locktime (4 bytes)
    locktime = bytes.fromhex("00000000")
    
    # Assemble complete raw transaction payload
    tx_payload = (
        version + 
        in_count + 
        prev_txid + 
        vout + 
        script_sig + 
        sequence + 
        out_count + 
        out_value + 
        script_pub_key + 
        locktime
    )
    
    # Calculate payload length (4 bytes, little-endian)
    payload_size = struct.pack("<I", len(tx_payload))
    
    # Final framed block container
    final_block = magic_bytes + payload_size + tx_payload
    
    output_filename = "op_return_revolving_block.dat"
    with open(output_filename, "wb") as f:
        f.write(final_block)
        
    print(f"[+] Successfully generated OP_RETURN block container.")
    print(f"[+] Output File    : {output_filename}")
    print(f"[+] Total Size     : {len(final_block)} bytes")
    print(f"[+] Payload Size   : {len(tx_payload)} bytes")
    print(f"[+] Complete Hex   :")
    print(f"    {final_block.hex()}")

if __name__ == "__main__":
    build_op_return_block()
