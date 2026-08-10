import subprocess
import os

def sync_workspace():
    print("[*] Staging all new control and configuration scripts...")
    subprocess.run(["git", "add", "."])
    
    print("[*] Committing workspace updates...")
    commit_res = subprocess.run(
        ["git", "commit", "-m", "ALPHA_ROOT_KERNEL: Sync control panel and external node modules for path 04/04/00/00"],
        capture_output=True, text=True
    )
    print(commit_res.stdout.strip())
    
    print("[*] Pushing updates to origin main...")
    push_res = subprocess.run(["git", "push", "origin", "main"], capture_output=True, text=True)
    if push_res.returncode == 0:
        print("[+] Repository successfully synchronized and updated on GitHub.")
        print(push_res.stdout.strip())
    else:
        print("[!] Push output / warning:")
        print(push_res.stderr.strip())

if __name__ == "__main__":
    sync_workspace()
