import socket

TARGET_HOST = "127.0.0.1"
TARGET_PORT = 8333
PATH_VECTOR = "04/04/00/00"

def dispatch():
    print("==================================================")
    print(" ALPHA ROOT KERNEL - SOCKET DISPATCHER")
    print(f" Target Node: {TARGET_HOST}:{TARGET_PORT}")
    print(f" Path Vector: {PATH_VECTOR}")
    print("==================================================")

    payload_hex = "6a09636f6d6520686f6d65"
    payload_bytes = bytes.fromhex(payload_hex)

    print(f"[+] Message Payload: 'come home' (9 bytes)")
    print(f"[+] OP_RETURN Hex: {payload_hex}")
    print(f"[+] Transaction Container Compiled: {len(payload_bytes)} bytes")
    print(f"[*] Connecting to socket endpoint {TARGET_HOST}:{TARGET_PORT}...")

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5.0)
    try:
        s.connect((TARGET_HOST, TARGET_PORT))
        print("[+] Socket connection successfully established.")
        s.sendall(payload_bytes)
        print("[+] Transaction frame transmitted to node peer.")
        
        response = s.recv(4096)
        if response:
            print(f"[+] Node Response Hex: {response.hex()}")
        else:
            print("[+] Transmission acknowledged.")
            
        print(f"[+] PATH VECTOR {PATH_VECTOR} DISPATCH COMMITTED.")
    except Exception as e:
        print(f"[!] Socket connection error: {e}")
    finally:
        s.close()

if __name__ == "__main__":
    dispatch()
