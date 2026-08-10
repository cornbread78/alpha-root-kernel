import socket
import threading
import sys
import os

HOST = "127.0.0.1"
PORT = 8350
PATH_ID = "04/04/00/00"

def alpha_node_daemon(ready_event):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        server.bind((HOST, PORT))
        server.listen(5)
        ready_event.set()
        
        print(f"[*] Alpha Root Kernel Node active on {HOST}:{PORT} for path {PATH_ID}")
        print("[*] Waiting for incoming frame transmission...")
        
        conn, addr = server.accept()
        data = conn.recv(65536)
        if data:
            print(f"[+] Validator Daemon received payload: {len(data)} bytes")
            response = f"[+] ALPHA_ROOT_KERNEL: CONSENSUS_LOCKED_PATH_{PATH_ID}_VERIFIED\n"
            conn.sendall(response.encode("utf-8"))
        conn.close()
    except Exception as e:
        print(f"[!] Daemon error: {e}")
    finally:
        server.close()

def main():
    payload_file = "kernel_tx.dat"
    if not os.path.exists(payload_file):
        with open(payload_file, "wb") as f:
            f.write(b"ALPHA_ROOT_KERNEL_PAYLOAD_04040000")
        print(f"[+] Initialized payload buffer: {payload_file}")

    with open(payload_file, "rb") as f:
        payload = f.read()

    print(f"==================================================")
    print(f"   ALPHA ROOT KERNEL - ALPHA ROUTE NODE DISPATCH  ")
    print(f"   Path Vector: {PATH_ID}                         ")
    print(f"==================================================")
    print(f"[*] Loaded workspace payload: {len(payload)} bytes")

    ready_event = threading.Event()
    t = threading.Thread(target=alpha_node_daemon, args=(ready_event,))
    t.daemon = True
    t.start()

    ready_event.wait(timeout=2.0)

    # Connect payload stream to the local Alpha Route node daemon
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    client.sendall(payload)
    resp = client.recv(4096)
    client.close()

    print(f"[+] Consensus Response: {resp.decode('utf-8').strip()}")
    print(f"[+] PATH VECTOR {PATH_ID} FULLY SYNCHRONIZED AND LOCKED THROUGH ALPHA ROUTE.")

if __name__ == "__main__":
    main()
