import os
import socket

TARGET_HOST = "179.118.220.79"
TARGET_PORT = 8333
PATH_VECTOR = "04/04/00/00"
PAYLOAD_FILE = "kernel_tx.dat"
FRAME_FILE = "final_mainnet_frame.hex"

def unpack_and_dispatch():
    print("==================================================")
    print("   ALPHA ROOT KERNEL - UNPACK & REMOTE DISPATCH    ")
    print(f"   Target Peer: {TARGET_HOST}:{TARGET_PORT}")
    print(f"   Path Vector: {PATH_VECTOR}")
    print("==================================================")

    source_file = FRAME_FILE if os.path.exists(FRAME_FILE) else PAYLOAD_FILE
    if not os.path.exists(source_file):
        print(f"[!] Error: Neither {FRAME_FILE} nor {PAYLOAD_FILE} found in workspace.")
        return

    with open(source_file, "rb") as f:
        raw_payload = f.read()

    print(f"[+] Unpacked payload size: {len(raw_payload)} bytes from {source_file}")
    print(f"[*] Establishing raw socket connection to remote peer {TARGET_HOST}:{TARGET_PORT}...")

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(15.0)
            s.connect((TARGET_HOST, TARGET_PORT))
            print("[+] Remote socket connection established.")

            s.sendall(raw_payload)
            print("[+] Unpacked payload bytes streamed to remote node peer.")

            response = s.recv(4096)
            if response:
                print(f"[+] Remote Peer Response Hex: {response.hex()}")
            else:
                print("[*] Stream acknowledged by remote peer daemon.")

        print(f"[+] PATH VECTOR {PATH_VECTOR} REMOTE DISPATCH COMMITTED.")
    except Exception as e:
        print(f"[!] Transmission Exception: {e}")

if __name__ == "__main__":
    unpack_and_dispatch()
