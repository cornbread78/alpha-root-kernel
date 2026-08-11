import os

def inspect_all_dat_files():
    print("==================================================")
    print(" COMPREHENSIVE .DAT FILES INSPECTION")
    print("==================================================")
    
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.dat'):
                path = os.path.join(root, file)
                size = os.path.getsize(path)
                print(f"\n[+] File: {path}")
                print(f"    Size: {size} bytes")
                
                with open(path, "rb") as f:
                    content = f.read()
                
                print(f"    Hex (first 64 bytes): {content[:64].hex()}")
                
                # If the file is small enough, print its full hex and printable strings
                if size <= 1024:
                    print(f"    Full Hex: {content.hex()}")
                    try:
                        ascii_str = "".join([chr(b) if 32 <= b <= 126 else '.' for b in content])
                        print(f"    Ascii View: {ascii_str}")
                    except Exception:
                        pass

if __name__ == "__main__":
    inspect_all_dat_files()
