import hashlib
import json
import os

def build_op_return_frame():
    print("==================================================")
    print(" ALPHA ROOT KERNEL - OP_RETURN TRANSACTION BUILDER")
    print("==================================================")

    # Load the target kernel payload
    payload_file = "xor_masked_kernel_tx.dat"
    if not os.path.exists(payload_file):
        payload_file = "kernel_tx.dat"

    if not os.path.exists(payload_file):
        print(f"[!] Error: No payload file found to anchor.")
        return

    with open(payload_file, "rb") as f:
        payload_data = f.read()

    # Generate the 32-byte SHA-256 hash for standard OP_RETURN data anchoring
    payload_hash = hashlib.sha256(payload_data).digest()
    
    print(f"[+] Source Payload: {payload_file} ({len(payload_data)} bytes)")
    print(f"[+] 32-Byte Hash for Anchoring: {payload_hash.hex()}")

    # Construct standard Bitcoin transaction template components
    # Version (4 bytes) + Input Count + Dummy Input (UTXO placeholder) + Output Count + OP_RETURN Output + Locktime
    # OP_RETURN script format: OP_RETURN (0x6a) + Push Data Length (0x20 = 32 bytes) + 32-byte Hash
    op_return_script = b"\x6a\x20" + payload_hash
    
    # Bundle into a structured JSON transmission template for node ingestion
    tx_template = {
        "version": 2,
        "marker": 0,
        "flag": 1,
        "inputs": [
            {
                "txid": "REPLACE_WITH_REAL_FUNDED_UTXO_TXID",
                "vout": 0,
                "scriptSig": "",
                "sequence": 4294967295
            }
        ],
        "outputs": [
            {
                "value": 0,
                "scriptPubKey": op_return_script.hex()
            }
        ],
        "locktime": 0
    }

    output_filename = "mainnet_op_return_template.json"
    with open(output_filename, "w") as tf:
        json.dump(tx_template, tf, indent=4)

    print(f"[+] Standard OP_RETURN Transaction Template Saved: {output_filename}")
    print("[+] STATUS: TRANSACTION STRUCTURE READY FOR UTXO LINKING & SIGNING")
    print("==================================================")

if __name__ == "__main__":
    build_op_return_frame()
