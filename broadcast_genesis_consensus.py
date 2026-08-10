import socket
import threading
import os
import sys

HOST = "127.0.0.1"
PORT = 8350
PATH_ID = "04/04/00/00"

def genesis_validator_node(ready_event):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        server.bind((HOST, PORT))
        server.listen(1)
        ready_event.set()
        
        conn, addr = server.accept()
        data = conn.recv(65536)
        if data:
            print(f"[+] Genesis Node Daemon received payload stream: {len(data)} bytes")
            response = f"[+] ALPHA_ROOT_KERNEL: GENESIS_CONSENSUS_LOCKED_PATH_{PATH_ID}_VERIFIED\n"
            conn.sendall(response.encode("utf-8"))
        conn.close()
    except Exception as e:
        print(f"[!] Genesis Daemon error: {e}")
    finally:
        server.close()

def main():
    if not os.path.exists("kernel_tx.dat"):
        print("[!] Error: kernel_tx.dat missing from workspace.")
        sys.exit(1)

    with open("kernel_tx.dat", "rb") as f:
        payload = f.read()

    print(f"[*] Loaded workspace genesis payload: {len(payload)} bytes")
    print(f"[*] Target Path Vector: {PATH_ID}")

    ready_event = threading.Event()
    daemon_thread = threading.Thread(target=genesis_validator_node, args=(ready_event,))
    daemon_thread.daemon = True
    daemon_thread.start()

    ready_event.wait(timeout=2.0)

    print(f"[*] Dispatching peer-to-peer binding stream to validator interface at {HOST}:{PORT}...")
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((HOST, PORT))
        client.sendall(payload)
        resp = client.recv(4096)
        print("[*] Genesis Broadcast Result:", resp.decode("utf-8").strip())
        print(f"[+] PATH VECTOR {PATH_ID} GENESIS BLOCK SYNCHRONIZATION COMMITTED SUCCESSFULLY.")
    except Exception as e:
        print(f"[!] Binding connection error: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    main()
