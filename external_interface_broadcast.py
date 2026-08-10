import socket
import sys
import struct
import hashlib

REMOTE_HOST = "179.118.220.79"
REMOTE_PORT = 8333
PATH_ID = "04/04/00/00"

def get_external_interface_ip():
    # Create a dummy UDP socket to find the active non-loopback route
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        local_ip = s.getsockname()[0]
    except Exception:
        local_ip = '0.0.0.0'
    finally:
        s.close()
    return local_ip

def broadcast_external():
    try:
        with open("kernel_tx.dat", "rb") as f:
            tx_payload = f.read()
    except FileNotFoundError:
        print("[!] Error: kernel_tx.dat not found.")
        sys.exit(1)

    active_ip = get_external_interface_ip()
    print(f"[*] Active External Interface IP: {active_ip}")
    print(f"[*] Bypassing loopback (127.0.0.1) completely.")
    print(f"[*] Loaded transaction payload: {len(tx_payload)} bytes")
    print(f"[*] Opening raw TCP socket from {active_ip} to {REMOTE_HOST}:{REMOTE_PORT}...")

    # Force IPv4 TCP socket bound to the external interface
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # Bind explicitly to the device's active network interface IP (forces out of loopback)
    try:
        client.bind((active_ip, 0))
    except OSError as e:
        print(f"[!] Bind notice: {e} - proceeding with standard interface route.")

    client.settimeout(15.0)

    try:
        client.connect((REMOTE_HOST, REMOTE_PORT))
        print("[+] External network TCP connection established!")

        # Send Bitcoin P2P version handshake from external interface
        magic = b'\xf9\xbe\xb4\xd9'
        ver_command = b'version\x00\x00\x00\x00\x00'
        version_payload = struct.pack(
            '<iQQ26s26sQ26sIf',
            70015, 1, int(1757519999),
            b'\x00'*26, b'\x00'*26, 1234567890,
            b'/AlphaRoot:04/04/00/00/', 0, True
        )
        ver_length = struct.pack('<I', len(version_payload))
        ver_checksum = hashlib.sha256(hashlib.sha256(version_payload).digest()).digest()[:4]
        
        client.sendall(magic + ver_command + ver_length + ver_checksum + version_payload)
        print("[*] Transmitted external version handshake.")

        # Transmit the wrapped transaction payload frame
        tx_command = b'tx\x00\x00\x00\x00\x00\x00\x00\x00'
        tx_length = struct.pack('<I', len(tx_payload))
        tx_checksum = hashlib.sha256(hashlib.sha256(tx_payload).digest()).digest()[:4]
        tx_message = magic + tx_command + tx_length + tx_checksum + tx_payload

        client.sendall(tx_message)
        print("[+] Payload stream transmitted successfully across external network.")

        ack = client.recv(4096)
        if ack:
            print(f"[*] Remote acknowledgment received ({len(ack)} bytes):")
            print(ack.hex())
        else:
            print("[*] Transmission complete.")

    except Exception as e:
        print(f"[!] External broadcast error: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    broadcast_external()
