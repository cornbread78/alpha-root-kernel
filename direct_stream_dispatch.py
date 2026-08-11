import socket
import os
import sys

TARGET_HOST = "127.0.0.1"
TARGET_PORT = 8333
PATH_VECTOR = "04/04/00/00"
PAYLOAD_FILE = "kernel_tx.dat"

def main():
    print("==================================================")
    print("   ALPHA ROOT KERNEL - DIRECT STREAM DISPATCH     ")
    print(f"   Target Endpoint: {TARGET_HOST}:{TARGET_PORT}")
    print(f"   Path Vector: {PATH_VECTOR}")
    print("==================================================")

    if not os.path.exists(PAYLOAD_FILE):
        print(f"[!] Error: {PAYLOAD_FILE} missing from workspace.")
        sys.exit(1)

    with open(PAYLOAD_FILE, "rb") as f:
        payload = f.read()

    print(f"[+] Loaded payload size: {len(payload)} bytes")
    print(f"[* ] Opening direct socket stream...")

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(10.0)
            s.connect((TARGET_HOST, TARGET_PORT))
            print("[+] Direct TCP connection established successfully.")

            s.sendall(payload)
            print("[+] Payload successfully streamed to endpoint.")

            response = s.recv(4096)
            if response:
                print(f"[+] Endpoint Response Hex: {response.hex()}")
            else:
                print("[* ] Stream accepted by endpoint (no response body).")

        print(f"[+] PATH VECTOR {PATH_VECTOR} DISPATCH COMMITTED.")
    except Exception as e:
        print(f"[!] Transmission Error: {e}")

if __name__ == "__main__":
    main()
