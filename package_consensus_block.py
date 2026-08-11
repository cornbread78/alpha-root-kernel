import os
import hashlib

def package_block():
    filename = "kernel_tx.dat"
    path_vector = "04/04/00/00"
    
    print("==================================================")
    print(" ALPHA ROOT KERNEL - CONSENSUS BLOCK PACKAGER")
    print(f" Path Vector: {path_vector}")
    print("==================================================")

    if not os.path.exists(filename):
        print(f"[!] Error: {filename} not found in workspace.")
        return

    with open(filename, "rb") as f:
        raw_data = f.read()

    xor_mask = bytes([4, 4, 0, 0])
    masked_data = bytearray(b ^ xor_mask[i % len(xor_mask)] for i, b in enumerate(raw_data))
    
    block_header = b"ARV1" + len(masked_data).to_bytes(4, 'big') + bytes([4, 4, 0, 0])
    consensus_block = block_header + masked_data
    
    output_filename = "alpha_consensus_block.bin"
    with open(output_filename, "wb") as f:
        f.write(consensus_block)

    block_hash = hashlib.sha256(consensus_block).hexdigest()

    print(f"[+] Loaded raw payload: {len(raw_data)} bytes")
    print(f"[+] Applied XOR mask: {[4, 4, 0, 0]}")
    print(f"[+] Generated Block Container: {output_filename}")
    print(f"[+] Total Block Size: {len(consensus_block)} bytes")
    print(f"[+] Consensus Block SHA-256 Hash: {block_hash}")
    print("==================================================")
    print("[+] STATUS: CONSENSUS BLOCK CONTAINER PACKAGED")
    print("==================================================")

if __name__ == "__main__":
    package_block()
