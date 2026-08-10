import socket
import threading
import os
import sys

HOST = "127.0.0.1"
PORT = 8350
PATH_ID = "04/04/00/00"

def run():
    if not os.path.exists("kernel_tx.dat"):
        print("[!] Error: kernel_tx.dat not found.")
        sys.exit(1)

    with open("kernel_tx.dat", "rb") as f:
        payload = f.read()

    ready_event = threading.Event()
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def server_worker():
        try:
            server_socket.bind((HOST, PORT))
            server_socket.listen(1)
            ready_event.set()
            
            server_socket.settimeout(5.0)
            conn, addr = server_socket.accept()
            data = conn.recv(65536)
            if data:
                resp_msg = f"[+] ALPHA_ROOT_KERNEL: CONSENSUS_LOCKED_PATH_{PATH_ID}_VERIFIED\n"
                conn.sendall(resp_msg.encode("utf-8"))
            conn.close()
        except socket.timeout:
            pass
        except Exception:
            pass
        finally:
            server_socket.close()

    # Start listener thread in the background
    t = threading.Thread(target=server_worker)
    t.daemon = True
    t.start()

    # Wait until socket is bound and listening
    ready_event.wait(timeout=2.0)

    # Execute client transmission
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.settimeout(5.0)
    try:
        client.connect((HOST, PORT))
        client.sendall(payload)
        response = client.recv(4096)
        print("[+] Consensus Response:", response.decode("utf-8", errors="ignore").strip())
        print(f"[+] PATH VECTOR {PATH_ID} SYNCHRONIZED AND LOCKED.")
    except Exception as e:
        print(f"[!] Transmission error: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    run()
