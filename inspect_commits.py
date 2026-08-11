import urllib.request
import json

# Target repository to inspect commit history and changes
REPO = "cornbread78/alpha-root-kernel"
COMMITS_URL = f"https://api.github.com/repos/{REPO}/commits"

def inspect_commits():
    req = urllib.request.Request(
        COMMITS_URL,
        headers={"User-Agent": "AlphaRootKernel-CommitInspector"}
    )
    try:
        with urllib.request.urlopen(req) as response:
            commits = json.loads(response.read().decode())
            print("==================================================")
            print(f"   COMMIT HISTORY & CHANGE INSPECTION")
            print(f"   Target: {REPO}")
            print("==================================================\n")
            
            for i, commit in enumerate(commits[:10]):  # Inspect last 10 commits
                sha = commit.get("sha")[:7]
                commit_data = commit.get("commit", {})
                message = commit_data.get("message", "").split("\n")[0]
                author = commit_data.get("author", {}).get("name", "Unknown")
                date = commit_data.get("author", {}).get("date", "Unknown")
                
                print(f"[{i+1}] Commit SHA: {sha}")
                print(f"    Author:  {author}")
                print(f"    Date:    {date}")
                print(f"    Message: {message}\n")
                
            print("[+] COMMIT INSPECTION COMPLETE.")
    except Exception as e:
        print(f"[!] Error fetching commit history: {e}")

if __name__ == "__main__":
    inspect_commits()
