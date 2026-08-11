import os
import hashlib

PATH_VECTOR = "04/04/00/00"
TARGET_FILES = ["kernel_tx.dat", "xor_masked_op_return.hex"]

def open_sesame_raw_bytes():
    print("==================================================")
    print("   ALPHA ROOT KERNEL - OPEN SESAME RAW HEX        ")
    print(f"   Path Vector: {PATH_VECTOR}")
    print("==================================================")

    for filename in TARGET_FILES:
        if os.path.exists(filename):
            with open(filename, "rb") as f:
                raw_bytes = f.read()
            print(f"[+] Target File: {filename}")
            print(f"[+] Total Size: {len(raw_bytes)} bytes")
            print(f"[+] Raw Byte Hex:\n{raw_bytes.hex()}")
            print("-" * 50)
        else:
            print(f"[!] Warning: {filename} not found in workspace.")

    print(f"[+] ALPHA_ROOT_KERNEL: OPEN_SESAME_UNLOCKED_PATH_04_04_00_00")
    print("==================================================")

if __name__ == "__main__":
    open_sesame_raw_bytes()
