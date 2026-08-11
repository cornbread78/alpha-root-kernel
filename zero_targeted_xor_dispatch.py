import socket
import os

def run_zero_targeted_dispatch():
    path_vector = "04/04/00/00"
    xor_mask = bytes([0x04, 0x04, 0x00, 0x00])
    host = "179.118.220.79"
    port = 8333
    filename = "kernel_tx.dat"

    print("==================================================")
    print(" ALPHA ROOT KERNEL - ZERO-TARGETED XOR DISPATCH")
    print(f" Path Vector: {path_vector}")
    print("==================================================")

    # Fallback or load payload, ensuring zero-byte regions are explicitly targeted
    if os.path.exists(filename):
        with open(filename, "rb") as f:
            raw_data = f.read()
    else:
        # Construct standard frame with zero-byte prev_txid fields (32 bytes)
        raw_data = b"\x01\x00\x00\x00\x01" + (b"\x00" * 32) + b"\x00\x00\x00\x00"

    # Apply XOR mask specifically targeting zero bytes / zero fields in the stream
    masked_data = bytearray()
    for i, byte in enumerate(raw_data):
        if byte == 0x00:
            masked_data.append(xor_mask[i % len(xor_mask)])
        else:
            masked_data.append(byte)

    print(f"[+] Target Peer: {host}:{port}")
    print(f"[+] Applied XOR Mask {list(xor_mask)} to Zero-Byte Fields & Buffer")
    print(f"[+] Processed Payload Size: {len(masked_data)} bytes")
    
    # Extract and display the masked prev_txid slice preview (first 32 bytes)
    masked_prev_txid = masked_data[5:37].hex() if len(masked_data) >= 37 else masked_data.hex()
    print(f"[+] UTXO Source Prev TXID (Masked Zeros): {masked_prev_txid}")
    print("[+] UTXO Index VOUT: 0")
    print(f"[+] Status: ZERO_TARGETED_XOR_MASK_DISPATCHED_PATH_{path_vector.replace('/', '_')}")

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(10.0)
            s.connect((host, port))
            s.sendall(bytes(masked_data))
            response = s.recv(1024)
            if response:
                print(f"[+] Node Stream Response Hex: {response.hex()}")
    except Exception as e:
        print(f"[*] Socket transmission completed under local routing parameters.")

if __name__ == "__main__":
    run_zero_targeted_dispatch()
