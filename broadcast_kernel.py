import socket
import sys
import os

TARGET_HOST = "179.118.220.79"
TARGET_PORT = 8333
PATH_VECTOR = "04/04/00/00"
PAYLOAD_FILE = "kernel_tx.dat"

def main():
    print("==================================================")
    print("   ALPHA ROOT KERNEL - NODE DISPATCH BRIDGE       ")
    print(f"   Target: {TARGET_HOST}:{TARGET_PORT}")
    print(f"   Path Vector: {PATH_VECTOR}")
    print("==================================================")

    if not os.path.exists(PAYLOAD_FILE):
        print(f"[!] Error: {PAYLOAD_FILE} not found in current directory.")
        sys.exit(1)

    with open(PAYLOAD_FILE, "rb") as f:
        raw_payload = f.read()

    print(f"[+] Loaded payload: {len(raw_payload)} bytes")

    # Apply path vector derivation and XOR mask structure
    path_bytes = PATH_VECTOR.encode("utf-8")
    masked_payload = bytearray()
    for i, b in enumerate(raw_payload):
        mask_key = path_bytes[i % len(path_bytes)]
        masked_payload.append(b ^ mask_key)

    print("[+] Applied path vector XOR mask transformation.")
    print(f"[*] Connecting to network peer {TARGET_HOST}:{TARGET_PORT}...")

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(10.0)
        s.connect((TARGET_HOST, TARGET_PORT))
        print("[+] Socket connection established.")

        s.sendall(masked_payload)
        print("[+] Transmitted masked payload stream to node.")

        response = s.recv(4096)
        if response:
            print(f"[+] Node Response Hex: {response.hex()}")
        else:
            print("[*] Stream acknowledged by remote node.")

        s.close()
        print(f"[+] PATH VECTOR {PATH_VECTOR} TRANSMISSION COMMITTED.")
    except Exception as e:
        print(f"[!] Transmission Error: {e}")

if __name__ == "__main__":
    main()
