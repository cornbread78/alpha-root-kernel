import hashlib

# Verified Workspace Proof-of-Work Hash
POW_HASH = "78a5d9fc5707af9eb253321744eae34a749f0ce3207fb5884cf560d2800d2452"
PATH_VECTOR = "04/04/00/00"

def build_compliant_transaction():
    print("==================================================")
    print("   ALPHA ROOT KERNEL - MAINNET OP_RETURN BUILDER  ")
    print(f"   Path Vector: {PATH_VECTOR}")
    print("==================================================")

    # 1. Transaction Version (4 bytes, little-endian)
    version = bytes.fromhex("01000000")
    
    # 2. Input Count (VarInt: 1 input slot)
    tx_in_count = bytes.fromhex("01")
    
    # 3. Input Source (Placeholder for UTXO reference: 32-byte txid + 4-byte index + scriptSig + sequence)
    prev_tx_hash = bytes.fromhex("0000000000000000000000000000000000000000000000000000000000000000")
    prev_index = bytes.fromhex("ffffffff")
    script_sig_len = bytes.fromhex("00")
    sequence = bytes.fromhex("ffffffff")
    tx_in = prev_tx_hash + prev_index + script_sig_len + sequence

    # 4. Output Count (VarInt: 1 output slot)
    tx_out_count = bytes.fromhex("01")
    
    # 5. Output Value: 0 satoshis (8 bytes, little-endian)
    value = bytes.fromhex("0000000000000000")
    
    # 6. OP_RETURN Script Construction: OP_RETURN (0x6a) + Push 32 bytes (0x20) + Hash payload
    hash_bytes = bytes.fromhex(POW_HASH)
    script_pub_key = bytes([0x6a, 0x20]) + hash_bytes
    script_pub_key_len = bytes([len(script_pub_key)])
    
    tx_out = value + script_pub_key_len + script_pub_key

    # 7. Locktime (4 bytes, little-endian)
    locktime = bytes.fromhex("00000000")

    # Assemble raw transaction frame
    raw_tx = version + tx_in_count + tx_in + tx_out_count + tx_out + locktime
    
    output_filename = "mainnet_op_return_tx.hex"
    with open(output_filename, "w") as f:
        f.write(raw_tx.hex())

    print(f"[+] Embedded POW Hash: {POW_HASH}")
    print(f"[+] Compliant Transaction Frame Generated: {output_filename}")
    print(f"[+] Total Serialized Size: {len(raw_tx)} bytes")
    print("--------------------------------------------------")
    print(f"[+] ALPHA_ROOT_KERNEL: OP_RETURN_STRUCTURE_LOCKED_PATH_{PATH_VECTOR.replace('/', '_')}")
    print("==================================================")

if __name__ == "__main__":
    build_compliant_transaction()
