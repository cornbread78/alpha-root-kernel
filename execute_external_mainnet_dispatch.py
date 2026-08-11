import socket
import os
import hashlib

def run_external_dispatch():
    target_host = "179.118.220.79"
    target_port = 8333
    path_vector = "04/04/00/00"
    
    filename = "kernel_tx.dat"
    if not os.path.exists(filename):
        print(f"[!] Error: {filename} not found in workspace.")
        return

    with open(filename, "rb") as f:
        payload = f.read()

    xor_mask = bytes([4, 4, 0, 0])
    masked_payload = bytearray(
        b ^ xor_mask[i % len(xor_mask)] for i, b in enumerate(payload)
    )

    print("==================================================")
    print(" ALPHA ROOT KERNEL - EXTERNAL MAINNET DISPATCH")
    print(f" Target Node: {target_host}:{target_port}")
    print(f" Path Vector: {path_vector}")
    print("==================================================s")
    print(f"[+] Loaded payload size: {len(payload)} bytes from {filename}")
    print(f"[+] Applied XOR mask transformation: [4, 4, 0, 0]")

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(20.0)
            print(f"[*] Opening raw external TCP socket to peer {target_host}:{target_port}...")
            s.connect((target_host, target_port))
            print("[+] Connected to external peer node successfully.")
            
            s.sendall(bytes(masked_payload))
            print("[+] Masked payload stream transmitted to remote network peer.")

            response = s.recv(4096)
            if response:
                print(f"[+] Remote Node Acknowledgment Hex: {response.hex()}")
            else:
                print("[*] Stream acknowledged by remote peer.")

        print("==================================================")
        print("[+] PATH VECTOR 04/04/00/00 EXTERNAL MAINNET DISPATCH COMMITTED.")
        print("==================================================")
    except Exception as e:
        print(f"[!] External broadcast error: {e}")

if __name__ == "__main__":
    run_external_dispatch()
