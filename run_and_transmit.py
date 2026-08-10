import socket
import threading
import sys

HOST = "127.0.0.1"
PORT = 8350
PATH_ID = "04/04/00/00"

def server_listener(ready_event):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        s.bind((HOST, PORT))
        s.listen(1)
        ready_event.set()
        conn, addr = s.accept()
        data = conn.recv(4096)
        if data:
            response = f"[+] ALPHA_ROOT_KERNEL: CONSENS_LOCKED_PATH_{PATH_ID}\n"
            conn.sendall(response.encode("utf-8"))
        conn.close()
    except Exception as e:
        pass
    finally:
        s.close()

def run_transmission():
    ready = threading.Event()
    t = threading.Thread(target=server_listener, args=(ready,))
    t.daemon = True
    t.start()
    
    # Wait for the listener to bind successfully
    ready.wait()

    try:
        with open("kernel_tx.dat", "rb") as f:
            payload = f.read()
    except FileNotFoundError:
        print("[!] Error: kernel_tx.dat payload not found.")
        return

    print(f"[*] Payload loaded: {len(payload)} bytes")
    print(f"[*] Connecting to local interface {HOST}:{PORT}...")

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((HOST, PORT))
        client.sendall(payload)
        resp = client.recv(4096)
        print("[+] Transmission Successful!")
        print("[*] Node Response:", resp.decode("utf-8").strip())
    except Exception as e:
        print(f"[!] Transmission failed: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    run_transmission()
