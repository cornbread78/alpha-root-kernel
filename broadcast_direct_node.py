import os
import sys
import socket

TARGET_HOST = "179.118.220.79"
TARGET_PORT = 8333
PATH_VECTOR = "04/04/00/00"
PAYLOAD_FILE = "kernel_tx.dat"

def main():
    print("==================================================")
    print("   ALPHA ROOT KERNEL - DIRECT NODE DISPATCH       ")
    print(f"   Target: {TARGET_HOST}:{TARGET_PORT}")
    print(f"   Path Vector: {PATH_VECTOR}")
    print("==================================================")

    if not os.path.exists(PAYLOAD_FILE):
        print(f"[!] Error: {PAYLOAD_FILE} not found in workspace.")
        sys.exit(1)

    with open(PAYLOAD_FILE, "rb") as f:
        payload_data = f.read()

    print(f"[+] Loaded payload size: {len(payload_data)} bytes")
    print(f"[*] Establishing direct TCP connection to {TARGET_HOST}:{TARGET_PORT}...")

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(15.0)
            s.connect((TARGET_HOST, TARGET_PORT))
            print("[+] Socket connection successfully established.")

            s.sendall(payload_data)
            print("[+] Payload successfully streamed to node socket.")

            response = s.recv(4096)
            if response:
                print(f"[+] Node Response Hex: {response.hex()}")
                print(f"[+] Node Response Text: {response.decode('utf-8', errors='ignore').strip()}")
            else:
                print("[*] Stream acknowledged by remote peer.")

        print(f"[+] PATH VECTOR {PATH_VECTOR} TRANSMISSION COMMITTED.")
    except Exception as e:
        print(f"[!] Dispatch Exception: {e}")

if __name__ == "__main__":
    main()
