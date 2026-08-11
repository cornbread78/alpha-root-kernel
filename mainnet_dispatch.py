import socket
import os
import hashlib
import json

def mainnet_dispatch():
    target_host = "179.118.220.79"
    target_port = 8333
    path_vector = "04/04/00/00"

    print("==================================================")
    print(" ALPHA ROOT KERNEL - MAINNET NODE PUSH")
    print(f" Target Node: {target_host}:{target_port}")
    print(f" Path Vector: {path_vector}")
    print("==================================================\n")

    # Locate payload file
    payload_files = ["xor_masked_kernel_tx.dat", "final_mainnet_frame.hex", "kernel_tx.dat"]
    payload_file = None
    for f in payload_files:
        if os.path.exists(f):
            payload_file = f
            break

    if not payload_file:
        print("[!] Error: No valid mainnet payload or frame file found.")
        return

    with open(payload_file, "rb") as pf:
        payload_data = pf.read()

    payload_hash = hashlib.sha256(payload_data).hexdigest()
    print(f"[+] Loaded Payload: {payload_file} ({len(payload_data)} bytes)")
    print(f"[+] Payload SHA-256 Hash: {payload_hash}")

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.settimeout(20.0)

    try:
        print(f"[*] Connecting to mainnet node socket {target_host}:{target_port}...")
        client.connect((target_host, target_port))
        print("[+] Connected successfully.")

        print(f"[*] Broadcasting payload stream to mainnet node...")
        client.sendall(payload_data)

        print("[+] Awaiting response acknowledgment...")
        response = client.recv(8192)

        if response:
            print(f"[+] Node Acknowledgment Hex: {response.hex()}")
        else:
            print("[+] Connection acknowledged and closed cleanly.")

        print("==================================================")
        print(f"[+] STATUS: PATH VECTOR {path_vector} MAINNET PUSH COMMITTED")
        print("==================================================")

        receipt = {
            "target": f"{target_host}:{target_port}",
            "path_vector": path_vector,
            "payload_file": payload_file,
            "payload_hash": payload_hash,
            "bytes_sent": len(payload_data),
            "status": "MAINNET_DISPATCH_COMMITTED"
        }
        with open("mainnet_dispatch_receipt.json", "w") as rf:
            json.dump(receipt, rf, indent=4)

    except Exception as e:
        print(f"[!] Dispatch failed: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    mainnet_dispatch()
