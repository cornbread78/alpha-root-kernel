import os
import json

def parse_container():
    filename = "kernel_tx.dat"
    print("==================================================")
    print(" ALPHA ROOT KERNEL - CONTAINER CARGO PARSER")
    print("==================================================")

    if not os.path.exists(filename):
        print(f"[!] Error: {filename} not found in current directory.")
        return

    with open(filename, "rb") as f:
        payload_bytes = f.read()

    print(f"[+] Total Payload Container Size: {len(payload_bytes)} bytes")

    # Deconstruct container segments based on structural layout
    container_data = {
        "version_marker": payload_bytes[0:4].hex(),
        "input_vector_index": payload_bytes[4:5].hex(),
        "prevout_reference_hash": payload_bytes[5:37].hex(),
        "sequence_or_height": payload_bytes[37:41].hex(),
        "embedded_cargo_data": payload_bytes[41:].hex(),
        "extracted_text_string": "".join([chr(b) if 32 <= b <= 126 else "." for b in payload_bytes[41:]])
    }

    print("--------------------------------------------------")
    print(f"[+] Version Marker: {container_data['version_marker']}")
    print(f"[+] Input Vector Index: {container_data['input_vector_index']}")
    print(f"[+] Reference Hash: {container_data['prevout_reference_hash']}")
    print(f"[+] Sequence/Height Field: {container_data['sequence_or_height']}")
    print(f"[+] Embedded Cargo Hex: {container_data['embedded_cargo_data']}")
    print(f"[+] Decoded Cargo Text: {container_data['extracted_text_string']}")
    print("--------------------------------------------------")

    # Save parsed container report
    report_filename = "container_cargo_report.json"
    with open(report_filename, "w") as rf:
        json.dump(container_data, rf, indent=4)
        
    print(f"[+] Container cargo successfully mapped and saved to: {report_filename}")

if __name__ == "__main__":
    parse_container()
