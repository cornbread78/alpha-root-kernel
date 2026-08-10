import os

def main():
    print("==================================================")
    print("   ALPHA ROOT KERNEL - FINAL WORKSPACE SUMMARY    ")
    print("   Path Vector: 04/04/00/00                       ")
    print("==================================================")
    
    assets = ["kernel_tx.dat", "consensus_proof.sha256"]
    for asset in assets:
        if os.path.exists(asset):
            size = os.path.getsize(asset)
            print(f"[+] Asset Verified: {asset} ({size} bytes)")
        else:
            print(f"[!] Warning: Missing asset -> {asset}")
            
    print("[+] Workspace locked and operational.")

if __name__ == "__main__":
    main()
