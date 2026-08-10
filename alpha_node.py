import socket
import sys

HOST = "127.0.0.1"
PORT = 8350
PATH_ID = "04/04/00/00"

def run_node():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        s.bind((HOST, PORT))
    except OSError as e:
        print(f"[!] Bind error on port {PORT}: {e}")
        sys.exit(1)
        
    s.listen(5)
    print(f"[*] Alpha Root Kernel Node active on {HOST}:{PORT} for path {PATH_ID}")
    print("[*] Waiting for incoming frame transmission...")
    
    try:
        while True:
            conn, addr = s.accept()
            print(f"[+] Connection established from {addr}")
            data = conn.recv(4096)
            if data:
                print(f"[+] Received raw frame: {len(data)} bytes")
                response = f"[+] ALPHA_ROOT_KERNEL: CONSENSUS_LOCKED_PATH_{PATH_ID}\n"
                conn.sendall(response.encode('utf-8'))
            conn.close()
    except KeyboardInterrupt:
        print("\n[*] Shutting down node daemon.")
        s.close()

if __name__ == "__main__":
    run_node()
