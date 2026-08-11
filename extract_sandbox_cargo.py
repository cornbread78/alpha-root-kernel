import os
import tarfile
import hashlib
import json

def package_cargo():
    print("==================================================w")
    print(" ALPHA ROOT KERNEL - SANDBOX CARGO EXTRACTION")
    print(" Path Vector: 04/04/00/00")
    print("==================================================")

    # Core assets to bundle
    assets = [
        "kernel_tx.dat",
        "xor_masked_kernel_tx.dat",
        "alpha_root.ledger",
        "alpha_root_export.json",
        "alpha_proof_manifest.json",
        "kernel_utxo_active.json"
    ]

    valid_assets = []
    manifest = {}

    for asset in assets:
        if os.path.exists(asset):
            with open(asset, "rb") as f:
                content = f.read()
            file_hash = hashlib.sha256(content).hexdigest()
            valid_assets.append(asset)
            manifest[asset] = {
                "size_bytes": len(content),
                "sha256": file_hash
            }
            print(f"[+] Verified & Packed: {asset} ({len(content)} bytes)")
        else:
            print(f"[!] Optional asset not found: {asset}")

    # Write export manifest summary
    export_filename = "sandbox_cargo_manifest.json"
    with open(export_filename, "w") as ef:
        json.dump(manifest, ef, indent=4)
    valid_assets.append(export_filename)

    # Create tarball archive
    archive_name = "alpha_root_sandbox_cargo.tar.gz"
    with tarfile.open(archive_name, "w:gz") as tar:
        for asset in valid_assets:
            if os.path.exists(asset):
                tar.add(asset)

    print("--------------------------------------------------")
    print(f"[+] Sandbox Cargo Archive Created: {archive_name}")
    print(f"[+] Cargo Manifest Saved: {export_filename}")
    print("[+] STATUS: SANDBOX_CARGO_EXTRACTED_SUCCESSFULLY")
    print("==================================================w")

if __name__ == "__main__":
    package_cargo()
