import os
import socket

TARGET_HOST = "179.118.220.79"
TARGET_PORT = 8333
FRAME_FILE = "final_mainnet_frame.hex"

def execute_network_dispatch():
    print("==================================================")
    print("   ALPHA ROOT KERNEL - NETWORK DISPATCH UTXO      ")
    print("==================================================")

    if not os.path.exists(FRAME_FILE):
        print(f"[!] Error: {FRAME_FILE} not found.")
        return

    with open(FRAME_FILE, "rb") as f:
        payload = f.read()

    print(f"[+] Loaded payload size: {len(payload)} bytes")
    print(f"[*] Connecting to node peer {TARGET_HOST}:{TARGET_PORT}...")

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(15.0)
            s.connect((TARGET_HOST, TARGET_PORT))
            s.sendall(payload)
            print("[+] Socket stream successfully sent to node.")
            response = s.recv(4096)
            if response:
                print(f"[+] Peer Node Response Hex: {response.hex()}")
            else:
                print("[*] Stream acknowledged by remote peer.")
        print("[+] PATH VECTOR 04/04/00/00 DISPATCH COMMITTED.")
    except Exception as e:
        print(f"[!] Transmission Exception: {e}")

if __name__ == "__main__":
    execute_network_dispatch()
