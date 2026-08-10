import json
import os

def translate_artifacts():
    print("[*] Translating workspace data structures...")
    
    if os.path.exists("alpha_root_export.json"):
        try:
            with open("alpha_root_export.json", "r") as f:
                data = json.load(f)
            print("[+] Decoded alpha_root_export.json successfully:")
            print(json.dumps(data, indent=2))
        except Exception as e:
            print(f"[!] JSON parse error: {e}")
            
    if os.path.exists("kernel_tx.dat"):
        with open("kernel_tx.dat", "rb") as f:
            raw = f.read()
        print(f"[+] kernel_tx.dat size: {len(raw)} bytes")
        print(f"[+] Hex preview: {raw.hex()}")

if __name__ == "__main__":
    translate_artifacts()
