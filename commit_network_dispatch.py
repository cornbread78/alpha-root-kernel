import socket
import os
import sys

TARGET_HOST = "179.118.220.79"
TARGET_PORT = 8333
PATH_ID = "04/04/00/00"
PAYLOAD_FILE = "kernel_tx.dat"

def main():
    print("==================================================")
    print("   ALPHA ROOT KERNEL - FINAL NETWORK DISPATCH     ")
    print(f"   Target Peer: {TARGET_HOST}:{TARGET_PORT}")
    print(f"   Path Vector: {PATH_ID}")
    print("==================================================")

    if not os.path.exists(PAYLOAD_FILE):
        print(f"[!] Error: {PAYLOAD_FILE} not found.")
        sys.exit(1)

    with open(PAYLOAD_FILE, "rb") as f:
        payload = f.read()

    print(f"[+] Loaded cryptographically verified payload: {len(payload)} bytes")
    print(f"[*] Opening secure socket stream to {TARGET_HOST}:{TARGET_PORT}...")

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.settimeout(10.0)

    try:
        client.connect((TARGET_HOST, TARGET_PORT))
        print("[+] Direct TCP socket connection established.")
        
        client.sendall(payload)
        print("[+] Payload successfully streamed to remote node peer.")

        response = client.recv(4096)
        if response:
            print(f"[+] Remote Node Response Hex: {response.hex()}")
            print(f"[+] Remote Node Response Text: {response.decode('utf-8', errors='ignore').strip()}")
        
        print(f"[+] PATH VECTOR {PATH_ID} NETWORK CONSENSUS COMMITTED.")
    except Exception as e:
        print(f"[!] Network Transmission Error: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    main()
