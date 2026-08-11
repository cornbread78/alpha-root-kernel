import os
import hashlib

def decode_payload():
    payload_file = "kernel_tx.dat"
    if not os.path.exists(payload_file):
        print(f"[!] Error: {payload_file} not found in workspace.")
        return

    with open(payload_file, "rb") as f:
        raw_data = f.read()

    # Apply the path vector XOR mask [0x04, 0x04, 0x00, 0x00]
    xor_mask = bytes([0x04, 0x04, 0x00, 0x00])
    unmasked = bytearray(raw_data)
    for i in range(len(unmasked)):
        unmasked[i] ^= xor_mask[i % len(xor_mask)]

    tx_hex = unmasked.hex()
    single_hash = hashlib.sha256(bytes(unmasked)).hexdigest()
    double_sha = hashlib.sha256(hashlib.sha256(bytes(unmasked)).digest()).hexdigest()

    print("==================================================")
    print(" ALPHA ROOT KERNEL - MAINNET PAYLOAD UNPACKER     ")
    print(" Path Vector: 04/04/00/00                          ")
    print("==================================================")
    print(f"[+] Processed Payload Size: {len(unmasked)} bytes")
    print(f"[+] Unmasked Hex Stream:\n{tx_hex}")
    print("--------------------------------------------------")
    print(f"[+] SHA-256 Proof Hash: {single_hash}")
    print(f"[+] Double SHA-256 (TXID): {double_sha}")
    print("==================================================")

    output_filename = "unmasked_mainnet_payload.hex"
    with open(output_filename, "w") as f:
        f.write(tx_hex)
    print(f"[+] Clean raw hex successfully exported to '{output_filename}'")

if __name__ == "__main__":
    decode_payload()
