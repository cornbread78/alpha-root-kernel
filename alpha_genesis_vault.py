import os
import json
import hashlib
from merkle_tree import compute_merkle_root

GENESIS_PREV_HASH = "0" * 64
BLOCK_FILE = "block_0.dat"
STATE_FILE = "chain_state.json"
VAULT_FILE = "vault_consensus.json"

def generate_genesis_vault():
    print("=== ALPHA ROOT KERNEL: GENESIS VAULT CONSENSUS ===")
    
    # 1. Verify ledger data
    if not os.path.exists(BLOCK_FILE):
        print(f"[FAIL] Missing {BLOCK_FILE}. Please generate transactions first.")
        return

    with open(BLOCK_FILE, 'r') as f:
        tx_lines = [line.strip() for line in f if line.strip()]

    if not tx_lines:
        print("[FAIL] No transactions found in genesis block.")
        return

    # 2. Compute Merkle Root across Genesis transactions
    merkle_root = compute_merkle_root(tx_lines)

    # 3. Formulate Genesis Header
    genesis_header = {
        "kernel_id": "ALPHA_ROOT_KERNEL_04040000",
        "block_height": 0,
        "prev_hash": GENESIS_PREV_HASH,
        "merkle_root": merkle_root,
        "tx_count": len(tx_lines),
        "status": "GENESIS_VAULT_LOCKED"
    }

    # 4. Compute Master Genesis Vault Hash
    header_raw = json.dumps(genesis_header, sort_keys=True).encode('utf-8')
    vault_hash = hashlib.sha256(header_raw).hexdigest()
    genesis_header["vault_hash"] = vault_hash

    # 5. Write to local vault consensus state
    with open(VAULT_FILE, 'w') as f:
        json.dump(genesis_header, f, indent=4)

    # Update chain_state.json to sync genesis height
    chain_state = {
        "height": 0,
        "genesis_hash": vault_hash,
        "prev_hash": GENESIS_PREV_HASH,
        "merkle_root": merkle_root,
        "tx_count": len(tx_lines)
    }
    with open(STATE_FILE, 'w') as f:
        json.dump(chain_state, f, indent=4)

    print("\n--------------------------------------------------")
    print(f"GENESIS HASH: {vault_hash}")
    print(f"MERKLE ROOT:  {merkle_root}")
    print(f"STATUS:       {genesis_header['status']}")
    print(f"SAVED TO:     {VAULT_FILE}")
    print("--------------------------------------------------")

if __name__ == "__main__":
    generate_genesis_vault()
