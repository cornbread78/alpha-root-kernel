import os
import urllib.request
import urllib.error

def dispatch_packet():
    print("==================================================")
    print("   ALPHA ROOT KERNEL - TRANSACTION DISPATCHER     ")
    print("   Path Vector: 04/04/00/00                       ")
    print("==================================================")
    
    packet_file = "compliant_tx.hex"
    if not os.path.exists(packet_file):
        print(f"[!] Critical Error: {packet_file} not found in workspace.")
        return

    with open(packet_file, "r") as f:
        tx_hex = f.read().strip()

    print(f"[+] Loaded transaction packet: {len(tx_hex)} hex characters")

    # Target broadcast endpoint (Testnet node gateway for protocol verification)
    url = "https://mempool.space/testnet/api/tx"
    print(f"[*] Dispatching packet to network node gateway...")

    req = urllib.request.Request(
        url, 
        data=tx_hex.encode('utf-8'), 
        headers={'Content-Type': 'text/plain'}
    )

    try:
        with urllib.request.urlopen(req) as response:
            txid = response.read().decode('utf-8')
            print(f"[+] Transmission accepted! Node TXID: {txid}")
    except urllib.error.HTTPError as e:
        error_response = e.read().decode('utf-8')
        print(f"[!] Node validation feedback: {error_response}")

if __name__ == "__main__":
    dispatch_packet()
