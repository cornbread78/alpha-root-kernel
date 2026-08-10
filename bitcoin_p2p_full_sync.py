import socket
import struct
import hashlib
import sys
import select

REMOTE_HOST = "179.118.220.79"
REMOTE_PORT = 8333
PATH_ID = "04/04/00/00"

def run_sync_broadcast():
    try:
        with open("kernel_tx.dat", "rb") as f:
            tx_payload = f.read()
    except FileNotFoundError:
        print("[!] Error: kernel_tx.dat not found.")
        sys.exit(1)

    print(f"[*] Loaded transaction payload: {len(tx_payload)} bytes")
    print(f"[*] Connecting to live Bitcoin peer {REMOTE_HOST}:{REMOTE_PORT}...")

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.settimeout(10.0)

    try:
        client.connect((REMOTE_HOST, REMOTE_PORT))
        print("[+] Connected to live network peer!")

        # 1. Send our version message
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
        print("[*] Sent version handshake. Listening for peer response stream...")

        # 2. Read incoming messages from peer (version, verack, etc.) using select
        buffer = b''
        while True:
            r, _, _ = select.select([client], [], [], 5.0)
            if not r:
                print("[!] Timeout waiting for peer stream response.")
                break
            chunk = client.recv(4096)
            if not chunk:
                print("[!] Peer closed connection.")
                break
            buffer += chunk
            print(f"[+] Received chunk: {len(chunk)} bytes (Total buffer: {len(buffer)} bytes)")
            
            if len(buffer) >= 24:
                break

        # 3. Send verack back to the peer
        verack_command = b'verack\x00\x00\x00\x00\x00\x00'
        verack_length = struct.pack('<I', 0)
        verack_checksum = hashlib.sha256(hashlib.sha256(b'').digest()).digest()[:4]
        client.sendall(magic + verack_command + verack_length + verack_checksum)
        print("[*] Sent verack confirmation response.")

        # 4. Wrap and send our transaction payload ('tx')
        tx_command = b'tx\x00\x00\x00\x00\x00\x00\x00\x00'
        tx_length = struct.pack('<I', len(tx_payload))
        tx_checksum = hashlib.sha256(hashlib.sha256(tx_payload).digest()).digest()[:4]
        tx_message = magic + tx_command + tx_length + tx_checksum + tx_payload

        client.sendall(tx_message)
        print("[+] Transaction frame injected into live peer socket stream!")

        # 5. Listen for final node acknowledgment or rejection
        client.settimeout(5.0)
        try:
            ack = client.recv(4096)
            if ack:
                print(f"[+] Peer reaction received ({len(ack)} bytes): {ack[:64].hex()}")
            else:
                print("[*] Stream acknowledged.")
        except socket.timeout:
            print("[*] Broadcast transmission cycle completed.")

    except Exception as e:
        print(f"[!] Protocol error: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    run_sync_broadcast()
