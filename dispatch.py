import socket
import os

def main():
    filename = "kernel_tx.dat"
    xor_mask = bytes([0x04, 0x04, 0x00, 0x00])
    host = "179.118.220.79"
    port = 8333

    if os.path.exists(filename):
        with open(filename, "rb") as f:
            raw_data = f.read()
    else:
        raw_data = b"\x01\x00\x00\x00\x01" + (b"\x00" * 32) + b"\x00\x00\x00\x00"

    masked_data = bytearray()
    for i, byte in enumerate(raw_data):
        if byte == 0x00:
            masked_data.append(xor_mask[i % len(xor_mask)])
        else:
            masked_data.append(byte)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(10.0)
        s.connect((host, port))
        s.sendall(bytes(masked_data))
        response = s.recv(4096)
        print(response.hex())

if __name__ == "__main__":
    main()
