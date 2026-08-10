import os
import json
import hashlib
import sys

def build_kernel_transaction(utxo, recipient, amount):
    with open('kernel_sync_config.json', 'r') as f:
        config = json.load(f)
        
    raw_data = f"{utxo}|{recipient}|{amount}".encode('utf-8')
    
    if config.get("xor_mask_active"):
        # Applies the 04/04/00/00 structural mask
        mask = bytes.fromhex("04040000")
        payload = bytes([b ^ mask[i % len(mask)] for i, b in enumerate(raw_data)])
    else:
        payload = raw_data
        
    txid = hashlib.sha256(payload).hexdigest()
    
    print(f"KERNEL_TXID: {txid}")
    print(f"RAW_HEX: {payload.hex()}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python3 alpha_tx.py <UTXO_HASH> <RECIPIENT_ADDRESS> <AMOUNT>")
        sys.exit(1)
    build_kernel_transaction(sys.argv[1], sys.argv[2], sys.argv[3])
