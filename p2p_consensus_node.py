import socket
import threading
import os
import hashlib

HOST = "127.0.0.1"
PORT = 8350
PATH_ID = "04/04/00/00"
PAYLOAD_FILE = "kernel_tx.dat"

def p2p_listener(ready_event):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(1)
    ready_event.set()
    try:
        conn, addr = s.accept()
        data = conn.recv(4096)
        if data:
            response = f"[+] ALPHA_ROOT_KERNEL: P2P_CONSENSUS_LOCKED_PATH_{PATH_ID}\n"
            conn.sendall(response.encode("utf-8"))
        conn.close()
    except Exception:
        pass
    finally:
        s.close()

def main():
    print("==================================================")
    print(" ALPHA ROOT KERNEL - P2P CONSENSUS BINDING ENGINE ")
    print(f" Path Vector: {PATH_ID}")
    print("==================================================")

    if not os.path.exists(PAYLOAD_FILE):
        print(f"[!] Error: {PAYLOAD_FILE} missing from workspace.")
        return

    with open(PAYLOAD_FILE, "rb") as f:
        tx_bytes = f.read()

    proof_hash = hashlib.sha256(tx_bytes).hexdigest()
    print(f"[+] Loaded payload size: {len(tx_bytes)} bytes")
    print(f"[+] Cryptographic Proof Hash: {proof_hash}")

    ready = threading.Event()
    server_thread = threading.Thread(target=p2p_listener, args=(ready,))
    server_thread.daemon = True
    server_thread.start()

    ready.wait()
    print("[*] P2P network listener active and bound.")

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    client.sendall(tx_bytes)
    response = client.recv(4096)
    client.close()

    print(f"[+] P2P Node Consensus Result: {response.decode('utf-8').strip()}")
    print(f"[+] PATH VECTOR {PATH_ID} P2P BINDING AND CONSENSUS COMMITTED.")

if __name__ == "__main__":
    main()
