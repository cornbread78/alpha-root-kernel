import socket
import json
import os
import hashlib

HOST = "127.0.0.1"
PORT = 8350
PATH_ID = "04/04/00/00"

def open_and_broadcast_kernel():
    print(f"[*] Opening Alpha Root Kernel for Path Vector: {PATH_ID}")
    
    if not os.path.exists("kernel_tx.dat"):
        print("[!] Error: kernel_tx.dat not found in workspace.")
        return
        
    with open("kernel_tx.dat", "rb") as f:
        payload = f.read()
        
    payload_hash = hashlib.sha256(payload).hexdigest()
    print(f"[+] Loaded Kernel Binary Payload: {len(payload)} bytes")
    print(f"[+] Payload SHA-256: {payload_hash}")
    
    if os.path.exists("alpha_root.ledger"):
        with open("alpha_root.ledger", "r") as f:
            print(f"[+] Loaded Ledger Record: {f.read().strip()}")
            
    print(f"[*] Dispatching kernel broadcast stream to local node interface {HOST}:{PORT}...")
    
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.settimeout(5.0)
    try:
        client.connect((HOST, PORT))
        client.sendall(payload)
        response = client.recv(4096)
        print("[+] Broadcast Response:", response.decode("utf-8", errors="ignore").strip())
        print(f"[+] ALPHA ROOT KERNEL PATH {PATH_ID} OPENED AND BROADCAST COMMITTED SUCCESSFULLY.")
    except Exception as e:
        print(f"[!] Broadcast transmission error: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    open_and_broadcast_kernel()
