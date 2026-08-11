import os
import socket

TARGET_HOST = "179.118.220.79"
TARGET_PORT = 8333
FRAME_FILE = "final_mainnet_frame.hex"

def broadcast_frame():
    print("==================================================")
    print("   ALPHA ROOT KERNEL - FINAL FRAME DISPATCH       ")
    print("==================================================")

    if not os.path.exists(FRAME_FILE):
        print(f"[!] Error: {FRAME_FILE} not found. Please run the encoder first.")
        return

    with open(FRAME_FILE, "rb") as f:
        payload = f.read()

    print(f"[+] Loaded Final Frame Size: {len(payload)} bytes")
    print(f"[*] Dispatching stream to peer node {TARGET_HOST}:{TARGET_PORT}...")

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(15.0)
            s.connect((TARGET_HOST, TARGET_PORT))
            s.sendall(payload)
            print("[+] Socket stream successfully sent to node.")
            response = s.recv(4096)
            if response:
                print(f"[+] Node Peer Response Hex: {response.hex()}")
            else:
                print("[*] Stream acknowledged by node.")
        print("[+] PATH VECTOR 04/04/00/00 FINAL DISPATCH COMMITTED.")
    except Exception as e:
        print(f"[!] Transmission Exception: {e}")

if __name__ == "__main__":
    broadcast_frame()
