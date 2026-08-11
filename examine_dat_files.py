import os

def inspect_dat_files():
    current_dir = os.getcwd()
    print(f"[*] Scanning for .dat files in: {current_dir}")
    
    dat_files = [f for f in os.listdir(current_dir) if f.endswith('.dat')]
    print(f"\n[+] Found {len(dat_files)} .dat files:")
    
    for file in sorted(dat_files):
        file_path = os.path.join(current_dir, file)
        size = os.path.getsize(file_path)
        print(f"\n{'='*50}")
        print(f"File: {file} | Size: {size} bytes")
        print(f"{'='*50}")
        
        try:
            with open(file_path, "rb") as f:
                preview = f.read(64)
                print(f"[*] Hex Preview (first 64 bytes):")
                print(f"    {preview.hex()}")
        except Exception as e:
            print(f"[-] Error reading file: {e}")

if __name__ == "__main__":
    inspect_dat_files()
