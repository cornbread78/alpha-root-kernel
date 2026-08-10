import urllib.request
import urllib.error

def broadcast_transaction(tx_hex, network="testnet"):
    # Select endpoint (use testnet for initial validation testing, or mainnet)
    if network == "mainnet":
        url = "https://mempool.space/api/tx"
    else:
        url = "https://mempool.space/testnet/api/tx"
        
    print(f"[*] Dispatching transaction to {network} broadcast node...")
    
    req = urllib.request.Request(
        url, 
        data=tx_hex.strip().encode('utf-8'), 
        headers={'Content-Type': 'text/plain'}
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            txid = response.read().decode('utf-8')
            print(f"[+] Broadcast successful! TXID: {txid}")
    except urllib.error.HTTPError as e:
        error_message = e.read().decode('utf-8')
        print(f"[!] Broadcast rejected by node: {error_message}")

if __name__ == "__main__":
    # Replace with your fully signed raw transaction hex string
    raw_tx_hex = "0200000001..." 
    broadcast_transaction(raw_tx_hex, network="testnet")
