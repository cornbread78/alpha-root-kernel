import os
import json

def inspect_local_files():
    print("[*] Inspecting local workspace files in current directory...")
    print("-" * 50)
    
    # Check ledger
    if os.path.exists("alpha_root.ledger"):
        print("[+] Found: alpha_root.ledger")
        try:
            with open("alpha_root.ledger", "r") as f:
                content = f.read()
            print(f"    Content: {content}")
        except Exception as e:
            print(f"    [!] Error reading ledger: {e}")
    else:
        print("[-] Missing: alpha_root.ledger")

    # Check export json
    if os.path.exists("alpha_root_export.json"):
        print("[+] Found: alpha_root_export.json")
        try:
            with open("alpha_root_export.json", "r") as f:
                data = json.load(f)
            print(f"    JSON Data: {json.dumps(data, indent=2)}")
        except Exception as e:
            print(f"    [!] Error reading JSON: {e}")
    else:
        print("[-] Missing: alpha_root_export.json")

    # Check kernel tx payload
    if os.path.exists("kernel_tx.dat"):
        print("[+] Found: kernel_tx.dat")
        try:
            with open("kernel_tx.dat", "rb") as f:
                payload = f.read()
            print(f"    Size: {len(payload)} bytes")
            print(f"    Hex Preview: {payload[:32].hex()}...")
        except Exception as e:
            print(f"    [!] Error reading payload: {e}")
    else:
        print("[-] Missing: kernel_tx.dat")
        
    print("-" * 50)
    print("[*] Inspection complete. Returning control to command line.")

if __name__ == "__main__":
    inspect_local_files()
