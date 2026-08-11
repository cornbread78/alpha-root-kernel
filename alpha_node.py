import socket

HOST = '127.0.0.1'
PORT = 8350

def run_node():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Enable SO_REUSEADDR to prevent [Errno 98] Address already in use
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        s.bind((HOST, PORT))
        s.listen(1)
        print(f"[*] Alpha Root Node listening on {HOST}:{PORT}...")
        
        while True:
            conn, addr = s.accept()
            print(f"[+] Connected by {addr}")
            data = conn.recv(1024)
            if data:
                conn.sendall(b"[+] ALPHA_ROOT_KERNEL: CONSENSUS_LOCKED_PATH_04/04/00/00\n")
            conn.close()
    except Exception as e:
        print(f"[!] Node error: {e}")
    finally:
        s.close()

if __name__ == '__main__':
    run_node()
