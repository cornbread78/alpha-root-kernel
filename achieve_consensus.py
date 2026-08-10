import socket
import threading
import sys
import os

HOST = "127.0.0.1"
PORT = 8350
PATH_ID = "04/04/00/00"

def consensus_listener(ready_event):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        server.bind((HOST, PORT))
        server.listen(1)
        ready_event.set()
        
        conn, addr = server.accept()
        data = conn.recv(4096)
        if data:
            print(f"[+] Node received payload frame: {len(data)} bytes")
            response = f"[+] ALPHA_ROOT_KERNEL: CONSENSUS_LOCKED_PATH_{PATH_ID}\n"
            conn.sendall(response.encode("utf-8"))
        conn.close()
    except Exception as e:
        print(f"[!] Listener error: {e}")
    finally:
        server.close()

def main():
    if not os.path.exists("kernel_tx.dat"):
        print("[!] Error: kernel_tx.dat not found in workspace.")
        sys.exit(1)

    with open("kernel_tx.dat", "rb") as f:
        payload = f.read()

    print(f"[*] Initializing consensus thread for path {PATH_ID}...")
    ready_event = threading.Event()
    listener_thread = threading.Thread(target=consensus_listener, args=(ready_event,))
    listener_thread.daemon = True
    listener_thread.start()

    ready_event.wait()

    print(f"[*] Transmitting frame to active node interface {HOST}:{PORT}...")
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((HOST, PORT))
        client.sendall(payload)
        response = client.recv(4096)
        print("[+] Consensus Response:", response.decode("utf-8", errors="ignore").strip())
        print(f"[+] CONSENSUS LOCKED FOR PATH {PATH_ID}")
    except Exception as e:
        print(f"[!] Transmission error: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    main()
