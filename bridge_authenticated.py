import socket
import json
import os
import sys
import base64

HOST = "127.0.0.1"
PORT = 8332
PATH_ID = "04/04/00/00"

def find_cookie():
    paths = [
        os.path.expanduser("~/.bitcoin/.cookie"),
        os.path.expanduser("~/.bitcoin/regtest/.cookie"),
        os.path.expanduser("~/.bitcoin/testnet3/.cookie"),
    ]
    for p in paths:
        if os.path.exists(p):
            with open(p, "r") as f:
                return f.read().strip()
    return None

def send_authenticated_rpc():
    if not os.path.exists("kernel_tx.dat"):
        print("[!] Error: kernel_tx.dat missing.")
        sys.exit(1)

    with open("kernel_tx.dat", "rb") as f:
        raw_payload = f.read()

    cookie = find_cookie()
    if cookie:
        print("[*] Detected local node session cookie.")
        auth_str = cookie
    else:
        print("[*] Using default local RPC credentials.")
        auth_str = "rpcuser:rpcpassword"

    auth_header = base64.b64encode(auth_str.encode("utf-8")).decode("utf-8")

    rpc_payload = {
        "jsonrpc": "1.0",
        "id": "genesis_consensus",
        "method": "sendrawtransaction",
        "params": [raw_payload.hex()]
    }
    
    body = json.dumps(rpc_payload)
    
    headers = [
        "POST / HTTP/1.1",
        f"Host: {HOST}:{PORT}",
        "Content-Type: application/json",
        f"Authorization: Basic {auth_header}",
        f"Content-Length: {len(body)}",
        "Connection: close",
        ""
    ]
    
    http_request = "\r\n".join(headers) + "\r\n" + body

    print(f"[*] Connecting to authenticated node daemon at {HOST}:{PORT}...")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(10.0)

    try:
        s.connect((HOST, PORT))
        s.sendall(http_request.encode("utf-8"))
        
        response = s.recv(65536)
        if response:
            print("[+] Node Daemon Response:")
            print(response.decode("utf-8", errors="ignore"))
        else:
            print("[+] Transmission completed.")
    except Exception as e:
        print(f"[!] Bridge error: {e}")
    finally:
        s.close()

if __name__ == "__main__":
    send_authenticated_rpc()
