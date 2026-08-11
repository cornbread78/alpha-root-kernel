import json
import urllib.request
import base64

def check_daemon():
    url = "http://127.0.0.1:8332/"
    username = "Cornbread78"
    password = "26a78aea33835e4d74654ce25e3e8b51a0706d8e55353f92b98c73f7ec33f416"
    
    credentials = f"{username}:{password}"
    auth_bytes = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
    
    rpc_payload = {
        "jsonrpc": "1.0",
        "id": "node_status",
        "method": "getblockchaininfo",
        "params": []
    }
    
    data = json.dumps(rpc_payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={
        'Content-Type': 'application/json',
        'Authorization': f'Basic {auth_bytes}'
    })
    
    try:
        with urllib.request.urlopen(req) as response:
            result = response.read().decode('utf-8')
            print("Node Connection Successful:")
            print(json.dumps(json.loads(result), indent=4))
    except urllib.error.HTTPError as e:
        err_body = e.read().decode('utf-8', errors='ignore')
        print(f"HTTP Error {e.code}: {e.reason}")
        if err_body:
            print(f"Response Details: {err_body}")
    except Exception as e:
        print(f"RPC Error: {e}")

if __name__ == "__main__":
    check_daemon()
