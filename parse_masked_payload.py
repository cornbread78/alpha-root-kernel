import os

def analyze_masked_payload():
    filename = "xor_masked_kernel_tx.dat"
    if not os.path.exists(filename):
        print(f"[!] {filename} not found.")
        return

    with open(filename, "rb") as f:
        data = f.read()

    print("==================================================")
    print(" ALPHA ROOT KERNEL - MASKED PAYLOAD KEY SCANNER")
    print("==================================================")
    print(f"[+] Loaded masked payload size: {len(data)} bytes")
    print(f"[+] Full Hex: {data.hex()}")
    
    # Extract printable ASCII view
    ascii_str = "".join([chr(b) if 32 <= b <= 126 else "." for b in data])
    print(f"[+] Printable ASCII Extract: {ascii_str}")
    print("==================================================")

if __name__ == "__main__":
    analyze_masked_payload()
