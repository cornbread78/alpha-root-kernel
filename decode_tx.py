import sys

def decode_payload(raw_hex):
    payload = bytes.fromhex(raw_hex)
    mask = bytes.fromhex("04040000")
    unmasked = bytes([b ^ mask[i % len(mask)] for i, b in enumerate(payload)])
    print(f"DECODED PAYLOAD: {unmasked.decode('utf-8', errors='ignore')}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        decode_payload(sys.argv[1])
