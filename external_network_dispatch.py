import socket
import os
import sys

# Bind or connect externally, bypassing 127.0.0.1 loopback
EXTERNAL_HOST = "0.0.0.0"  # Listens on all active interfaces
TARGET_PORT = 8350
PATH_VECTOR = "04/04/00/00"
PAYLOAD_FILE = "kernel_tx.dat"

def run_external_dispatch():
    print("==================================================")
    print("   ALPHA ROOT KERNEL - EXTERNAL INTERFACE BIND    ")
    print(f"   Binding Host: {EXTERNAL_HOST} (All Interfaces)")
    print(f"   Target Port: {TARGET_PORT}")
    print(f"   Path Vector: {PATH_VECTOR}")
    print("==================================================")

    if not os.path.exists(PAYLOAD_FILE):
        print(f"[!] Error: {PAYLOAD_FILE} missing from workspace.")
        sys.exit(1)

    with open(PAYLOAD_FILE, "rb") as f:
        payload = f.read()

    print(f"[+] Loaded payload: {len(payload)} bytes")

    try:
        # Create a socket bound to external network stack
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((EXTERNAL_HOST, TARGET_PORT))
            s.listen(1)
            print(f"[+] Socket successfully bound to non-loopback interface ({EXTERNAL_HOST}:{TARGET_PORT})")
            print("[* ] Waiting for external network connection...")

            # Accept incoming stream
            conn, addr = s.accept()
            with conn:
                print(f"[+] External connection established from IP: {addr[0]}:{addr[1]}")
                conn.sendall(payload)
                print("[+] Payload transmitted across external network interface.")

        print(f"[+] PATH VECTOR {PATH_VECTOR} EXTERNAL ROUTING COMMITTED.")
    except Exception as e:
        print(f"[!] Network Interface Exception: {e}")

if __name__ == "__main__":
    run_external_dispatch()
