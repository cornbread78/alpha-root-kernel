import os
import json

PATH_VECTOR = "04/04/00/00"
TARGET_DIR = os.path.expanduser(f"~/{PATH_VECTOR}")

def main():
    print("==================================================")
    print("      ALPHA ROOT KERNEL - WORKSPACE INSPECTOR     ")
    print(f"      Path Vector Directory: {TARGET_DIR}")
    print("==================================================")

    if not os.path.exists(TARGET_DIR):
        print(f"[!] Directory {TARGET_DIR} does not exist.")
        return

    files = [f for f in os.listdir(TARGET_DIR) if os.path.isfile(os.path.join(TARGET_DIR, f))]
    
    if not files:
        print("[!] Workspace directory is empty.")
        return

    print(f"[+] Found {len(files)} workspace artifact(s):\n")

    for filename in sorted(files):
        filepath = os.path.join(TARGET_DIR, filename)
        size = os.path.getsize(filepath)
        
        print("--------------------------------------------------")
        print(f" Artifact: {filename} ({size} bytes)")
        print("--------------------------------------------------")

        try:
            with open(filepath, "rb") as f:
                raw_bytes = f.read()

            # Attempt JSON rendering
            try:
                json_data = json.loads(raw_bytes.decode('utf-8'))
                print("[Format: Structured JSON]")
                print(json.dumps(json_data, indent=2))
            except Exception:
                # Attempt plain UTF-8 text rendering
                try:
                    text_str = raw_bytes.decode('utf-8')
                    if text_str.isprintable() or '\n' in text_str or '\r' in text_str:
                        print("[Format: Text Sequence]")
                        print(text_str.strip())
                    else:
                        raise ValueError()
                except Exception:
                    # Fallback to raw hex inspection
                    print("[Format: Raw Binary Hex]")
                    print(f"Hex Stream: {raw_bytes.hex()}")

        except Exception as e:
            print(f"[!] Unable to read artifact: {e}")

        print("\n")

    print("==================================================")
    print("            INSPECTION COMPLETE                   ")
    print("==================================================")

if __name__ == "__main__":
    main()
