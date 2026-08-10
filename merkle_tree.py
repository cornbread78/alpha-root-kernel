import os
import hashlib

def compute_merkle_root(tx_lines):
    if not tx_lines:
        return None

    # Step 1: Compute initial hash for each raw hex transaction string
    current_level = [hashlib.sha256(tx.encode('utf-8')).digest() for tx in tx_lines]

    print("=== LEAF HASHES ===")
    for i, h in enumerate(current_level):
        print(f"TX [{i}]: {h.hex()}")
    print("===================\n")

    # Step 2: Build the tree upward layer by layer
    layer = 0
    while len(current_level) > 1:
        layer += 1
        # Duplicate last element if odd number of hashes
        if len(current_level) % 2 != 0:
            current_level.append(current_level[-1])

        next_level = []
        for i in range(0, len(current_level), 2):
            combined = current_level[i] + current_level[i+1]
            parent_hash = hashlib.sha256(combined).digest()
            next_level.append(parent_hash)
            
        current_level = next_level

    return current_level[0].hex()

def main():
    block_file = 'block_0.dat'
    
    if not os.path.exists(block_file):
        print("[FAIL] block_0.dat not found.")
        return

    with open(block_file, 'r') as f:
        tx_lines = [line.strip() for line in f if line.strip()]

    if not tx_lines:
        print("[FAIL] No transactions found in block_0.dat.")
        return

    root = compute_merkle_root(tx_lines)
    print(f"MERKLE ROOT HASH: {root}")

if __name__ == "__main__":
    main()
