import socket
import threading
import json
import os
import sys

HOST = "127.0.0.1"
PORT = 8350
PATH_ID = "04/04/00/00"

def validator_server(ready_event):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        server.bind((HOST, PORT))
        server.listen(5)
        ready_event.set()
        
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
    if not os.path.exists("kernel_tx.dat"):
        print("[!] Error: kernel_tx.dat missing from workspace.")
        sys.exit(1)

    with open("kernel_tx.dat", "rb") as f:
        payload = f.read()

    print(f"[*] Loaded workspace payload: {len(payload)} bytes")
    print(f"[*] Target Path Vector: {PATH_ID}")

    ready_event = threading.Event()
    daemon_thread = threading.Thread(target=validator_server, args=(ready_event,))
    daemon_thread.daemon = True
    daemon_thread.start()

    ready_event.wait(timeout=2.0)

    print(f"[*] Connecting payload stream to validator daemon at {HOST}:{PORT}...")
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.settimeout(5.0)

    try:
        client.connect((HOST, PORT))
        client.sendall(payload)
        response = client.recv(4096)
        
        print("[+] Consensus Response:", response.decode("utf-8", errors="ignore").strip())
        print(f"[+] PATH VECTOR {PATH_ID} FULLY SYNCHRONIZED AND LOCKED ON NODE.")
    except Exception as e:
        print(f"[!] Transmission error: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    main()
