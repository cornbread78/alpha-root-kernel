import sys
def run_consensus_mask():
    path_bytes = bytes([0x04, 0x04, 0x00, 0x00])
    xor_mask = bytes([0x53, 0x65, 0x63, 0x72, 0x65, 0x74])
    masked_stream = bytes(b ^ xor_mask[i % len(xor_mask)] for i, b in enumerate(path_bytes))
    print("[*] Alpha Root Kernel: XOR Mask Applied")
    print("[-] Raw Path: 04/04/00/00")
    print("[+] Masked Output Hex:", masked_stream.hex())
if __name__ == "__main__":
    run_consensus_mask()
