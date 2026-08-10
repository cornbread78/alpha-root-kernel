import json
import os

CONFIG_FILE = "external_node_config.json"

def configure_target():
    print("[*] Configuring external network target interface...")
    
    # Define external node parameters (update HOST with your target node IP if needed)
    config = {
        "target_mode": "EXTERNAL_P2P",
        "host": "179.118.220.79",  # Active external peer endpoint
        "port": 8333,
        "path_vector": "04/04/00/00",
        "payload_file": "kernel_tx.dat"
    }
    
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)
        
    print(f"[+] External configuration saved to {CONFIG_FILE}")
    print(f"[+] Target interface set to {config['host']}:{config['port']}")

if __name__ == "__main__":
    configure_target()
