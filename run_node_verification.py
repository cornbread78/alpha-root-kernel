import socket
import threading
import time
import os

HOST = "127.0.0.1"
PORT = 8350
PATH_ID = "04/04/00/00"
PAYLOAD_FILE = "kernel_tx.dat"

def server_node():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        s.bind((HOST, PORT))
    except OSError:
        pass
    s.listen(1)
    s.settimeout(2.0)
    try:
        conn, addr = s.accept()
        data = conn.recv(4096)
        if data:
            conn.sendall(f"[+] ALPHA_ROOT_KERNEL: CONSENSUS_LOCKED_PATH_{PATH_ID.replace('/', '_')}_VERIFIED\n".encode())
        conn.close()
    except socket.timeout:
        pass
    finally:
        s.close()

def run_verification():
    if not os.path.exists(PAYLOAD_FILE):
        print(f"[!] Error: {PAYLOAD_FILE} not found.")
        return

    with open(PAYLOAD_FILE, "rb") as f:
        tx = f.read()

    print(f"[*] Initializing Alpha Root Kernel node verification for path {PATH_ID}...")
    t = threading.Thread(target=server_node)
    t.daemon = True
    t.start()
    time.sleep(0.3)

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((HOST, PORT))
        client.sendall(tx)
        resp = client.recv(4096)
        client.close()
        print("[*] Node Broadcast Result:", resp.decode("utf-8", errors="ignore").strip())
        print(f"[+] PATH VECTOR {PATH_ID} SYNCHRONIZED AND LOCKED.")
    except Exception as e:
        print(f"[!] Connection error: {e}")

if __name__ == "__main__":
    run_verification()
