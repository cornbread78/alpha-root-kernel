import os
import json

def read_ledger():
    block_file = 'block_0.dat'
    state_file = 'chain_state.json'
    mask = bytes.fromhex("04040000")

    if not os.path.exists(block_file):
        print("Error: block_0.dat not found.")
        return

    print("=== LOCAL CHAIN STATE ===")
    if os.path.exists(state_file):
        with open(state_file, 'r') as f:
            state = json.load(f)
            print(json.dumps(state, indent=4))

    print("\n=== UNMASKED TRANSACTIONS IN BLOCK 0 ===")
    with open(block_file, 'r') as f:
        for idx, line in enumerate(f):
            raw_hex = line.strip()
            if not raw_hex:
                continue
            payload = bytes.fromhex(raw_hex)
            unmasked = bytes([b ^ mask[i % len(mask)] for i, b in enumerate(payload)])
            print(f"TX [{idx}]: {unmasked.decode('utf-8', errors='ignore')}")

if __name__ == "__main__":
    read_ledger()
