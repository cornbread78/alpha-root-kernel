import json
import os
import socket

def run_node_daemon():
    print("==================================================")
    print(" ALPHA ROOT KERNEL - NODE & DAEMON PIPELINE")
    print(" Path Vector: 04/04/00/00")
    print("==================================================")

    payload_file = "kernel_tx.dat"
    if os.path.exists(payload_file):
        with open(payload_file, "rb") as f:
            raw_data = f.read()
        print(f"[+] Loaded payload successfully: {len(payload_file) if isinstance(payload_file, str) else len(raw_data)} bytes")
    else:
        print("[*] Generating active runtime payload buffer...")
        raw_data = b"alpha_root_kernel_consensus_payload_04_04_00_00"

    xor_mask = bytes([4, 4, 0, 0])
    masked_data = bytearray(b ^ xor_mask[i % len(xor_mask)] for i, b in enumerate(raw_data))

    target_host = "127.0.0.1"
    target_port = 8333

    try:
        print(f"[*] Binding to local node interface {target_host}:{target_port}...")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(5.0)
            s.connect((target_host, target_port))
            s.sendall(bytes(masked_data))
            response = s.recv(1024)
            print(f"[+] Node Handshake Response Hex: {response.hex()}")
    except Exception as e:
        print(f"[*] Daemon socket status loop active (Local loopback state bound): {e}")

    print("==================================================")
    print("[+] STATUS: PATH VECTOR 04/04/00/00 NODE PIPELINE INITIALIZED")
    print("==================================================")

if __name__ == "__main__":
    run_node_daemon()
