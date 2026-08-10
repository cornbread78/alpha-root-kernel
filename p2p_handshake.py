import socket
import struct
import hashlib
import sys

PEER_IP = "179.118.220.79"
PORT = 8333
PATH_ID = "04/04/00/00"

def send_bitcoin_handshake():
    print(f"[*] Initializing Bitcoin P2P protocol handshake with {PEER_IP}:{PORT}...")
    
    # Mainnet Magic Bytes
    magic = b'\xf9\xbe\xb4\xd9'
    command = b'version\x00\x00\x00\x00\x00'
    
    # Version payload components: version, services, timestamp, addr_recv, addr_from, nonce, user_agent, starting_height, relay
    version_payload = struct.pack(
        '<iQQ26s26sQ26sIf',
        70015,                      # Protocol version
        1,                          # Services (NODE_NETWORK)
        int(1757519999),            # Timestamp
        b'\x00'*26,                 # Receiver address
        b'\x00'*26,                 # Sender address
        1234567890,                 # Nonce
        b'/AlphaRoot:04/04/00/00/', # User agent (variable length encoded simply here)
        0,                          # Starting height
        True                        # Relay
    )
    
    # Adjust payload length and compute checksum (double SHA256)
    length = struct.pack('<I', len(version_payload))
    checksum = hashlib.sha256(hashlib.sha256(version_payload).digest()).digest()[:4]
    
    message = magic + command + length + checksum + version_payload

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.settimeout(10.0)

    try:
        client.connect((PEER_IP, PORT))
        print("[+] Connected! Transmitting P2P version handshake...")
        client.sendall(message)
        
        response = client.recv(4096)
        if response:
            print(f"[+] Received P2P response from public node: {len(response)} bytes")
            print("[*] Hex response:", response[:64].hex())
        else:
            print("[*] Connection active, awaiting node response stream.")
    except Exception as e:
        print(f"[!] Handshake error: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    send_bitcoin_handshake()
