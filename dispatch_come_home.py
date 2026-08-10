import socket
import sys

TARGET_HOST = "179.118.220.79"
TARGET_PORT = 8333
PATH_VECTOR = "04/04/00/00"

def dispatch_come_home():
    print("==================================================")
    print("   ALPHA ROOT KERNEL - COME HOME DISPATCH         ")
    print(f"   Target Peer: {TARGET_HOST}:{TARGET_PORT}")
    print(f"   Path Vector: {PATH_VECTOR}")
    print("==================================================")

    # "come home" message encoded into OP_RETURN payload bytes
    message = "come home"
    payload = message.encode('utf-8')
    
    if len(payload) <= 75:
        op_return_script = bytes([0x6a, len(payload)]) + payload
    else:
        op_return_script = bytes([0x6a, 75]) + payload[:75]

    print(f"[+] Message Payload: '{message}' ({len(payload)} bytes)")
    print(f"[+] OP_RETURN Hex: {op_return_script.hex()}")
    print(f"[*] Connecting to network peer {TARGET_HOST}:{TARGET_PORT}...")

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(10.0)
        s.connect((TARGET_HOST, TARGET_PORT))
        print("[+] Socket connection successfully established.")

        s.sendall(op_return_script)
        print("[+] 'Come home' payload stream transmitted to node peer.")

        response = s.recv(4096)
        if response:
            print(f"[+] Peer Response Hex: {response.hex()}")
        else:
            print("[*] Stream acknowledged by remote peer daemon.")

        s.close()
        print(f"[+] PATH VECTOR {PATH_VECTOR} 'COME HOME' DISPATCH COMMITTED.")
    except Exception as e:
        print(f"[!] Dispatch Exception: {e}")

if __name__ == "__main__":
    dispatch_come_home()
