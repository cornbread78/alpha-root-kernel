import os
import sys
import socket

HOST = "127.0.0.1"
PORT = 8333
PATH_ID = "04/04/00/00"
PAYLOAD_FILE = "kernel_tx.dat"

def main():
    print("==================================================")
    print("   ALPHA ROOT KERNEL - DIRECT P2P SOCKET DISPATCH ")
    print(f"   Path Vector: {PATH_ID}                        ")
    print("==================================================")

    if not os.path.exists(PAYLOAD_FILE):
        print(f"[!] Error: {PAYLOAD_FILE} missing from workspace.")
        sys.exit(1)

    with open(PAYLOAD_FILE, "rb") as f:
        payload = f.read()

    print(f"[+] Loaded payload size: {len(payload)} bytes")
    print(f"[*] Connecting to Bitcoin P2P node socket at {HOST}:{PORT}...")

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(10.0)
        s.connect((HOST, PORT))
        s.sendall(payload)
        print("[+] Payload successfully streamed to node P2P layer.")
        
        response = s.recv(4096)
        if response:
            print(f"[+] Node P2P Response Hex: {response.hex()}")
        s.close()
        print(f"[+] PATH VECTOR {PATH_ID} BROADCAST COMMITTED.")
    except Exception as e:
        print(f"[!] P2P Transmission Error: {e}")

if __name__ == "__main__":
    main()
