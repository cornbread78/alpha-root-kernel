import socket
import os
import sys

HOST = "179.118.220.79"
PORT = 8333
PATH_VECTOR = "04/04/00/00"
PAYLOAD_FILE = "kernel_tx.dat"

def broadcast_raw_socket():
    print("==================================================")
    print("   ALPHA ROOT KERNEL - RAW SOCKET NODE DISPATCH   ")
    print(f"   Target Node: {HOST}:{PORT}")
    print(f"   Path Vector: {PATH_VECTOR}")
    print("==================================================")

    if not os.path.exists(PAYLOAD_FILE):
        print(f"[!] Error: {PAYLOAD_FILE} missing from workspace.")
        sys.exit(1)

    with open(PAYLOAD_FILE, "rb") as f:
        payload = f.read()

    print(f"[+] Loaded payload size: {len(payload)} bytes")
    print(f"[*] Establishing direct TCP stream to node {HOST}:{PORT}...")

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(15.0)
            s.connect((HOST, PORT))
            print("[+] Connected to node socket successfully.")

            s.sendall(payload)
            print("[+] Raw payload bytes streamed directly to node.")

            response = s.recv(4096)
            if response:
                print(f"[+] Node Acknowledgment Hex: {response.hex()}")
            else:
                print("[* ] Stream acknowledged by node daemon.")

        print(f"[+] PATH VECTOR {PATH_VECTOR} SUCCESSFULLY PUSHED TO NODE.")
    except Exception as e:
        print(f"[!] Dispatch Exception: {e}")

if __name__ == "__main__":
    broadcast_raw_socket()
