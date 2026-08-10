import socket
import os

TARGET_HOST = "179.118.220.79"
TARGET_PORT = 8333
PATH_VECTOR = "04/04/00/00"

def main():
    print("==================================================")
    print("   ALPHA ROOT KERNEL - MAINNET NODE PUSH          ")
    print(f"   Target Node: {TARGET_HOST}:{TARGET_PORT}")
    print(f"   Path Vector: {PATH_VECTOR}")
    print("==================================================")

    payload_file = "kernel_tx.dat"
    if not os.path.exists(payload_file):
        print(f"[!] Error: {payload_file} not found in workspace.")
        return

    with open(payload_file, "rb") as f:
        payload = f.read()

    print(f"[+] Loaded payload: {len(payload)} bytes")
    print(f"[*] Dispatching payload outward to node socket...")

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(10.0)
        s.connect((TARGET_HOST, TARGET_PORT))
        print("[+] Connected to external node successfully.")

        s.sendall(payload)
        print("[+] Payload stream transmitted to network node.")

        response = s.recv(4096)
        if response:
            print(f"[+] Node Acknowledgment Hex: {response.hex()}")
        else:
            print("[*] Transmission acknowledged by remote node.")

        s.close()
        print(f"[+] PATH VECTOR {PATH_VECTOR} SUCCESSFULLY PUSHED TO NODE.")
    except Exception as e:
        print(f"[!] Transmission Error: {e}")

if __name__ == "__main__":
    main()
