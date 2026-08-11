import socket
import os
import sys

# Target configuration for external network peer node
HOST = "179.118.220.79"
PORT = 8333
PAYLOAD_FILE = "kernel_tx.dat"
XOR_MASK = [4, 4, 0, 0]

def main():
    print("==================================================")
    print("   ALPHA ROOT KERNEL - EXTERNAL NODE DISPATCH     ")
    print(f"   Target Peer: {HOST}:{PORT}")
    print("   Path Vector: 04/04/00/00")
    print("==================================================\n")

    if not os.path.exists(PAYLOAD_FILE):
        print(f"[!] Error: {PAYLOAD_FILE} not found in workspace.")
        sys.exit(1)

    with open(PAYLOAD_FILE, "rb") as f:
        raw_payload = f.read()

    print(f"[+] Loaded raw kernel payload: {len(raw_payload)} bytes")

    # Apply XOR Mask transformation
    masked_payload = bytearray(
        b ^ XOR_MASK[i % len(XOR_MASK)] for i, b in enumerate(raw_payload)
    )
    print(f"[+] Applied XOR mask transformation: {XOR_MASK}")

    print(f"[*] Opening raw external TCP socket to peer {HOST}:{PORT}...")

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(15.0)
            s.connect((HOST, PORT))
            print("[+] Connected to external peer node successfully.")

            s.sendall(masked_payload)
            print("[+] Masked payload stream transmitted to remote network peer.")

            response = s.recv(4096)
            if response:
                print(f"[+] Remote Node Acknowledgment Hex: {response.hex()}")
            else:
                print("[*] Stream acknowledged by remote peer daemon.")

        print("[+] PATH VECTOR 04/04/00/00 EXTERNAL DISPATCH COMMITTED.")
    except Exception as e:
        print(f"[!] Transmission Exception: {e}")

if __name__ == "__main__":
    main()
