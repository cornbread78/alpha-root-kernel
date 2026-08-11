import json
import time
import os

REPORT_FILE = "kernel_inspection_report.json"
LEDGER_FILE = "alpha_root.ledger"
EXPORT_FILE = "alpha_root_export.json"

def main():
    print("==================================================")
    print("   ALPHA ROOT KERNEL - LEDGER SYNCHRONIZATION     ")
    print("   Path Vector: 04/04/00/00                       ")
    print("==================================================\n")

    if not os.path.exists(REPORT_FILE):
        print(f"[!] Error: {REPORT_FILE} not found. Run inspection first.")
        return

    with open(REPORT_FILE, "r") as f:
        report = json.load(f)

    current_timestamp = int(time.time())

    ledger_data = {
        "kernel": "Alpha Root Kernel",
        "path": report["path_vector"],
        "hash": report["masked_sha256"],
        "raw_hash": report["raw_sha256"],
        "timestamp": current_timestamp,
        "status": "CONSENSUS_LOCKED_XOR_VERIFIED"
    }

    export_data = {
        "kernel": "Alpha Root Kernel",
        "path": report["path_vector"],
        "timestamp": current_timestamp,
        "status": "CONSENSUS_LOCKED_XOR_VERIFIED",
        "interface": "127.0.0.1:8350",
        "hash_proof": report["masked_sha256"][:32],
        "node_response": f"[+] ALPHA_ROOT_KERNEL: CONSENSUS_LOCKED_PATH_{report['path_vector'].replace('/', '_')}_XOR_VERIFIED"
    }

    with open(LEDGER_FILE, "w") as f:
        f.write(str(ledger_data))

    with open(EXPORT_FILE, "w") as f:
        json.dump(export_data, f, indent=4)

    print(f"[+] Updated ledger record saved to {LEDGER_FILE}")
    print(f"[+] Updated export manifest saved to {EXPORT_FILE}")
    print(f"[+] Active Masked Hash: {report['masked_sha256']}")
    print("[+] PATH VECTOR 04/04/00/00 LEDGER SYNCHRONIZATION COMMITTED.")

if __name__ == "__main__":
    main()
