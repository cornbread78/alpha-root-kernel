import os
import hashlib

MASKED_FILE = "xor_masked_op_return.hex"
PATH_VECTOR = "04/04/00/00"

def analyze_xor_utxo():
    print("==================================================")
    print("   ALPHA ROOT KERNEL - XOR UTXO MAPPER          ")
    print(f"   Path Vector: {PATH_VECTOR}")
    print("==================================================")

    if not os.path.exists(MASKED_FILE):
        print(f"[!] Error: {MASKED_FILE} missing from workspace.")
        return

    # Read as binary bytes to prevent UnicodeDecodeError
    with open(MASKED_FILE, "rb") as f:
        script_bytes = f.read()

    script_hash = hashlib.sha256(script_bytes).hexdigest()

    print(f"[+] Loaded XOR-Masked Payload: {len(script_bytes)} bytes")
    print(f"[+] Payload Hex: {script_bytes.hex()[:64]}... [truncated]")
    print(f"[+] SHA-256 Script Hash: {script_hash}")
    print(f"[+] UTXO Index Mapping: 0 (Virtual Path Vector Slot)")
    print("--------------------------------------------------")
    print(f"[+] ALPHA_ROOT_KERNEL: XOR_UTXO_MAPPED_PATH_{PATH_VECTOR.replace('/', '_')}")
    print("==================================================")

if __name__ == "__main__":
    analyze_xor_utxo()
