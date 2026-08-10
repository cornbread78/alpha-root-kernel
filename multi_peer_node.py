import socket
import threading
import sys

HOST = "127.0.0.1"
PORT = 8350
PATH_ID = "04/04/00/00"
HASH_PROOF = "78a5d9fc5707af9eb253321744eae34a"

def run_node_daemon():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        s.bind((HOST, PORT))
        s.listen(5)
        print(f"[*] Multi-Peer Validator Daemon active on {HOST}:{PORT}")
        print(f"[*] Path Vector: {PATH_ID} | Hash Proof: {HASH_PROOF}")
        print("[*] Press Ctrl+C to stop the daemon cleanly.")
        
        while True:
            conn, addr = s.accept()
            client_thread = threading.Thread(target=handle_client, args=(conn, addr))
            client_thread.daemon = True
            client_thread.start()
    except KeyboardInterrupt:
        print("\n[*] Validator daemon stopped cleanly.")
    except Exception as e:
        print(f"[!] Daemon error: {e}")
    finally:
        s.close()

def handle_client(conn, addr):
    try:
        data = conn.recv(4096)
        if data:
            print(f"[*] Incoming transmission from {addr[0]}:{addr[1]} ({len(data)} bytes)")
            response = f"[+] ALPHA_ROOT_KERNEL: CONSENSUS_LOCKED_PATH_{PATH_ID}\n"
            conn.sendall(response.encode("utf-8"))
    except Exception as e:
        print(f"[!] Connection handling error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    run_node_daemon()
