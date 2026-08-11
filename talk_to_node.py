import socket
import os

HOST = "127.0.0.1"
PORT = 8350
PATH_ID = "04/04/00/00"
PAYLOAD_FILE = "kernel_tx.dat"

def communicate_with_node():
    print("==================================================")
    print(" ALPHA ROOT KERNEL - DIRECT NODE COMMUNICATION   ")
    print(f" Target Node: {HOST}:{PORT}")
    print(f" Path Vector: {PATH_ID}")
    print("==================================================")

    if not os.path.exists(PAYLOAD_FILE):
        print(f"[!] Error: {PAYLOAD_FILE} not found.")
        return

    with open(PAYLOAD_FILE, "rb") as f:
        payload = f.read()

    print(f"[+] Loaded payload: {len(payload)} bytes")
    
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((HOST, PORT))
        client.sendall(payload)
        response = client.recv(4096)
        client.close()
        
        print(f"[+] Socket connection established successfully.")
        print(f"[+] Node Response: {response.decode('utf-8').strip()}")
        print(f"[+] STATUS: NODE_COMMUNICATION_LOCKED_PATH_{PATH_ID.replace('/', '_')}")
    except Exception as e:
        print(f"[!] Connection Exception: {e}")

if __name__ == "__main__":
    communicate_with_node()
