import socket
import os
import hashlib

PATH_VECTOR = "04/04/00/00"
PAYLOAD_FILE = "kernel_tx.dat"
TARGET_HOST = "179.118.220.79"
TARGET_PORT = 8333

def engage_kernel():
    print("==================================================")
    print(" ALPHA ROOT KERNEL - P2P CONSENSUS ENGAGEMENT")
    print(f" Path Vector: {PATH_VECTOR}")
    print(f" Target Node: {TARGET_HOST}:{TARGET_PORT}")
    print("==================================================")

    if not os.path.exists(PAYLOAD_FILE):
        print(f"[!] Error: {PAYLOAD_FILE} missing from workspace.")
        return

    with open(PAYLOAD_FILE, "rb") as f:
        payload = f.read()

    proof_hash = hashlib.sha256(payload).hexdigest()
    print(f"[+] Payload Loaded: {len(payload)} bytes")
    print(f"[+] Cryptographic Proof Hash: {proof_hash}")

    print(f"[* ] Establishing P2P stream to peer network...")
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(12.0)
            s.connect((TARGET_HOST, TARGET_PORT))
            print("[+] P2P Socket Connection Established.")

            s.sendall(payload)
            print("[+] Payload stream successfully transmitted to network peer.")

            response = s.recv(4096)
            if response:
                print(f"[+] Peer Acknowledgment Hex: {response.hex()}")
            else:
                print("[* ] Stream accepted; awaiting network relay confirmation.")

        print(f"[+] PATH VECTOR {PATH_VECTOR} PROOF-OF-WORK BROADCAST COMMITTED.")
    except Exception as e:
        print(f"[!] Transmission Exception: {e}")

if __name__ == "__main__":
    engage_kernel()
