import struct
def create_kernel_transaction():
    path_str = "04/04/00/00"
    masked_hex = "57616372"
    version = struct.pack("<I", 1)
    tx_in_count = b"\x01"
    previous_output = bytes.fromhex("00" * 32)
    previous_index = struct.pack("<I", 0)
    sig_payload = path_str.encode("utf-8") + bytes.fromhex(masked_hex)
    script_sig = struct.pack("B", len(sig_payload)) + sig_payload
    sequence = struct.pack("<I", 0xffffffff)
    tx_out_count = b"\x01"
    value = struct.pack("<Q", 5000000000)
    pubkey_script = bytes.fromhex("41" + "04" + "00" * 32 + "ac")
    lock_time = struct.pack("<I", 0)
    raw_tx = version + tx_in_count + previous_output + previous_index + script_sig + sequence + tx_out_count + value + pubkey_script + lock_time
    print("--- Alpha Root Kernel: Transaction Frame ---")
    print("Path:", path_str)
    print("Kernel State Hex:", masked_hex)
    print("Raw Transaction Hex:\\n" + raw_tx.hex())
if __name__ == "__main__":
    create_kernel_transaction()
