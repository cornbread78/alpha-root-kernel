import os
import struct

def frame_kernel_data():
    print("==================================================")
    print(" MAGIC BYTES FRAME PARSER & BLOCK BUILDER")
    print("==================================================")
    
    kernel_path = "kernel_tx.dat"
    if os.path.exists(kernel_path):
        with open(kernel_path, "rb") as f:
            kernel_data = f.read()
        print(f"[+] Loaded {kernel_path}: {len(kernel_data)} bytes")
    else:
        print("[-] Error: kernel_tx.dat not found.")
        return

    # Mainnet magic bytes (Little-Endian: d9b4bef9)
    magic_bytes = bytes.fromhex("d9b4bef9")
    
    # Calculate payload size (4 bytes, little-endian)
    payload_size = struct.pack("<I", len(kernel_data))
    
    # Construct the framed binary block/message structure
    framed_payload = magic_bytes + payload_size + kernel_data
    
    output_filename = "framed_kernel_block.dat"
    with open(output_filename, "wb") as f:
        f.write(framed_payload)
        
    print(f"[+] Successfully wrote framed data to {output_filename}")
    print(f"[+] Total Framed Size: {len(framed_payload)} bytes")
    print(f"[+] Hex Preview: {framed_payload[:32].hex()}...")

if __name__ == "__main__":
    frame_kernel_data()
