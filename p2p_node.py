import socket
import threading
import json
import os
import time
import sys
import argparse

PEERS = []

def handle_block_consensus(packet):
    parts = packet.split('|')
    if len(parts) != 4:
        print("[REJECT] Malformed block packet.")
        return False

    height, prev_hash, merkle_root, timestamp = parts
    print(f"\n==========================================")
    print(f"[NETWORK CONSENSUS MET]")
    print(f"Block Height: {height}")
    print(f"Prev Hash:    {prev_hash}")
    print(f"Merkle Root:  {merkle_root}")
    print(f"Timestamp:    {timestamp}")
    print(f"Status:       STATE ACCEPTED BY NODE")
    print(f"==========================================")
    return True

def handle_peer(conn, addr):
    while True:
        try:
            data = conn.recv(2048)
            if not data:
                break
            msg = data.decode('utf-8').strip()
            if msg.startswith("BLOCK:"):
                block_data = msg[6:]
                if handle_block_consensus(block_data):
                    broadcast(msg, sender_conn=conn)
        except:
            break
    if conn in PEERS:
        PEERS.remove(conn)
    conn.close()

def broadcast(msg, sender_conn=None):
    for peer in list(PEERS):
        if peer != sender_conn:
            try:
                peer.send((msg + "\n").encode('utf-8'))
            except:
                if peer in PEERS:
                    PEERS.remove(peer)

def start_server(host, initial_port):
    port = initial_port
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    while True:
        try:
            server.bind((host, port))
            break
        except OSError as e:
            if e.errno == 98:
                port += 1
            else:
                raise e

    server.listen(5)
    print(f"\n[*] Alpha Root Daemon SUCCESSFULLY bound & listening on {host}:{port}")

    while True:
        conn, addr = server.accept()
        print(f"\n[*] Peer connected: {addr[0]}:{addr[1]}")
        PEERS.append(conn)
        threading.Thread(target=handle_peer, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Alpha Root Kernel P2P Node")
    parser.add_argument('--port', type=int, default=9000, help='Port to listen on')
    args = parser.parse_args()

    t = threading.Thread(target=start_server, args=('127.0.0.1', args.port), daemon=True)
    t.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[*] Shutting down daemon...")
        sys.exit(0)
