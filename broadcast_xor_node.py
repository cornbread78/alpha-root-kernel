import socket
import os
import sys

HOST = "179.118.220.79"
PORT = 8333
PATH_VECTOR = "04/04/00/00"
MASKED_FILE = "xor_masked_op_return.hex"

def broadcast_xor_payload():
    print("==================================================")
    print("   ALPHA ROOT KERNEL - XOR NODE DISPATCH          ")
    print(f"   Target Node: {HOST}:{PORT}")
    print(f"   Path Vector: {PATH_VECTOR}")
    print("==================================================")

    if not os.path.exists(MASKED_FILE):
        print(f"[!] Error: {MASKED_FILE} missing from workspace.")
        sys.exit(1)

    # Read raw binary bytes directly
    with open(MASKED_FILE, "rb") as f:
        payload_bytes = f.read()

    print(f"[+] Loaded XOR payload size: {len(payload_bytes)} bytes")
    print(f"[*] Establishing direct TCP stream to node {HOST}:{PORT}...")

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(15.0)
            s.connect((HOST, PORT))
            print("[+] Connected to node socket successfully.")

            s.sendall(payload_bytes)
            print("[+] XOR-masked payload bytes streamed directly to node.")

            response = s.recv(4096)
            if response:
                print(f"[+] Node Acknowledgment Hex: {response.hex()}")
            else:
                print("[*] Stream acknowledged by node daemon.")

        print(f"[+] PATH VECTOR {PATH_VECTOR} XOR PAYLOAD SUCCESSFULLY PUSHED.")
    except Exception as e:
        print(f"[!] Dispatch Exception: {e}")

if __name__ == "__main__":
    broadcast_xor_payload()
