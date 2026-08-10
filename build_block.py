import os
import json
import hashlib
import time

def append_to_block_0(tx_hex):
    config_file = 'kernel_sync_config.json'
    block_file = 'block_0.dat'
    state_file = 'chain_state.json'

    if not os.path.exists(config_file):
        print("Error: kernel_sync_config.json not found.")
        return

    # 1. Append the raw hex payload to block_0.dat
    with open(block_file, 'a') as f:
        f.write(tx_hex + '\n')

    # 2. Load or initialize local chain state
    if os.path.exists(state_file):
        with open(state_file, 'r') as f:
            state = json.load(f)
    else:
        state = {
            "height": 0,
            "prev_hash": "0000000000000000000000000000000000000000000000000000000000000000",
            "tx_count": 0
        }

    # 3. Compute block header hash bound to path 04/04/00/00
    timestamp = int(time.time())
    header_data = f"{state['height']}|{state['prev_hash']}|{tx_hex}|{timestamp}|04/04/00/00".encode('utf-8')
    block_hash = hashlib.sha256(header_data).hexdigest()

    # 4. Advance consensus state
    current_height = state["height"]
    state["height"] += 1
    state["prev_hash"] = block_hash
    state["tx_count"] += 1
    state["last_updated"] = timestamp

    with open(state_file, 'w') as f:
        json.dump(state, f, indent=4)

    print(f"COMMITTED TO HEIGHT: {current_height}")
    print(f"BLOCK_HASH: {block_hash}")
    print(f"LEDGER_FILE: {block_file}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        append_to_block_0(sys.argv[1])
    else:
        print("Usage: python3 build_block.py <RAW_HEX>")
