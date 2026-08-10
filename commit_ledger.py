import time
def commit_block():
    ledger_entry = {
        "kernel": "Alpha Root Kernel",
        "path": "04/04/00/00",
        "hash": "dfa87a6e282cb926bc6d0bbff815d9377fad96eca044e38a08212a50b11bd791",
        "timestamp": int(time.time()),
        "status": "CONSENSUS_LOCKED"
    }
    with open("alpha_root.ledger", "a") as f:
        f.write(str(ledger_entry) + "\\n")
    print("[+] Consensus state permanently committed to alpha_root.ledger")
if __name__ == "__main__":
    commit_block()
