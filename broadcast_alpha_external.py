import socket
import os
import sys

# Update HOST and PORT to point to your real external node endpoint if needed
HOST = "127.0.0.1"
PORT = 8333
PATH_ID = "04/04/00/00"

def main():
    if not os.path.exists("kernel_tx.dat"):
        print("[!] Error: kernel_tx.dat not found in workspace.")
        sys.exit(1)

    with open("kernel_tx.dat", "rb") as f:
        payload = f.read()

    print(f"[*] Loaded workspace payload: {len(payload)} bytes")
    print(f"[*] Target Path Vector: {PATH_ID}")
    print(f"[*] Connecting to target node at {HOST}:{PORT}...")

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.settimeout(10.0)

    try:
        client.connect((HOST, PORT))
        client.sendall(payload)
        response = client.recv(4096)
        
        print("[+] External Node Response Hex:", response.hex())
        print("[+] External Node Response Text:", response.decode("utf-8", errors="ignore").strip())
        print(f"[+] PATH VECTOR {PATH_ID} TRANSMISSION COMMITTED.")
    except Exception as e:
        print(f"[!] Transmission error: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    main()
