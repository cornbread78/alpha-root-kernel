import socket
import sys
import os

# External Bitcoin peer node target endpoint
EXTERNAL_HOST = "179.118.220.79"
EXTERNAL_PORT = 8333
PATH_ID = "04/04/00/00"
PAYLOAD_FILE = "kernel_tx.dat"

def main():
    print("==================================================")
    print("   ALPHA ROOT KERNEL - EXTERNAL P2P DISPATCHER    ")
    print(f"   Target Node: {EXTERNAL_HOST}:{EXTERNAL_PORT}   ")
    print(f"   Path Vector: {PATH_ID}                         ")
    print("==================================================")

    if not os.path.exists(PAYLOAD_FILE):
        print(f"[!] Error: {PAYLOAD_FILE} missing from workspace.")
        sys.exit(1)

    with open(PAYLOAD_FILE, "rb") as f:
        payload = f.read()

    print(f"[+] Loaded payload size: {len(payload)} bytes")
    print(f"[*] Opening raw socket to external node {EXTERNAL_HOST}:{EXTERNAL_PORT}...")

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(12.0)
        s.connect((EXTERNAL_HOST, EXTERNAL_PORT))
        print("[+] External TCP socket connection established.")
        
        s.sendall(payload)
        print("[+] Payload successfully streamed to remote node peer.")
        
        response = s.recv(4096)
        if response:
            print(f"[+] Remote Node Response Hex: {response.hex()}")
        else:
            print("[*] Connection active, awaiting asynchronous remote acknowledgement.")
            
        s.close()
        print(f"[+] PATH VECTOR {PATH_ID} EXTERNAL TRANSMISSION COMMITTED.")
    except Exception as e:
        print(f"[!] External Socket Transmission Error: {e}")

if __name__ == "__main__":
    main()
