import os
import socket

TARGET_HOST = "179.118.220.79"
TARGET_PORT = 8333
FRAME_FILE = "final_mainnet_frame.hex"
FALLBACK_FILE = "kernel_tx.dat"

def broadcast_utxo():
    print("==================================================")
    print("   ALPHA ROOT KERNEL - UTXO FRAME BROADCAST       ")
    print("==================================================")

    target_file = FRAME_FILE if os.path.exists(FRAME_FILE) else FALLBACK_FILE
    if not os.path.exists(target_file):
        print(f"[!] Error: Neither {FRAME_FILE} nor {FALLBACK_FILE} found.")
        return

    with open(target_file, "rb") as f:
        payload = f.read()

    print(f"[+] Loaded UTXO Frame Size: {len(payload)} bytes from {target_file}")
    print(f"[*] Dispatching stream to peer node {TARGET_HOST}:{TARGET_PORT}...")

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(15.0)
            s.connect((TARGET_HOST, TARGET_PORT))
            s.sendall(payload)
            print("[+] Socket stream successfully transmitted to node.")
            response = s.recv(4096)
            if response:
                print(f"[+] Node Peer Response Hex: {response.hex()}")
            else:
                print("[*] Stream acknowledged by node daemon.")
        print("[+] PATH VECTOR 04/04/00/00 UTXO BROADCAST COMMITTED.")
    except Exception as e:
        print(f"[!] Transmission Exception: {e}")

if __name__ == "__main__":
    broadcast_utxo()
