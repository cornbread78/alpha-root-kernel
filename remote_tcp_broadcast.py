import socket
import sys

# Replace with your target remote peer IP and port, or a public TCP listener/echo endpoint
REMOTE_HOST = "179.118.220.79"  # Example remote node endpoint
REMOTE_PORT = 8333

def broadcast_externally():
    try:
        with open("kernel_tx.dat", "rb") as f:
            payload = f.read()
    except FileNotFoundError:
        print("[!] Error: kernel_tx.dat not found in workspace.")
        sys.exit(1)

    print(f"[*] Loaded {len(payload)} bytes from local workspace.")
    print(f"[*] Bypassing loopback (127.0.0.1). Opening raw TCP socket to {REMOTE_HOST}:{REMOTE_PORT}...")

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.settimeout(10.0)

    try:
        client.connect((REMOTE_HOST, REMOTE_PORT))
        print("[+] External TCP connection established!")
        
        client.sendall(payload)
        print("[+] Payload stream transmitted successfully across network.")
        
        try:
            response = client.recv(4096)
            if response:
                print(f"[*] Remote acknowledgment received ({len(response)} bytes):")
                print(response[:64].hex())
            else:
                print("[*] Stream acknowledged by remote host.")
        except socket.timeout:
            print("[*] Transmission complete (no immediate response payload returned).")
            
    except ConnectionRefusedError:
        print(f"[!] Connection refused by {REMOTE_HOST}:{REMOTE_PORT}. Verify remote listener status and firewall rules.")
    except socket.timeout:
        print(f"[!] Connection timed out reaching {REMOTE_HOST}:{REMOTE_PORT}.")
    except Exception as e:
        print(f"[!] External network error: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    broadcast_externally()
