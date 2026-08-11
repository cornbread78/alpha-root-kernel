import os

def process_framed_block():
    print("==================================================")
    print(" FRAMED BLOCK - XOR MASS INJECTION")
    print("==================================================")
    
    framed_path = "framed_kernel_block.dat"
    if not os.path.exists(framed_path):
        print("[-] Error: framed_kernel_block.dat not found.")
        return
        
    with open(framed_path, "rb") as f:
        data = f.read()
        
    print(f"[+] Loaded {framed_path}: {len(data)} bytes")
    
    # Separate network message header (8 bytes: 4 magic + 4 size) from transaction data
    header = data[:8]
    tx_data = data[8:]
    
    # Preserve transaction header (Version: 4 bytes, Input Count: 1 byte)
    version_incount = tx_data[:5]
    
    # The 32-byte prev_txid slot is currently zero-filled (indices 5 to 37)
    # Injecting the XOR mask mass pattern [4, 4, 0, 0] across the 32 bytes
    xor_pattern = bytes([4, 4, 0, 0]) * 8
    
    # Load block XOR modifier if available
    xor_key_path = "blocks/xor.dat"
    if os.path.exists(xor_key_path):
        with open(xor_key_path, "rb") as f:
            block_xor = f.read()
        print(f"[+] Loaded block XOR modifier: {block_xor.hex()}")
    
    rest_of_tx = tx_data[37:]
    
    # Reassemble the transaction with the injected XOR mass
    modified_tx = version_incount + xor_pattern + rest_of_tx
    final_payload = header + modified_tx
    
    output_file = "final_mutant_block.dat"
    with open(output_file, "wb") as f:
        f.write(final_payload)
        
    print(f"[+] Successfully generated {output_file} ({len(final_payload)} bytes)")
    print(f"[+] Final Hex Preview: {final_payload.hex()[:64]}...")

if __name__ == "__main__":
    process_framed_block()
