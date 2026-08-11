import os

def parse_keys():
    filename = "xor_masked_kernel_tx.dat"
    if not os.path.exists(filename):
        print(f"[!] {filename} not found.")
        return

    with open(filename, "rb") as f:
        data = f.read()

    print("==================================================")
    print(" ALPHA ROOT KERNEL - DETAILED KEY PARSER")
    print("==================================================")
    print(f"[+] Payload Size: {len(data)} bytes")
    
    candidates = []
    for i in range(len(data)):
        if data[i] in [2, 3, 4] and i + 1 < len(data):
            candidates.append((i, data[i]))

    print(f"[+] Byte markers matching key prefixes found at offsets: {[c[0] for c in candidates]}")
    
    print("--------------------------------------------------")
    print("[+] Segment Analysis (16-byte blocks):")
    for offset in range(0, len(data), 16):
        chunk = data[offset:offset+16]
        print(f"    Offset {offset:03d}: {chunk.hex()}")

    print("==================================================")

if __name__ == "__main__":
    parse_keys()
