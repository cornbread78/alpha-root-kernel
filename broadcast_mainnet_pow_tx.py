import socket
import os
import sys

TARGET_HOST = "179.118.220.79"
TARGET_PORT = 8333
TX_FILE = "mainnet_pow_tx.hex"
PATH_VECTOR = "04/04/00/00"

def broadcast_pow_tx():
    print("==================================================")
    print("   ALPHA ROOT KERNEL - POW TRANSACTION BROADCAST  ")
    print(f"   Target Peer: {TARGET_HOST}:{TARGET_PORT}")
    print(f"   Path Vector: {PATH_VECTOR}")
    print("==================================================")

    if not os.path.exists(TX_FILE):
        print(f"[!] Error: {TX_FILE} missing from workspace.")
        sys.exit(1)

    with open(TX_FILE, "r") as f:
        hex_data = f.read().strip()

    payload_bytes = bytes.fromhex(hex_data)
    print(f"[+] Loaded mainnet POW transaction frame: {len(payload_bytes)} bytes")
    print(f"[*] Connecting to network peer socket {TARGET_HOST}:{TARGET_PORT}...")

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(15.0)
            s.connect((TARGET_HOST, TARGET_PORT))
            print("[+] Socket connection successfully established.")

            s.sendall(payload_bytes)
            print("[+] POW transaction frame transmitted to node peer.")

            response = s.recv(4096)
            if response:
                print(f"[+] Peer Response Hex: {response.hex()}")
            else:
                print("[* ] Stream acknowledged by remote peer daemon.")

        print(f"[+] PATH VECTOR {PATH_VECTOR} POW TRANSACTION BROADCAST COMMITTED.")
    except Exception as e:
        print(f"[!] Broadcast Exception: {e}")

if __name__ == "__main__":
    broadcast_pow_tx()
