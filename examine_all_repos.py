import urllib.request
import json

USER_REPOS_URL = "https://api.github.com/users/cornbread78/repos"

def fetch_user_repos(url):
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "AlphaRootKernel-MultiRepoInspector"}
    )
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode())
    except Exception as e:
        print(f"[!] Error fetching repositories: {e}")
        return []

def main():
    print("==================================================")
    print("   MULTI-REPOSITORY GITHUB AUDIT UTILITY         ")
    print("   Target User: cornbread78                       ")
    print("==================================================\n")

    repos = fetch_user_repos(USER_REPOS_URL)
    if not repos:
        print("[!] No repositories retrieved or user profile not accessible.")
        return

    print(f"[+] Successfully connected to GitHub API.")
    print(f"[+] Total public repositories found: {len(repos)}\n")

    print("--------------------------------------------------")
    print("   REPOSITORY MANIFEST & DETAILS                  ")
    print("--------------------------------------------------")

    for repo in repos:
        name = repo.get("name")
        full_name = repo.get("full_name")
        description = repo.get("description", "No description provided")
        language = repo.get("language", "N/A")
        updated_at = repo.get("updated_at")
        clone_url = repo.get("clone_url")
        
        print(f"\n* Repository: {full_name}")
        print(f"  - Description: {description}")
        print(f"  - Primary Language: {language}")
        print(f"  - Last Updated: {updated_at}")
        print(f"  - Clone URL: {clone_url}")

    print("\n[+] MULTI-REPOSITORY AUDIT COMPLETE.")

if __name__ == "__main__":
    main()
