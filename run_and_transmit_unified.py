import socket
import threading
import sys

HOST = "127.0.0.1"
PORT = 8350
PATH_ID = "04/04/00/00"

def run_server(ready_event):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        s.bind((HOST, PORT))
        s.listen(1)
        ready_event.set()
        conn, addr = s.accept()
        data = conn.recv(4096)
        if data:
            response = f"[+] ALPHA_ROOT_KERNEL: CONSENSUS_LOCKED_PATH_{PATH_ID}\n"
            conn.sendall(response.encode("utf-8"))
        conn.close()
    except Exception as e:
        print(f"[!] Server error: {e}")
    finally:
        s.close()

def main():
    try:
        with open("kernel_tx.dat", "rb") as f:
            tx_bytes = f.read()
    except FileNotFoundError:
        print("[!] Error: kernel_tx.dat not found.")
        sys.exit(1)

    print(f"[*] Payload loaded: {len(tx_bytes)} bytes")

    ready = threading.Event()
    server_thread = threading.Thread(target=run_server, args=(ready,))
    server_thread.daemon = True
    server_thread.start()

    ready.wait()

    print(f"[*] Connecting to local interface {HOST}:{PORT}...")
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((HOST, PORT))
        client.sendall(tx_bytes)
        response = client.recv(4096)
        print("[+] Transmission Successful!")
        print("[*] Node Response:", response.decode("utf-8", errors="ignore").strip())
    except Exception as e:
        print(f"[!] Transmission error: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    main()
