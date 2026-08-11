import socket
import os
import hashlib

def main():
    target_host = "179.118.220.79"
    target_port = 8333
    path_vector = "04/04/00/00"
    
    print("==================================================")
    print(" ALPHA ROOT KERNEL - FULL FRAME XOR MASK DISPATCH")
    print(f" Target Peer: {target_host}:{target_port}")
    print(f" Path Vector: {path_vector}")
    print("==================================================")

    # Load payload
    payload_file = "kernel_tx.dat"
    if os.path.exists(payload_file):
        with open(payload_file, "rb") as f:
            payload = f.read()
    else:
        payload = b"come home"

    # Construct raw transaction container with zero-filled prevtxid fields
    prev_txid_zeros = b"\x00" * 32
    
    raw_frame = (
        b"\x01\x00\x00\x00" + # Version 1
        b"\x01" +             # Input count
        prev_txid_zeros +     # Zero-filled Prev TXID (to be XOR masked)
        b"\x00\x00\x00\x00" + # Vout index 0
        b"\x00" +             # Empty scriptSig length
        b"\xff\xff\xff\xff" + # Sequence
        b"\x01" +             # Output count
        b"\x00\x00\x00\x00\x00\x00\x00\x00" + # Value 0
        bytes([len(payload)]) + # Payload length byte
        payload +             # Payload data
        b"\x00\x00\x00\x00"   # Locktime
    )

    # Apply XOR mask [4, 4, 0, 0] to the ENTIRE frame (including all zero fields)
    xor_mask = bytes([4, 4, 0, 0])
    masked_frame = bytearray(
        b ^ xor_mask[i % len(xor_mask)] for i, b in enumerate(raw_frame)
    )

    masked_hash = hashlib.sha256(masked_frame).hexdigest()
    
    print(f"[+] Unmasked frame size: {len(raw_frame)} bytes")
    print(f"[+] Applied XOR mask [4, 4, 0, 0] to all bytes (including zero-filled prevtxid)")
    print(f"[+] Computed Masked Frame SHA-256 Hash: {masked_hash}")
    print(f"[ *] Establishing TCP stream to {target_host}:{target_port}...")

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(15.0)
            s.connect((target_host, target_port))
            print("[+] Socket connection successfully established.")

            s.sendall(bytes(masked_frame))
            print("[+] Fully XOR-masked frame transmitted to node peer.")

            response = s.recv(4096)
            if response:
                print(f"[+] Node Acknowledgment Hex: {response.hex()}")
            else:
                print("[* ] Stream acknowledged and closed by node daemon.")

        print("==================================================")
        print(f"[+] PATH VECTOR {path_vector} FULL-FRAME XOR DISPATCH COMMITTED.")
        print("==================================================")

    except Exception as e:
        print(f"[!] Dispatch error: {e}")

if __name__ == "__main__":
    main()
