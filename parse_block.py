import json

data = {
  "hash": "000000006a625f06636b8bb6ac7b960a8d03705d1ace08b1a19da3fdcc99ddbd",
  "confirmations": 961942,
  "height": 2,
  "version": 1,
  "versionHex": "00000001",
  "merkleroot": "d5fdcc541e25de1c7a5addedf24858b8bb665c9f36ef744ee42c316022c90f9b",
  "time": 1231469744,
  "mediantime": 1231469665,
  "nonce": 1639830024,
  "bits": "1d00ffff",
  "target": "00000000ffff0000000000000000000000000000000000000000000000000000",
  "difficulty": 1,
  "chainwork": "0000000000000000000000000000000000000000000000000000000300030003",
  "previousblockhash": "00000000839a8e6886ab5951d76f411475428afc90947ee320161bbf18eb6048",
  "nextblockhash": "0000000082b5015589a3fdf2d4baff403e6f0be035a5d9742c1cae6295464449"
}

print(f"[+] Parsed Block Height: {data['height']}")
print(f"[+] Hash: {data['hash']}")
print(f"[+] Previous Hash: {data['previousblockhash']}")
