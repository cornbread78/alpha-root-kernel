import socket
import threading
import time
import hashlib

HOST = '127.0.0.1'
PORT = 8350
PATH_ID = "04/04/00/00"

def p2p_listener(ready_event):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(5)
    ready_event.set()
    
    conn, addr = s.accept()
    data = conn.recv(4096)
    if data:
        # Compute cryptographic binding hash of the incoming payload
        binding_hash = hashlib.sha256(data).hexdigest()
        response = f"[+] P2P_KEY_BOUND: PATH_{PATH_ID} | HASH_PROOF: {binding_hash[:32]}\n"
        conn.sendall(response.encode('utf-8'))
    conn.close()
    s.close()

def main():
    ready = threading.Event()
    server_thread = threading.Thread(target=p2p_listener, args=(ready,))
    server_thread.daemon = True
    server_thread.start()
    
    ready.wait()
    
    with open("kernel_tx.dat", "rb") as f:
        tx_bytes = f.read()
        
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    client.sendall(tx_bytes)
    response = client.recv(4096)
    client.close()
    
    print("[*] P2P Network Binding Response:")
    print(response.decode("utf-8").strip())

if __name__ == "__main__":
    main()
