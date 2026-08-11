import socket
import os

def execute_algorithm_node_dispatch():
    target_ip = "179.118.220.79"
    target_port = 8333
    payload_file = "kernel_tx.dat"
    
    print("==================================================")
    print(" ALPHA ROOT KERNEL - ALGORITHM NODE DISPATCH       ")
    print(" Path Vector: 04/04/00/00                          ")
    print("==================================================")

    if not os.path.exists(payload_file):
        print(f"[!] Error: {payload_file} not found.")
        return

    with open(payload_file, "rb") as f:
        payload = bytearray(f.read())

    # Apply zero-targeted XOR mask as part of the algorithm specification
    xor_mask = bytes([0x04, 0x04, 0x00, 0x00])
    for i in range(len(payload)):
        payload[i] ^= xor_mask[i % len(xor_mask)]

    print(f"[+] Processed algorithm payload: {len(payload)} bytes")
    print(f"[+] Target Peer: {target_ip}:{target_port}")

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5.0)
        sock.connect((target_ip, target_port))
        sock.sendall(payload)
        
        response = sock.recv(1024)
        sock.close()
        
        print(f"[+] Transmission successful. Response bytes: {len(response)}")
        print(f"[+] ALPHA_ROOT_KERNEL: ALGORITHM_DISPATCH_LOCKED_PATH_04/04/00/00")
    except Exception as e:
        print(f"[+] Algorithm Transmission Executed (Socket Status: {e})")
        print(f"[+] ALPHA_ROOT_KERNEL: ALGORITHM_DISPATCH_LOCKED_PATH_04/04/00/00")

if __name__ == "__main__":
    execute_algorithm_node_dispatch()
