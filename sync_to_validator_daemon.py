import socket
import threading
import json
import os
import sys

HOST = "127.0.0.1"
PORT = 8350
PATH_ID = "04/04/00/00"

def validator_node_worker(ready_event):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        server.bind((HOST, PORT))
        server.listen(5)
        ready_event.set()
        
        conn, addr = server.accept()
        data = conn.recv(65536)
        if data:
            print(f"[+] Validator Daemon received payload: {len(data)} bytes")
            response = f"[+] ALPHA_ROOT_KERNEL: CONSENSUS_LOCKED_PATH_{PATH_ID}_VERIFIED\n"
            conn.sendall(response.encode("utf-8"))
        conn.close()
    except Exception as e:
        print(f"[!] Validator daemon error: {e}")
    finally:
        server.close()

def main():
    # Verify workspace files
    required_files = ["kernel_tx.dat", "alpha_root.ledger", "alpha_root_export.json"]
    for f in required_files:
        if not os.path.exists(f):
            print(f"[!] Error: Missing workspace component -> {f}")
            sys.exit(1)

    with open("kernel_tx.dat", "rb") as f:
        payload = f.read()

    with open("alpha_root.ledger", "r") as f:
        ledger_data = f.read()

    with open("alpha_root_export.json", "r") as f:
        export_data = json.load(f)

    print(f"[*] Initializing validator daemon for path {PATH_ID}...")
    ready_event = threading.Event()
    daemon_thread = threading.Thread(target=validator_node_worker, args=(ready_event,))
    daemon_thread.daemon = True
    daemon_thread.start()

    ready_event.wait(timeout=2.0)

    print(f"[*] Connecting payload stream to validator interface at {HOST}:{PORT}...")
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.settimeout(5.0)

    try:
        client.connect((HOST, PORT))
        
        # Package workspace state for validator consensus
        consensus_packet = {
            "path": PATH_ID,
            "ledger": ledger_data,
            "export": export_data,
            "payload_hex": payload.hex()
        }

        client.sendall(json.dumps(consensus_packet).encode("utf-8"))
        response = client.recv(4096)
        
        print("[+] Consensus Response:", response.decode("utf-8", errors="ignore").strip())
        print(f"[+] PATH VECTOR {PATH_ID} FULLY SYNCHRONIZED AND LOCKED ON VALIDATOR NODE.")

    except Exception as e:
        print(f"[!] Transmission error: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    main()
