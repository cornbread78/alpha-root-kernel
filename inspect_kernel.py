import os
import hashlib
import json

PATH_ID = "04/04/00/00"
FILENAME = "kernel_tx.dat"

def main():
    print(f"[*] Target Path Vector: {PATH_ID}")
    if not os.path.exists(FILENAME):
        print(f"[!] Error: {FILENAME} not found in workspace.")
        return

    with open(FILENAME, "rb") as f:
        data = f.read()

    file_hash = hashlib.sha256(data).hexdigest()
    print(f"[+] File: {FILENAME}")
    print(f"[+] Size: {len(data)} bytes")
    print(f"[+] SHA-256 Hash: {file_hash}")
    print(f"[+] Hex Preview: {data.hex()}")
    
    report = {
        "path_vector": PATH_ID,
        "filename": FILENAME,
        "size_bytes": len(data),
        "sha256": file_hash,
        "hex_payload": data.hex()
    }
    
    with open("kernel_inspection_report.json", "w") as out:
        json.dump(report, out, indent=4)
        
    print("[+] Generated workspace report: kernel_inspection_report.json")

if __name__ == "__main__":
    main()
