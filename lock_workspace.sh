#!/bin/bash
echo "[+] Locking Alpha Root Kernel workspace files against modification..."

# Make all files read-only (owner, group, others)
find . -type f -exec chmod 444 {} +

# Make all directories read-only and traverse-only
find . -type d -exec chmod 555 {} +

echo "[+] Workspace files successfully locked. Write permissions removed."
