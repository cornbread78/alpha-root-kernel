import os
import socket
import sys

def main():
    print("==================================================")
    print(" ALPHA ROOT KERNEL - MAINNET NODE SYNC DISPATCH")
    print(" Path Vector: 04/04/00/00")
    print("==================================================")

    target_host = "127.0.0.1"
    target_port = 8350
    xor_mask = bytes([0x04, 0x04, 0x00, 0x00])
    message = b"come home"

    # Construct OP_RETURN script format for the protocol
    op_return_script = bytes([0x6a, len(message)]) + message
    print(f"[+] Protocol Message Payload: {message}")
    print(f"[+] OP_RETURN Hex Structure: {op_return_script.hex()}")

    # Apply active XOR mask to the protocol payload
    masked_data = bytearray(op_return_script)
    for i in range(len(masked_data)):
        masked_data[i] ^= xor_mask[i % len(xor_mask)]
    print(f"[+] Applied XOR Mask: {list(xor_mask)}")

    print(f"[*] Connecting stream to active alpha route node at {target_host}:{target_port}...")
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(10.0)
        s.connect((target_host, target_port))
        print("[+] Socket connection successfully established.")

        s.sendall(bytes(masked_data))
        print("[+] XOR-masked protocol stream transmitted to node interface.")

        response = s.recv(4096)
        if response:
            print(f"[+] Node Acknowledgment / Consensus Hex: {response.hex()}")
            try:
                print(f"[+] Decoded Response: {response.decode('utf-8').strip()}")
            except Exception:
                pass
        else:
            print("[*] Stream acknowledged by remote node peer.")

        s.close()
        print("[+] PATH VECTOR 04/04/00/00 NODE SYNC COMMITTED.")
    except Exception as e:
        print(f"[!] Dispatch Error: {e}")

if __name__ == "__main__":
    main()
