import http.client
import json
import base64

# Node connection configuration (adjust to your node's RPC parameters)
RPC_HOST = "127.0.0.1"
RPC_PORT = 8332
RPC_USER = "rpcuser"
RPC_PASSWORD = "rpcpassword"

def broadcast_tx(tx_hex):
    auth_str = f"{RPC_USER}:{RPC_PASSWORD}"
    encoded_auth = base64.b64encode(auth_str.encode()).decode()
    
    headers = {
        "Authorization": f"Basic {encoded_auth}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "jsonrpc": "1.0",
        "id": "alpha_broadcast",
        "method": "sendrawtransaction",
        "params": [tx_hex]
    }
    
    try:
        conn = http.client.HTTPConnection(RPC_HOST, RPC_PORT, timeout=10)
        conn.request("POST", "/", json.dumps(payload), headers)
        response = conn.getresponse()
        data = response.read().decode()
        conn.close()
        
        result = json.loads(data)
        print("==================================================")
        print("          NODE JSON-RPC BROADCAST RESULT          ")
        print("==================================================")
        if "error" in result and result["error"] is not None:
            print(f"[!] Node Rejection Error: {result['error']}")
        else:
            print(f"[+] Transaction Accepted/Broadcasted: {result.get('result')}")
        print("==================================================")
    except Exception as e:
        print(f"[!] Connection Exception: {e}")

if __name__ == "__main__":
    # Standard placeholder or generated transaction hex
    sample_tx_hex = "010000000100000000000000000000000000000000000000000000000000000000000000000000000000ffffffff0100000000000000000b6a09636f6d6520686f6d6500000000"
    broadcast_tx(sample_tx_hex)
