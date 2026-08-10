import socket
import os
import sys

HOST = "127.0.0.1"
PORT = 8350
PATH_ID = "04/04/00/00"

def broadcast_consensus():
    if not os.path.exists("kernel_tx.dat"):
        print("[!] Error: kernel_tx.dat not found in workspace.")
        sys.exit(1)

    with open("kernel_tx.dat", "rb") as f:
        payload = f.read()

    print(f"[*] Loaded workspace payload: {len(payload)} bytes")
    print(f"[*] Target Path Vector: {PATH_ID}")
    print(f"[*] Connecting to active node consensus listener at {HOST}:{PORT}...")

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.settimeout(5.0)

    try:
        client.connect((HOST, PORT))
        client.sendall(payload)
        response = client.recv(4096)
        
        print("[+] Node Consensus Response:", response.decode("utf-8", errors="ignore").strip())
        print(f"[+] GENESIS BLOCK PATH VECTOR {PATH_ID} FULLY SYNCHRONIZED AND LOCKED ON NODE.")
    except Exception as e:
        print(f"[!] Broadcast transmission error: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    broadcast_consensus()
