import struct

def analyze_payload():
    # Decoded hex from your workspace payload
    payload_hex = "01000000010000000000000000000000000000000000000000000000000000000000000000000000000f30342f30342f30302f303057616372ffffffff0100f2052a0100000041040000000000000000000000000000000000000000000000000000000000000000ac00000000"
    raw_bytes = bytes.fromhex(payload_hex)
    
    print(f"[*] Total Payload Size: {len(raw_bytes)} bytes")
    print(f"[*] Version: {raw_bytes[0:4][::-1].hex()}")
    print(f"[*] Input Count: {raw_bytes[4]}")
    print(f"[*] Previous TxID (Input 0): {raw_bytes[5:37].hex()}")
    
    if raw_bytes[5:37] == b"\x00" * 32:
        print("[!] NOTICE: Input 0 uses a zero-hash outpoint (Coinbase signature format).")
        print("[!] Bitcoin Core rejects standalone coinbase transactions via sendrawtransaction.")

if __name__ == "__main__":
    analyze_payload()
