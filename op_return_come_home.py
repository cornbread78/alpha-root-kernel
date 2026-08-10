import os

def main():
    print("==================================================")
    print("   ALPHA ROOT KERNEL - OP_RETURN COME HOME        ")
    print("   Path Vector: 04/04/00/00                       ")
    print("==================================================")
    
    # Target payload message
    message = "come home"
    payload = message.encode('utf-8')

    print(f"[+] Loaded payload message: '{message}' ({len(payload)} bytes)")

    # Constructing OP_RETURN data carrier structure
    if len(payload) <= 75:
        script_pub_key = bytes([0x6a, len(payload)]) + payload
    elif len(payload) <= 255:
        script_pub_key = bytes([0x6a, 0x4c, len(payload)]) + payload
    else:
        truncated = payload[:80]
        script_pub_key = bytes([0x6a, len(truncated)]) + truncated

    print(f"[+] OP_RETURN Script Hex: {script_pub_key.hex()}")
    print("[+] Path vector 04/04/00/00 'come home' frame compiled successfully.")

if __name__ == "__main__":
    main()
