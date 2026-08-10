import socket
import sys

TARGET_HOST = "179.118.220.79"
TARGET_PORT = 8333
PATH_VECTOR = "04/04/00/00"

def main():
    print("==================================================")
    print("   ALPHA ROOT KERNEL - DIRECT VECTOR DISPATCH     ")
    print(f"   Target Node: {TARGET_HOST}:{TARGET_PORT}")
    print(f"   Path Vector: {PATH_VECTOR}")
    print("==================================================")

    # Compile the OP_RETURN payload frame
    message = "come home"
    payload = message.encode('utf-8')
    
    if len(payload) <= 75:
        op_return_script = bytes([0x6a, len(payload)]) + payload
    else:
        op_return_script = bytes([0x6a, 75]) + payload[:75]

    print(f"[+] Message Payload: '{message}' ({len(payload)} bytes)")
    print(f"[+] OP_RETURN Hex: {op_return_script.hex()}")

    script_len_byte = bytes([len(op_return_script)])

    # Construct transaction container frame
    tx_frame = (
        b"\x01\x00\x00\x00" +  # Version 1
        b"\x01" +               # Input count: 1
        b"\x00" * 32 +          # Previous TxHash (Null outpoint)
        b"\x00\x00\x00\x00" +  # Output index
        b"\x00" +               # Empty scriptSig
        b"\xff\xff\xff\xff" +  # Sequence
        b"\x01" +               # Output count: 1
        b"\x00\x00\x00\x00\x00\x00\x00\x00" +  # Value: 0 satoshis
        script_len_byte +       # Script length byte
        op_return_script +      # OP_RETURN script
        b"\x00\x00\x00\x00"     # Locktime
    )

    print(f"[+] Transaction Container Compiled: {len(tx_frame)} bytes")
    print(f"[*] Connecting to socket endpoint...")

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(10.0)
        s.connect((TARGET_HOST, TARGET_PORT))
        print("[+] Socket connection successfully established.")

        s.sendall(tx_frame)
        print("[+] Payload frame transmitted successfully.")

        response = s.recv(4096)
        if response:
            print(f"[+] Endpoint Response Hex: {response.hex()}")
        else:
            print("[*] Stream acknowledged by remote endpoint.")

        s.close()
        print(f"[+] PATH VECTOR {PATH_VECTOR} TRANSMISSION COMMITTED.")
    except Exception as e:
        print(f"[!] Transmission Exception: {e}")

if __name__ == "__main__":
    main()
