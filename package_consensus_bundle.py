import tarfile
import os
import sys

def package_bundle():
    files_to_bundle = ["kernel_tx.dat", "alpha_root.ledger", "alpha_root_export.json"]
    archive_name = "alpha_root_consensus_bundle.tar.gz"
    
    print("[*] Checking workspace components for final packaging...")
    for f in files_to_bundle:
        if not os.path.exists(f):
            print(f"[!] Error: Required file missing -> {f}")
            sys.exit(1)
        print(f"[+] Verified: {f}")

    print(f"[*] Packaging into distribution archive: {archive_name}...")
    with tarfile.open(archive_name, "w:gz") as tar:
        for f in files_to_bundle:
            tar.add(f)
            
    print(f"[+] Consensus bundle successfully created: {archive_name}")
    print("[+] Path vector 04/04/00/00 packaged and ready for deployment.")

if __name__ == "__main__":
    package_bundle()
