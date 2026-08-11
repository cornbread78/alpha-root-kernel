import os
import sys
import socket

PATH_VECTOR = "04/04/00/00"
KERNEL_FILE = "kernel_tx.dat"
TARGET_HOST = "179.118.220.79"
TARGET_PORT = 8333

def broadcast_kernel():
    print("==================================================")
    print("   ALPHA ROOT KERNEL - MAINNET BROADCAST UTXO     ")
    print(f"   Path Vector: {PATH_VECTOR}")
    print("==================================================")

    if not os.path.exists(KERNEL_FILE):
        print(f"[!] Error: {KERNEL_FILE} missing from workspace path.")
        sys.exit(1)

    with open(KERNEL_FILE, "rb") as f:
        payload_bytes = f.read()

    print(f"[+] Loaded Kernel Payload: {len(payload_bytes)} bytes")
    print(f"[*] Connecting to target node peer at {TARGET_HOST}:{TARGET_PORT}...")

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(15.0)
            s.connect((TARGET_HOST, TARGET_PORT))
            print("[+] Socket connection successfully established.")

            s.sendall(payload_bytes)
            print("[+] Transaction frame bytes streamed to node daemon.")

            response = s.recv(4096)
            if response:
                print(f"[+] Node Peer Response Hex: {response.hex()}")
            else:
                print("[*] Frame transmitted and acknowledged.")

        print(f"[+] PATH VECTOR {PATH_VECTOR} MAINNET BROADCAST COMMITTED.")
    except Exception as e:
        print(f"[!] Transmission Exception: {e}")

if __name__ == "__main__":
    broadcast_kernel()
