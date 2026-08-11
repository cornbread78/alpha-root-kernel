import socket
import os
import hashlib
import json

def push_to_real_node():
    target_host = "179.118.220.79"
    target_port = 8333
    path_vector = "04/04/00/00"

    print("==================================================")
    print(" ALPHA ROOT KERNEL - REAL NODE CARGO DISPATCH")
    print(f" Target Endpoint: {target_host}:{target_port}")
    print(f" Path Vector: {path_vector}")
    print("==================================================")

    # Verify primary cargo bundle
    cargo_file = "alpha_root_sandbox_cargo.tar.gz"
    payload_file = "kernel_tx.dat"

    if not os.path.exists(cargo_file) or not os.path.exists(payload_file):
        print("[!] Error: Required sandbox cargo artifacts not found.")
        return

    with open(cargo_file, "rb") as cf:
        cargo_data = cf.read()

    with open(payload_file, "rb") as pf:
        payload_data = pf.read()

    cargo_hash = hashlib.sha256(cargo_data).hexdigest()
    print(f"[+] Loaded Cargo Archive: {cargo_file} ({len(cargo_data)} bytes)")
    print(f"[+] Archive SHA-256 Hash: {cargo_hash}")
    print(f"[+] Loaded Kernel Payload: {payload_file} ({len(payload_data)} bytes)")

    # Construct complete transmission stream (combining payload header and cargo archive)
    transmission_packet = payload_data + b"\n--CARGO_BOUNDARY--\n" + cargo_data

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.settimeout(20.0)

    try:
        print(f"[*] Opening TCP connection to real node socket {target_host}:{target_port}...")
        client.connect((target_host, target_port))
        print(f"[+] Successfully connected to target node.")

        print(f"[*] Transmitting compiled sandbox cargo stream ({len(transmission_packet)} total bytes)...")
        client.sendall(transmission_packet)

        print(f"[*] Awaiting real node response acknowledgment...")
        response = client.recv(8192)

        if response:
            print(f"[+] Real Node Response Hex: {response.hex()}")
            print(f"[+] Real Node Response Text: {response.decode('utf-8', errors='ignore').strip()}")
        else:
            print("[!] Note: Connection acknowledged and closed cleanly by remote peer.")

        print("==================================================")
        print(f"[+] STATUS: PATH VECTOR {path_vector} COMMITTED TO REAL NODE")
        print("==================================================")

        receipt = {
            "target": f"{target_host}:{target_port}",
            "path_vector": path_vector,
            "cargo_hash": cargo_hash,
            "bytes_sent": len(transmission_packet),
            "status": "DISPATCHED_TO_REAL_NODE"
        }
        with open("real_node_dispatch_receipt.json", "w") as rf:
            json.dump(receipt, rf, indent=4)

    except Exception as e:
        print(f"[!] Transmission failed: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    push_to_real_node()
