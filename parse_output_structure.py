import os
import struct

def parse_output():
    print("==================================================")
    print(" TRANSACTION OUTPUT (VOUT) DETAILED DISSECTION")
    print("==================================================")
    
    file_path = "final_mutant_block.dat"
    with open(file_path, "rb") as f:
        data = f.read()
        
    # Extract remaining payload after header (8), version (4), incount (1), prev_txid (32), vout (4), scriptSig length + scriptSig, sequence (4), outcount (1)
    tx_data = data[8:]
    rest = tx_data[41:]
    
    script_sig_len = rest[0]
    offset = 1 + script_sig_len + 4 # skip scriptSig and sequence (4 bytes)
    out_count = rest[offset]
    offset += 1
    
    print(f"[+] Output Count: {out_count}")
    
    # Parse first output
    out_value_bytes = rest[offset:offset+8]
    out_value = struct.unpack("<Q", out_value_bytes)[0]
    offset += 8
    
    pk_script_len = rest[offset]
    offset += 1
    
    pk_script = rest[offset:offset+pk_script_len]
    
    print(f"\n--- OUTPUT DETAILS ---")
    print(f"    Value (Satoshis) : {out_value}")
    print(f"    Value (BTC)      : {out_value / 100000000:.8f} BTC")
    print(f"    ScriptPubKey Len : {pk_script_len} bytes")
    print(f"    ScriptPubKey Hex : {pk_script.hex()}")
    
    try:
        ascii_out = "".join([chr(b) if 32 <= b <= 126 else '.' for b in pk_script])
        print(f"    ScriptPubKey ASCII: {ascii_out}")
    except Exception:
        pass

if __name__ == "__main__":
    parse_output()
