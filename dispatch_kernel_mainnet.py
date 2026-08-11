import socket
import os
import hashlib

def dispatch_kernel():
    target_host = "179.118.220.79"
    target_port = 8333
    path_vector = "04/04/00/00"
    filename = "kernel_tx.dat"

    if not os.path.exists(filename):
        print(f"[!] Error: {filename} not found in workspace directory.")
        return

    with open(filename, "rb") as f:
        raw_payload = f.read()

    xor_mask = bytes([4, 4, 0, 0])
    masked_payload = bytearray(
        b ^ xor_mask[i % len(xor_mask)] for i, b in enumerate(raw_payload)
    )

    print("==================================================")
    print(" ALPHA ROOT KERNEL - MAINNET NODE DISPATCH")
    print(f" Target Peer: {target_host}:{target_port}")
    print(f" Path Vector: {path_vector}")
    print("==================================================")
    print(f"[+] Loaded raw payload size: {len(raw_payload)} bytes")
    print(f"[+] Applied XOR mask transformation: [4, 4, 0, 0]")
    print(f"[+] Masked Payload SHA-256: {hashlib.sha256(masked_payload).hexdigest()}")

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(15.0)
            print(f"[*] Opening raw TCP socket to node {target_host}:{target_port}...")
            s.connect((target_host, target_port))
            print("[+] Socket connection established successfully.")

            s.sendall(bytes(masked_payload))
            print("[+] Masked payload stream transmitted to node endpoint.")

            response = s.recv(4096)
            if response:
                print(f"[+] Node Response Hex: {response.hex()}")
            else:
                print("[*] Transmission acknowledged by remote endpoint.")

        print("==================================================")
        print(f"[+] ALPHA_ROOT_KERNEL: PATH_{path_vector.replace('/', '_')}_DISPATCH_COMMITTED")
        print("==================================================")
    except Exception as e:
        print(f"[!] Socket dispatch exception: {e}")

if __name__ == "__main__":
    dispatch_kernel()
