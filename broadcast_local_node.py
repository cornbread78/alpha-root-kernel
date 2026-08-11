import os
import socket

LOCAL_HOST = "127.0.0.1"
LOCAL_PORT = 8350
FRAME_FILE = "final_mainnet_frame.hex"
FALLBACK_FILE = "kernel_tx.dat"

def broadcast_to_local_node():
    print("==================================================")
    print("   ALPHA ROOT KERNEL - LOCAL NODE DISPATCH        ")
    print(f"   Target: {LOCAL_HOST}:{LOCAL_PORT}")
    print("==================================================")

    target_file = FRAME_FILE if os.path.exists(FRAME_FILE) else FALLBACK_FILE
    if not os.path.exists(target_file):
        print(f"[!] Error: Neither {FRAME_FILE} nor {FALLBACK_FILE} found in workspace.")
        return

    with open(target_file, "rb") as f:
        payload = f.read()

    print(f"[+] Loaded payload size: {len(payload)} bytes from {target_file}")
    print(f"[*] Connecting to local node interface {LOCAL_HOST}:{LOCAL_PORT}...")

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(10.0)
            s.connect((LOCAL_HOST, LOCAL_PORT))
            print("[+] Connected to local node socket successfully.")

            s.sendall(payload)
            print("[+] Payload stream successfully transmitted to local node.")

            response = s.recv(4096)
            if response:
                print(f"[+] Local Node Response Hex: {response.hex()}")
                print(f"[+] Local Node Response Text: {response.decode('utf-8', errors='ignore').strip()}")
            else:
                print("[*] Stream acknowledged by local node daemon.")

        print("[+] LOCAL NODE BROADCAST SEQUENCE COMMITTED.")
    except Exception as e:
        print(f"[!] Connection Exception: {e}")

if __name__ == "__main__":
    broadcast_to_local_node()
