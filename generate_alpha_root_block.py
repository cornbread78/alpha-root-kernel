import struct

def build_alpha_root_block():
    print("==================================================")
    print(" ALPHA ROOT - FINAL GENESIS BLOCK STRUCTURE BUILDER")
    print("==================================================")
    
    # 1. Network Message Header (8 bytes)
    magic_bytes = bytes.fromhex("d9b4bef9")
    
    # 2. Transaction Components
    version = bytes.fromhex("01000000")
    in_count = bytes.fromhex("01")
    
    # XOR-masked prev_txid vector [4, 4, 0, 0] * 8 (32 bytes)
    prev_txid = bytes([4, 4, 0, 0]) * 8
    
    # VOUT index (4 bytes)
    vout = bytes.fromhex("00000000")
    
    # scriptSig: length (15 bytes) + ASCII data ("04/04/00/00Wacr")
    script_sig_data = b"04/04/00/00Wacr"
    script_sig_len = bytes([len(script_sig_data)])
    script_sig = script_sig_len + script_sig_data
    
    # Sequence (4 bytes)
    sequence = bytes.fromhex("ffffffff")
    
    # Output Count (1 byte)
    out_count = bytes.fromhex("01")
    
    # Output Value: 50,000,000,000 satoshis (8 bytes, little-endian -> 00f2052a01000000)
    out_value = struct.pack("<Q", 50000000000)
    
    # scriptPubKey: length (65 bytes / 0x41) + P2PK script payload
    pk_script_payload = bytes.fromhex("040000000000000000000000000000000000000000000000000000000000000000ac00000000")
    pk_script_len = bytes([len(pk_script_payload)])
    script_pub_key = pk_script_len + pk_script_payload
    
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
    
    output_filename = "alpha_root_genesis_block.dat"
    with open(output_filename, "wb") as f:
        f.write(final_block)
        
    print(f"[+] Successfully constructed raw block container.")
    print(f"[+] Output File    : {output_filename}")
    print(f"[+] Total Size     : {len(final_block)} bytes")
    print(f"[+] Payload Size   : {len(tx_payload)} bytes")
    print(f"[+] Complete Hex   :")
    print(f"    {final_block.hex()}")

if __name__ == "__main__":
    build_alpha_root_block()
