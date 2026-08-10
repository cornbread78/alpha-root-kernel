import json
import socket
import os
import sys
from merkle_tree import compute_merkle_root

def broadcast_consensus_block(port=9000):
    block_file = 'block_0.dat'
    state_file = 'chain_state.json'

    if not os.path.exists(block_file) or not os.path.exists(state_file):
        print("[FAIL] Missing ledger or state files.")
        return

    # 1. Load chain state
    with open(state_file, 'r') as f:
        state = json.load(f)

    # 2. Load transactions & compute Merkle Root
    with open(block_file, 'r') as f:
        txs = [line.strip() for line in f if line.strip()]

    merkle_root = compute_merkle_root(txs)

    # 3. Formulate Block Consensus Packet
    block_packet = f"BLOCK:{state['height']}|{state['prev_hash']}|{merkle_root}|{state['last_updated']}"

    print(f"\n--- BROADCASTING CONSENSUS BLOCK ---")
    print(f"Height:      {state['height']}")
    print(f"Prev Hash:   {state['prev_hash']}")
    print(f"Merkle Root: {merkle_root}")
    print(f"Packet:      {block_packet}\n")

    # 4. Transmit packet to local P2P daemon node
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('127.0.0.1', port))
        s.send((block_packet + '\n').encode('utf-8'))
        s.close()
        print(f"[SUCCESS] Consensus packet broadcasted to peer node on port {port}")
    except Exception as e:
        print(f"[FAIL] Could not reach node on port {port}: {e}")

if __name__ == "__main__":
    target_port = int(sys.argv[1]) if len(sys.argv) > 1 else 9000
    broadcast_consensus_block(target_port)
