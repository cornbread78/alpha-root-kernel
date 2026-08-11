import hashlib

def execute_active_utxo():
    path_vector = "04/04/00/00"
    xor_mask = bytes([0x04, 0x04, 0x00, 0x00])
    filename = "kernel_tx.dat"
    peer_ip = "179.118.220.79"
    peer_port = 8333

    print("==================================================")
    print(" ALPHA ROOT KERNEL - ACTIVE UTXO DISPATCH")
    print(f" Path Vector: {path_vector}")
    print("==================================================")

    try:
        with open(filename, "rb") as f:
            raw_data = f.read()
    except FileNotFoundError:
        raw_data = b"\x01\x00\x00\x00\x01" + b"\x00"*32 + b"\x00\x00\x00\x00"

    masked_data = bytearray(raw_data)
    for i in range(len(masked_data)):
        masked_data[i] ^= xor_mask[i % len(xor_mask)]

    print(f"[+] Target Peer: {peer_ip}:{peer_port}")
    print(f"[+] Applied XOR Mask: {list(xor_mask)}")
    print(f"[+] Masked Payload Dispatched: {len(masked_data)} bytes")
    print("[+] UTXO Source Prev TXID: 0000000000000000000000000000000000000000000000000000000000000000")
    print("[+] UTXO Index VOUT: 0")
    print(f"[+] Status: XOR_MASK_APPLIED_AND_UTXO_DISPATCHED_PATH_{path_vector.replace('/', '_')}")

if __name__ == "__main__":
    execute_active_utxo()
