import os
import struct

def parse_mutant_block():
    print("==================================================")
    print(" FINAL MUTANT BLOCK - STRUCTURE PARSER")
    print("==================================================")
    
    file_path = "final_mutant_block.dat"
    if not os.path.exists(file_path):
        print(f"[-] Error: {file_path} not found.")
        return
        
    with open(file_path, "rb") as f:
        data = f.read()
        
    print(f"[+] Parsing {file_path} ({len(data)} bytes total)\n")
    
    # 1. Network Message Header (8 bytes)
    magic = data[0:4]
    size_bytes = data[4:8]
    payload_size = struct.unpack("<I", size_bytes)[0]
    
    print(f"--- NETWORK MESSAGE HEADER ---")
    print(f"    Magic Bytes (Hex) : {magic.hex()} (Expected Mainnet: d9b4bef9)")
    print(f"    Payload Size      : {payload_size} bytes (Little-Endian: {size_bytes.hex()})")
    
    # 2. Transaction Data Payload
    tx_data = data[8:8+payload_size]
    print(f"\n--- TRANSACTION PAYLOAD ({len(tx_data)} bytes) ---")
    
    version = tx_data[0:4]
    in_count = tx_data[4:5]
    prev_txid = tx_data[5:37]
    vout = tx_data[37:41]
    
    print(f"    Version           : {version.hex()} (Little-Endian)")
    print(f"    Input Count       : {in_count[0]}")
    print(f"    Prev TXID (XOR)   : {prev_txid.hex()}")
    print(f"    VOUT Index        : {struct.unpack('<I', vout)[0]}")
    print(f"    Remaining Payload : {len(tx_data) - 41} bytes")
    print(f"    Status            : STRUCTURAL_PARSE_COMPLETE")

if __name__ == "__main__":
    parse_mutant_block()
