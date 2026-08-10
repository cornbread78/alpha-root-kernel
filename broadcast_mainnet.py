import urllib.request
import urllib.error
import sys

def broadcast_to_mainnet():
    try:
        with open("kernel_tx.dat", "rb") as f:
            tx_bytes = f.read()
    except FileNotFoundError:
        print("[!] Error: kernel_tx.dat not found.")
        sys.exit(1)

    hex_payload = tx_bytes.hex()
    url = "https://blockstream.info/api/tx"
    
    print(f"[*] Submitting {len(tx_bytes)} bytes ({len(hex_payload)} hex chars) to public mainnet endpoint...")

    req = urllib.request.Request(
        url,
        data=hex_payload.encode('utf-8'),
        headers={'Content-Type': 'text/plain'}
    )

    try:
        with urllib.request.urlopen(req) as response:
            result = response.read().decode('utf-8')
            print("[+] Public Network Broadcast Successful!")
            print("[*] Mainnet Response:", result)
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8', errors='ignore')
        print(f"[!] HTTP Error {e.code}: {e.reason}")
        print(f"[!] Server Response: {error_body}")
    except Exception as e:
        print(f"[!] Transmission Error: {e}")

if __name__ == "__main__":
    broadcast_to_mainnet()
