import os
import json
from datetime import datetime

print("==================================================")
print("     ALPHA ROOT KERNEL - LOCAL MANIFEST")
print("==================================================")

path_vector = "04/04/00/00"
files_in_dir = os.listdir(".")

manifest = {
    "timestamp": datetime.utcnow().isoformat(),
    "path_vector": path_vector,
    "tracked_files": [f for f in files_in_dir if os.path.isfile(f)]
}

print(f"[+] Target Path Vector: {path_vector}")
print(f"[+] Local Files Tracked: {len(manifest['tracked_files'])}")
for f in sorted(manifest['tracked_files']):
    print(f"    - {f}")

with open("alpha_root_export.json", "w") as f:
    json.dump(manifest, f, indent=4)

print("[+] Workspace manifest successfully updated.")
