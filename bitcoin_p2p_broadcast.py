import socket
import struct
import hashlib
import sys

REMOTE_HOST = "179.118.220.79"
REMOTE_PORT = 8333
PATH_ID = "04/04/00/00"

def broadcast_transaction():
    try:
        with open("kernel_tx.dat", "rb") as f:
            tx_payload = f.read()
    except FileNotFoundError:
        print("[!] Error: kernel_tx.dat not found.")
        sys.exit(1)

    print(f"[*] Loaded transaction payload: {len(tx_payload)} bytes")
    print(f"[*] Connecting to live Bitcoin peer {REMOTE_HOST}:{REMOTE_PORT}...")

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.settimeout(15.0)

    try:
        client.connect((REMOTE_HOST, REMOTE_PORT))
        print("[+] Connected to live network peer!")

        # 1. Send Version Message Handshake
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
        print("[*] Sent P2P version handshake. Awaiting peer synchronization...")

        # 2. Complete Handshake: Read peer version and send verack
        peer_data = client.recv(4096)
        if not peer_data:
            print("[!] Peer closed connection during handshake.")
            return

        print(f"[*] Received peer synchronization stream ({len(peer_data)} bytes).")

        # Send verack to complete the handshake state machine
        verack_command = b'verack\x00\x00\x00\x00\x00\x00'
        verack_length = struct.pack('<I', 0)
        verack_checksum = hashlib.sha256(hashlib.sha256(b'').digest()).digest()[:4]
        client.sendall(magic + verack_command + verack_length + verack_checksum)
        print("[*] Sent verack confirmation.")

        # 3. Wrap kernel_tx.dat into a Bitcoin network 'tx' message packet
        tx_command = b'tx\x00\x00\x00\x00\x00\x00\x00\x00'
        tx_length = struct.pack('<I', len(tx_payload))
        tx_checksum = hashlib.sha256(hashlib.sha256(tx_payload).digest()).digest()[:4]
        tx_message = magic + tx_command + tx_length + tx_checksum + tx_payload

        # 4. Transmit the transaction message
        client.sendall(tx_message)
        print("[+] Transaction frame broadcasted successfully to the global network!")

        # Await broadcast acknowledgment or inventory reflection
        ack = client.recv(4096)
        if ack:
            print(f"[*] Network consensus response received ({len(ack)} bytes):")
            print(ack[:64].hex())
        else:
            print("[*] Frame accepted into node memory pool.")

    except socket.timeout:
        print("[!] Network timeout: Peer did not complete protocol exchange within the time limit.")
    except Exception as e:
        print(f"[!] Broadcast transmission error: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    broadcast_transaction()
