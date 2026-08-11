import socket

def run():
    target_ip = "179.118.220.79"
    target_port = 8333
    
    with open("kernel_tx.dat", "rb") as f:
        payload = bytearray(f.read())

    xor_mask = bytes([0x04, 0x04, 0x00, 0x00])
    for i in range(len(payload)):
        payload[i] ^= xor_mask[i % len(xor_mask)]

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((target_ip, target_port))
    sock.sendall(payload)
    response = sock.recv(4096)
    sock.close()

    print(response.hex())

if __name__ == "__main__":
    run()
