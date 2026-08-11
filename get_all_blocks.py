import subprocess
import json

rpc_user = "Cornbread78"
rpc_pass = "26a78aea33835e4d74654ce25e3e8b51a0706d8e55353f92b98c73f7ec33f416"

def bitcoin_cli(method, *args):
    cmd = ["bitcoin-cli", f"-rpcuser={rpc_user}", f"-rpcpassword={rpc_pass}", method] + list(args)
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(result.stderr.strip())
    return result.stdout.strip()

start_height = 76
end_height = 100

print(f"[-] Fetching block headers from height {start_height} to {end_height}...\n")
for height in range(start_height, end_height + 1):
    try:
        block_hash_raw = bitcoin_cli("getblockhash", str(height))
        block_hash = block_hash_raw.strip('"')
        
        header_raw = bitcoin_cli("getblockheader", block_hash)
        header = json.loads(header_raw)
        
        print(f"[+] Height: {header['height']:3d} | Hash: {header['hash']} | Next: {header.get('nextblockhash', 'N/A')}")
    except Exception as e:
        print(f"[!] Error at height {height}: {e}")
        break
