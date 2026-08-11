import os
import struct

def examine_dat_files():
    print("==================================================")
    print(" COMPREHENSIVE WORKSPACE .DAT FILES SCANNER")
    print("==================================================")
    
    target_files = []
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.dat'):
                target_files.append(os.path.join(root, file))
                
    print(f"[+] Found {len(target_files)} target .dat files across workspace directories.\n")
    
    for file_path in sorted(target_files):
        size = os.path.getsize(file_path)
        print(f"{'='*50}")
        print(f"File Path : {file_path}")
        print(f"File Size : {size} bytes")
        print(f"{'='*50}")
        
        try:
            with open(file_path, "rb") as f:
                data = f.read()
            
            # Show Hex Preview
            preview_len = min(64, len(data))
            print(f"[*] Hex Preview ({preview_len} bytes):")
            print(f"    {data[:preview_len].hex()}")
            
            # If the file is small (like transactions or small data blocks), print full hex and ASCII
            if size <= 512:
                print(f"[*] Full Hex Content:")
                print(f"    {data.hex()}")
                
                ascii_view = "".join([chr(b) if 32 <= b <= 126 else '.' for b in data])
                print(f"[*] ASCII View:")
                print(f"    {ascii_view}")
            else:
                print(f"[*] File exceeds display threshold for full hex dump (Size > 512 bytes).")
                
        except Exception as e:
            print(f"[-] Error reading file {file_path}: {e}")
        print()

if __name__ == "__main__":
    examine_dat_files()
