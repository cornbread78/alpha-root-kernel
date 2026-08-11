import subprocess
import json

cmd = [
    "bitcoin-cli",
    "-rpcuser=Cornbread78",
    "-rpcpassword=26a78aea33835e4d74654ce25e3e8b51a0706d8e55353f92b98c73f7ec33f416",
    "getblockheader",
    "0000000082b5015589a3fdf2d4baff403e6f0be035a5d9742c1cae6295464449"
]

result = subprocess.run(cmd, capture_output=True, text=True)
if result.returncode == 0:
    data = json.loads(result.stdout)
    print(f"[+] Parsed Block Height: {data['height']}")
    print(f"[+] Hash: {data['hash']}")
    print(f"[+] Previous Hash: {data['previousblockhash']}")
    print(f"[+] Next Block Hash: {data['nextblockhash']}")
else:
    print(f"[!] Error: {result.stderr.strip()}")
