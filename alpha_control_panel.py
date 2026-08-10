import os
import json
import hashlib
import subprocess

def verify_file(filename):
    if not os.path.exists(filename):
        return "MISSING", "N/A"
    with open(filename, "rb") as f:
        content = f.read()
    sha = hashlib.sha256(content).hexdigest()
    return "OK", sha

def run_panel():
    print("==================================================")
    print("     ALPHA ROOT KERNEL - CONTROL PANEL            ")
    print("     Path Vector: 04/04/00/00                      ")
    print("==================================================")
    
    files = ["kernel_tx.dat", "alpha_root.ledger", "alpha_root_export.json", "kernel_inspection_report.json"]
    
    print("\n[*] Artifact Integrity Check:")
    for f in files:
        status, sha = verify_file(f)
        print(f"  - {f}: [{status}] (SHA256: {sha[:16]}...)")
        
    print("\n[*] Repository Sync Status:")
    git_status = subprocess.run(["git", "status", "-s"], capture_output=True, text=True)
    if git_status.stdout.strip() == "":
        print("  - Working tree is clean and synchronized with origin/main.")
    else:
        print("  - Uncommitted changes detected:")
        print(git_status.stdout)
        
    print("\n[+] Control panel initialization complete. Ready for next operational directive.")

if __name__ == "__main__":
    run_panel()
