import socket
import json
import os
import sys

HOST = "127.0.0.1"
PORT = 8332
PATH_ID = "04/04/00/00"

def send_http_rpc():
    if not os.path.exists("kernel_tx.dat"):
        print("[!] Error: kernel_tx.dat missing.")
        sys.exit(1)

    with open("kernel_tx.dat", "rb") as f:
        raw_payload = f.read()

    rpc_payload = {
        "jsonrpc": "1.0",
        "id": "alpha_sync",
        "method": "sendrawtransaction",
        "params": [raw_payload.hex()]
    }
    
    body = json.dumps(rpc_payload)
    
    # Construct proper HTTP POST request headers required by the node daemon
    headers = [
        "POST / HTTP/1.1",
        f"Host: {HOST}:{PORT}",
        "Content-Type: application/json",
        f"Content-Length: {len(body)}",
        "Connection: close",
        ""
    ]
    
    http_request = "\r\n".join(headers) + "\r\n" + body

    print(f"[*] Connecting to HTTP JSON-RPC node daemon at {HOST}:{PORT}...")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(10.0)

    try:
        s.connect((HOST, PORT))
        s.sendall(http_request.encode("utf-8"))
        
        response = s.recv(65536)
        if response:
            print("[+] Node Daemon HTTP Response:")
            print(response.decode("utf-8", errors="ignore"))
        else:
            print("[+] Transmission completed with empty response.")
    except Exception as e:
        print(f"[!] Bridge error: {e}")
    finally:
        s.close()

if __name__ == "__main__":
    send_http_rpc()
