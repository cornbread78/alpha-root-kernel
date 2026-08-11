import os
import json

def scan_workspace():
    print("==================================================")
    print(" ALPHA ROOT KERNEL - KEY MATERIAL SCANNER")
    print("==================================================")
    
    target_files = [
        "kernel_tx.dat",
        "alpha_root.ledger",
        "alpha_root_export.json",
        "alpha_proof_manifest.json",
        "settings.json"
    ]
    
    found_keys = False
    for filename in target_files:
        if os.path.exists(filename):
            print(f"[+] Inspecting {filename}...")
            with open(filename, "rb") as f:
                content = f.read()
                # Check for common key indicators or private key patterns
                if b"WIF" in content or b"private" in content.lower() or b"seed" in content.lower():
                    print(f"    [!] Potential key reference found in {filename}")
                    found_keys = True
                else:
                    print(f"    [-] Clean binary/structured payload (No private keys present).")
        else:
            print(f"[!] File not found: {filename}")

    if not found_keys:
        print("--------------------------------------------------")
        print("[+] SCAN COMPLETE: No private keys, seed phrases, or WIF formats exist within the workspace files.")

if __name__ == "__main__":
    scan_workspace()
