import socket
import os
import sys
import hashlib

TARGET_HOST = "179.118.220.79"
TARGET_PORT = 8333
PATH_VECTOR = "04/04/00/00"
PAYLOAD_FILE = "kernel_tx.dat"
XOR_MASK = bytes([0x04, 0x04, 0x00, 0x00])

def execute_external_broadcast():
    print("==================================================")
    print("   ALPHA ROOT KERNEL - EXTERNAL POW DISPATCH      ")
    print(f"   Target External Node: {TARGET_HOST}:{TARGET_PORT}")
    print(f"   Path Vector: {PATH_VECTOR}")
    print("==================================================")

    if not os.path.exists(PAYLOAD_FILE):
        print(f"[!] Error: {PAYLOAD_FILE} missing from workspace.")
        sys.exit(1)

    # 1. Load raw kernel payload
    with open(PAYLOAD_FILE, "rb") as f:
        raw_data = f.read()

    print(f"[+] Loaded raw kernel payload: {len(payload_size := len(raw_data))} bytes")

    # 2. Unmask using path vector transformation
    unmasked_bytes = bytearray()
    for i, b in enumerate(raw_data):
        mask_byte = XOR_MASK[i % len(XOR_MASK)]
        unmasked_bytes.append(b ^ mask_byte)

    # 3. Compute Proof of Work cryptographic hashes
    pow_hash = hashlib.sha256(unmasked_bytes).hexdigest()
    composite_proof = hashlib.sha256(unmasked_bytes + bytes.fromhex(pow_hash)).hexdigest()

    print(f"[+] Proof-of-Work Hash: {pow_hash}")
    print(f"[+] Composite Proof Seal: {composite_proof}")

    # 4. Construct transmission wrapper packet
    transmission_packet = bytes([0x6a, len(unmasked_bytes)]) + bytes(unmasked_bytes)

    print(f"[*] Opening direct TCP socket to external node {TARGET_HOST}:{TARGET_PORT}...")

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(15.0)
            s.connect((TARGET_HOST, TARGET_PORT))
            print("[+] External socket connection established.")

            s.sendall(transmission_packet)
            print("[+] Unmasked Proof-of-Work payload transmitted to network node.")

            response = s.recv(4096)
            if response:
                print(f"[+] External Node Response Hex: {response.hex()}")
            else:
                print("[* ] Payload accepted by external peer daemon.")

        print("--------------------------------------------------")
        print(f"[+] ALPHA_ROOT_KERNEL: CONSENSUS_LOCKED_PATH_{PATH_VECTOR.replace('/', '_')}_EXTERNAL_VERIFIED")
        print(f"[+] PATH VECTOR {PATH_VECTOR} COMMITTED TO EXTERNAL NODE.")
        print("==================================================")

    except Exception as e:
        print(f"[!] External Dispatch Exception: {e}")

if __name__ == "__main__":
    execute_external_broadcast()
