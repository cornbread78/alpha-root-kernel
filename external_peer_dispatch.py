import socket
import os
import sys

TARGET_HOST = "179.118.220.79"
TARGET_PORT = 8333
PATH_VECTOR = "04/04/00/00"
PAYLOAD_FILE = "kernel_tx.dat"

def dispatch_to_peer():
    print("==================================================")
    print("   ALPHA ROOT KERNEL - EXTERNAL PEER DISPATCH     ")
    print(f"   Target Peer: {TARGET_HOST}:{TARGET_PORT}")
    print(f"   Path Vector: {PATH_VECTOR}")
    print("==================================================")

    if not os.path.exists(PAYLOAD_FILE):
        print(f"[!] Error: {PAYLOAD_FILE} missing from workspace.")
        sys.exit(1)

    with open(PAYLOAD_FILE, "rb") as f:
        payload = f.read()

    print(f"[+] Loaded payload: {len(payload)} bytes")
    print(f"[*] Connecting to external peer socket {TARGET_HOST}:{TARGET_PORT}...")

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(10.0)
            s.connect((TARGET_HOST, TARGET_PORT))
            print("[+] Connected to external peer node successfully.")

            s.sendall(payload)
            print("[+] Payload stream transmitted to network peer.")

            response = s.recv(4096)
            if response:
                print(f"[+] Peer Response Hex: {response.hex()}")
            else:
                print("[* ] Stream acknowledged by remote peer daemon.")

        print(f"[+] PATH VECTOR {PATH_VECTOR} EXTERNAL PEER DISPATCH COMMITTED.")
    except Exception as e:
        print(f"[!] Network Dispatch Exception: {e}")

if __name__ == "__main__":
    dispatch_to_peer()
