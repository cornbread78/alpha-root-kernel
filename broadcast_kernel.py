import socket
import sys

HOST = "127.0.0.1"
PORT = 8350
PATH_ID = "04/04/00/00"

def broadcast_kernel():
    print(f"[*] Loading kernel transaction payload for path {PATH_ID}...")
    try:
        with open("kernel_tx.dat", "rb") as f:
            tx_data = f.read()
    except FileNotFoundError:
        print("[!] Error: kernel_tx.dat not found.")
        sys.exit(1)

    print(f"[*] Payload loaded: {len(tx_data)} bytes")
    print(f"[*] Transmitting frame to node interface {HOST}:{PORT}...")

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((HOST, PORT))
        client.sendall(tx_data)
        response = client.recv(4096)
        print("[*] Broadcast Confirmation Received:")
        print(response.decode("utf-8").strip())
    except Exception as e:
        print(f"[!] Transmission error: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    broadcast_kernel()
