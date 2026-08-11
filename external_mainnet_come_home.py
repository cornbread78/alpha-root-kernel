import os
import socket

def external_dispatch():
    print("==================================================")
    print(" ALPHA ROOT KERNEL - EXTERNAL MAINNET DISPATCH")
    print(" Target Node: 179.118.220.79:8333")
    print(" Path Vector: 04/04/00/00")
    print("==================================================")

    target_host = "179.118.220.79"
    target_port = 8333
    xor_mask = bytes([0x04, 0x04, 0x00, 0x00])
    
    # "come home" protocol message wrapped in OP_RETURN format
    message = b"come home"
    op_return_script = bytes([0x6a, len(message)]) + message
    print(f"[+] Message Payload: {message}")
    print(f"[+] OP_RETURN Hex: {op_return_script.hex()}")

    # Check for payload file or fallback to OP_RETURN script
    payload_file = "kernel_tx.dat"
    if os.path.exists(payload_file):
        with open(payload_file, "rb") as f:
            raw_data = f.read()
        print(f"[+] Loaded payload size: {len(raw_data)} bytes from {payload_file}")
        masked_data = bytearray(raw_data)
    else:
        print("[*] Local payload file not found, using compiled OP_RETURN frame.")
        masked_data = bytearray(op_return_script)

    # Apply XOR mask transformation
    for i in range(len(masked_data)):
        masked_data[i] ^= xor_mask[i % len(xor_mask)]
    print(f"[+] Applied XOR mask transformation: {list(xor_mask)}")

    print(f"[*] Opening raw external TCP socket to peer {target_host}:{target_port}...")
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(10.0)
        s.connect((target_host, target_port))
        print("[+] Connected to external peer node successfully.")

        s.sendall(bytes(masked_data))
        print("[+] Masked payload stream transmitted to remote network peer.")

        response = s.recv(4096)
        if response:
            print(f"[+] Remote Node Acknowledgment Hex: {response.hex()}")
        else:
            print("[*] Stream acknowledged by remote peer daemon.")

        s.close()
        print("[+] PATH VECTOR 04/04/00/00 EXTERNAL DISPATCH COMMITTED.")
    except Exception as e:
        print(f"[!] External Dispatch Exception: {e}")

if __name__ == "__main__":
    external_dispatch()
