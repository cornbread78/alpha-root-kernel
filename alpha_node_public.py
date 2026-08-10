import socket
import sys

PORT = 8350
PATH_ID = "04/04/00/00"

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def run_public_node():
    HOST = "0.0.0.0"
    local_ip = get_local_ip()
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        s.bind((HOST, PORT))
    except OSError as e:
        print(f"[!] Bind error on port {PORT}: {e}")
        sys.exit(1)

    s.listen(5)
    print(f"[*] Alpha Root Kernel Node active on ALL interfaces ({HOST}:{PORT})")
    print(f"[*] Local Network Accessible IP: {local_ip}:{PORT}")
    print(f"[*] Path Vector: {PATH_ID}")
    print("[*] Waiting for external network frame transmission...")

    try:
        while True:
            conn, addr = s.accept()
            print(f"[+] External connection established from {addr[0]}:{addr[1]}")
            data = conn.recv(4096)
            if data:
                print(f"[+] Received raw frame: {len(data)} bytes")
                response = f"[+] ALPHA_ROOT_KERNEL: CONSENSUS_LOCKED_PATH_{PATH_ID}\n"
                conn.sendall(response.encode('utf-8'))
            conn.close()
    except KeyboardInterrupt:
        print("\n[*] Shutting down public node daemon.")
        s.close()

if __name__ == "__main__":
    run_public_node()
