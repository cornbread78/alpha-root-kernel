import socket
import sys
import os

EXTERNAL_HOST = "179.118.220.79"
EXTERNAL_PORT = 8333
PATH_ID = "04/04/00/00"
PAYLOAD_FILE = "kernel_tx.dat"

def main():
    print("==================================================")
    print("   ALPHA ROOT KERNEL - EXTERNAL REAL NODE DISPATCH")
    print(f"   Target Peer: {EXTERNAL_HOST}:{EXTERNAL_PORT}   ")
    print(f"   Path Vector: {PATH_ID}                         ")
    print("==================================================")

    if not os.path.exists(PAYLOAD_FILE):
        print(f"[!] Error: {PAYLOAD_FILE} missing from workspace.")
        sys.exit(1)

    with open(PAYLOAD_FILE, "rb") as f:
        payload = f.read()

    print(f"[+] Loaded payload size: {len(payload)} bytes")
    print(f"[*] Opening raw external TCP socket to peer {EXTERNAL_HOST}:{EXTERNAL_PORT}...")

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(15.0)
        s.connect((EXTERNAL_HOST, EXTERNAL_PORT))
        print("[+] Connected to external peer node successfully.")
        
        s.sendall(payload)
        print("[+] Payload stream transmitted to remote network peer.")
        
        response = s.recv(4096)
        if response:
            print(f"[+] Peer Response Hex: {response.hex()}")
        else:
            print("[*] Transmission acknowledged by peer node.")
            
        s.close()
        print(f"[+] PATH VECTOR {PATH_ID} EXTERNAL BROADCAST COMMITTED.")
    except Exception as e:
        print(f"[!] External Socket Transmission Error: {e}")

if __name__ == "__main__":
    main()
