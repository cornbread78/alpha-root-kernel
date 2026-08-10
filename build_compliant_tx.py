import os
import struct

def build_transaction():
    print("==================================================")
    print("   ALPHA ROOT KERNEL - PROTOCOL TRANSACTION BUILDER")
    print("   Path Vector: 04/04/00/00                       ")
    print("==================================================")

    payload_file = "kernel_tx.dat"
    if not os.path.exists(payload_file):
        print(f"[!] Critical Error: {payload_file} not found.")
        return

    with open(payload_file, "rb") as f:
        payload = f.read()

    print(f"[+] Loaded workspace payload: {len(payload)} bytes")

    # 1. Transaction Version (4 bytes, little-endian)
    tx_version = struct.pack("<I", 2)

    # 2. Input Count (VarInt: 1 input required by network rules)
    tx_in_count = b'\x01'

    # 3. Previous Output Hash (32 bytes of zeros as a placeholder for a UTXO)
    prev_out_hash = b'\x00' * 32

    # 4. Previous Output Index (4 bytes, little-endian)
    prev_out_index = struct.pack("<I", 0)

    # 5. ScriptSig Length and ScriptSig (Empty for unsigned template, 1 byte length = 0x00)
    script_sig_len = b'\x00'
    script_sig = b''

    # 6. Sequence (4 bytes, little-endian, usually 0xffffffff)
    sequence = struct.pack("<I", 0xffffffff)

    # Combine input components
    tx_in = prev_out_hash + prev_out_index + script_sig_len + script_sig + sequence

    # 7. Output Count (VarInt: 2 outputs -> 1 for OP_RETURN data carrier, 1 for value/change)
    tx_out_count = b'\x02'

    # 8. Output 0: OP_RETURN Data Carrier
    # OP_RETURN (0x6a) + pushdata length + payload
    if len(payload) <= 75:
        op_return_script = bytes([0x6a, len(payload)]) + payload
    elif len(payload) <= 255:
        op_return_script = bytes([0x6a, 0x4c, len(payload)]) + payload
    else:
        truncated = payload[:80]
        op_return_script = bytes([0x6a, len(truncated)]) + truncated

    value_zero = struct.pack("<Q", 0) # 0 satoshis for OP_RETURN
    script_pubkey_len = struct.pack("B", len(op_return_script))
    output_op_return = value_zero + script_pubkey_len + op_return_script

    # 9. Output 1: Standard P2PKH or P2WPKH placeholder for funds/fee handling
    # Standard dust output stub
    value_change = struct.pack("<Q", 546) 
    # Dummy standard scriptPubKey (e.g., P2PKH 25 bytes stub)
    dummy_pubkey_script = b'\x76\xa9\x14' + (b'\x00' * 20) + b'\x88\ac'
    output_change_len = struct.pack("B", len(dummy_pubkey_script))
    output_change = value_change + output_change_len + dummy_pubkey_script

    # 10. LockTime (4 bytes, little-endian)
    lock_time = struct.pack("<I", 0)

    # Assemble complete raw transaction bytes
    raw_tx = tx_version + tx_in_count + tx_in + tx_out_count + output_op_return + output_change + lock_time

    print(f"[+] Protocol-compliant Raw Transaction Hex:")
    print(raw_tx.hex())
    
    # Save to file for inspection
    with open("compliant_tx.hex", "w") as f:
        f.write(raw_tx.hex())
    print(f"[+] Saved structured transaction hex to compliant_tx.hex ({len(raw_tx)} bytes total)")

if __name__ == "__main__":
    build_transaction()
