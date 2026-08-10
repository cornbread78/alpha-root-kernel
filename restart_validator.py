import socket
import threading
import time
import sys

HOST = "127.0.0.1"
PORT = 8350
PATH_ID = "04/04/00/00"

def background_validator():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        server.bind((HOST, PORT))
        server.listen(5)
        print(f"[+] Validator node listener successfully bound to {HOST}:{PORT}")
        while True:
            try:
                server.settimeout(1.0)
                conn, addr = server.accept()
                data = conn.recv(65536)
                if data:
                    print(f"[+] Received sync frame from {addr}: {len(data)} bytes")
                    response = f"[+] ALPHA_ROOT_KERNEL: VALIDATOR_ONLINE_PATH_{PATH_ID}_ACTIVE\n"
                    conn.sendall(response.encode("utf-8"))
                conn.close()
            except socket.timeout:
                continue
            except Exception as e:
                break
    except Exception as e:
        print(f"[!] Port bind error (is another instance running?): {e}")
    finally:
        server.close()

if __name__ == "__main__":
    print(f"[*] Restoring validator node for path {PATH_ID}...")
    t = threading.Thread(target=background_validator)
    t.daemon = True
    t.start()
    
    print("[*] Validator node is online and listening. Press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[*] Shutting down validator node.")

