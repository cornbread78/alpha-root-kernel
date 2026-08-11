import socket
import os
import sys

# Target configuration for your running node instance
HOST = "127.0.0.1"
PORT = 8333
PAYLOAD_FILE = "kernel_tx.dat"

def main():
    print("==================================================")
    print("   ALPHA ROOT KERNEL - RUNNING NODE DISPATCH      ")
    print(f"   Target Node: {HOST}:{PORT}")
    print("==================================================\n")

    if not os.path.exists(PAYLOAD_FILE):
        print(f"[!] Error: {PAYLOAD_FILE} not found in workspace.")
        sys.exit(1)

    with open(PAYLOAD_FILE, "rb") as f:
        payload_data = f.read()

    print(f"[+] Loaded workspace payload: {len(payload_data)} bytes")
    print(f"[*] Connecting to running node socket at {HOST}:{PORT}...")

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(10.0)
            s.connect((HOST, PORT))
            print("[+] Socket connection successfully established.")

            s.sendall(payload_data)
            print("[+] Payload stream transmitted to running node instance.")

            response = s.recv(4096)
            if response:
                print(f"[+] Node Response Hex: {response.hex()}")
            else:
                print("[* ] Stream acknowledged by node daemon.")

        print("[+] PATH VECTOR 04/04/00/00 DISPATCH COMMITTED.")
    except Exception as e:
        print(f"[!] Transmission Exception: {e}")

if __name__ == "__main__":
    main()
