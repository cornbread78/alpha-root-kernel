import socket
import os

def main():
    print("==================================================")
    print(" ALPHA ROOT KERNEL - CLEAN 'COME HOME' DISPATCH")
    print(" Path Vector: 04/04/00/00")
    print("==================================================")

    target_host = "179.118.220.79"
    target_port = 8333
    xor_mask = bytes([0x04, 0x04, 0x00, 0x00])
    
    # Clean string payload without byte prefix notation
    message_str = "come home"
    message_bytes = message_str.encode('utf-8')

    op_return_script = bytes([0x6a, len(message_bytes)]) + message_bytes
    print(f"[+] Message Payload: {message_str}")
    print(f"[+] OP_RETURN Hex: {op_return_script.hex()}")

    masked_data = bytearray(op_return_script)
    for i in range(len(masked_data)):
        masked_data[i] ^= xor_mask[i % len(xor_mask)]
    print(f"[+] Applied XOR Mask: {list(xor_mask)}")

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(10.0)
        s.connect((target_host, target_port))
        print("[+] Connected to node socket successfully.")

        s.sendall(bytes(masked_data))
        print("[+] Clean stream transmitted to remote peer.")

        response = s.recv(4096)
        if response:
            print(f"[+] Peer Response Hex: {response.hex()}")
        else:
            print("[*] Stream acknowledged.")

        s.close()
        print("[+] PATH VECTOR 04/04/00/00 CLEAN DISPATCH COMMITTED.")
    except Exception as e:
        print(f"[!] Error: {e}")

if __name__ == "__main__":
    main()
