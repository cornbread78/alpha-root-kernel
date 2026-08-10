import subprocess
import os

def run_git_check():
    print("[*] Checking local repository and tracking status...")
    
    if not os.path.exists(".git"):
        print("[!] Error: Not a git repository workspace.")
        return

    # Run git status
    status_res = subprocess.run(["git", "status"], capture_output=True, text=True)
    print("\n--- Git Status ---")
    print(status_res.stdout.strip())

    # Run git remote -v
    remote_res = subprocess.run(["git", "remote", "-v"], capture_output=True, text=True)
    print("\n--- Remote Tracking ---")
    print(remote_res.stdout.strip())

    print("\n[+] Repository synchronization check complete.")

if __name__ == "__main__":
    run_git_check()
