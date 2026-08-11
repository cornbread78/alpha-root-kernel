import os
import struct

def parse_remaining_payload():
    print("==================================================")
    print(" REMAINING TRANSACTION PAYLOAD DISSECTION")
    print("==================================================")
    
    file_path = "final_mutant_block.dat"
    if not os.path.exists(file_path):
        print(f"[-] Error: {file_path} not found.")
        return
        
    with open(file_path, "rb") as f:
        data = f.read()
        
    # Header: 8 bytes, Version: 4, InCount: 1, PrevTXID: 32, VOUT: 4 -> Total offset = 49 bytes
    tx_data = data[8:]
    rest = tx_data[41:]
    
    print(f"[+] Total Remaining Payload: {len(rest)} bytes")
    print(f"[+] Remaining Hex: {rest.hex()}")
    
    # Parse scriptSig
    script_sig_len = rest[0]
    script_sig = rest[1:1+script_sig_len]
    print(f"\n--- INPUT SCRIPT (SCRIPTSIG) ---")
    print(f"    Length : {script_sig_len} bytes")
    print(f"    Hex    : {script_sig.hex()}")
    try:
        ascii_val = "".join([chr(b) if 32 <= b <= 126 else '.' for b in script_sig])
        print(f"    ASCII  : {ascii_val}")
    except Exception:
        pass
        
    # Sequence and Outputs offset
    offset = 1 + script_sig_len
    sequence = rest[offset:offset+4]
    out_count = rest[offset+4:offset+5]
    
    print(f"\n--- TRANSACTION CONTROLS & OUTPUTS ---")
    print(f"    Sequence   : {sequence.hex()}")
    print(f"    Output Count : {out_count[0]}")
    
    outputs_data = rest[offset+5:]
    print(f"    Outputs Data Length : {len(outputs_data)} bytes")
    print(f"    Outputs Hex  : {outputs_data.hex()}")

if __name__ == "__main__":
    parse_remaining_payload()
