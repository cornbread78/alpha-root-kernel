import socket
import sys

# Configuration for external network transmission
TARGET_HOST = "0.0.0.0"  # Set to target listener or broadcast IP
TARGET_PORT = 8350
PATH_ID = "04/04/00/00"

def broadcast_kernel():
    try:
        with open("kernel_tx.dat", "rb") as f:
            payload = f.read()
    except FileNotFoundError:
        print("[!] Error: kernel_tx.dat not found in workspace.")
        sys.exit(1)

    print(f"[*] Loaded kernel payload: {len(payload)} bytes")
    print(f"[*] Initializing external socket stream for path {PATH_ID}...")

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.settimeout(15.0)

    try:
        # Connect to the specified external node or interface
        client.connect((TARGET_HOST if TARGET_HOST != "0.0.0.0" else "127.0.0.1", TARGET_PORT))
        print(f"[+] Connected to target interface successfully.")

        client.sendall(payload)
        print("[+] Payload frame transmitted across network stream.")

        response = client.recv(4096)
        if response:
            print(f"[+] Remote Node Response: {response.decode('utf-8', errors='ignore').strip()}")
        else:
            print("[*] Stream acknowledged by target endpoint.")

    except Exception as e:
        print(f"[!] External broadcast transmission error: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    broadcast_kernel()
