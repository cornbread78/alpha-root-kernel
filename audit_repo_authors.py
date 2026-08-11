import urllib.request
import json

USERNAME = "cornbread78"
REPOS_URL = f"https://api.github.com/users/{USERNAME}/repos"

def api_get(url):
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "RepoAuthorAudit-Utility"}
    )
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode())
    except Exception:
        return None

def main():
    print("==================================================")
    print("   MULTI-REPOSITORY AUTHOR & INTEGRITY AUDIT      ")
    print(f"   Target User: {USERNAME}")
    print("==================================================\n")

    repos = api_get(REPOS_URL)
    if not repos or not isinstance(repos, list):
        print("[!] Error fetching user repositories.")
        return

    print(f"[+] Scanning {len(repos)} repositories for external commits...\n")
    foreign_commits_found = False

    for repo in repos:
        repo_name = repo.get("full_name")
        commits_url = f"https://api.github.com/repos/{repo_name}/commits"
        commits = api_get(commits_url)

        if not commits or not isinstance(commits, list):
            continue

        for commit in commits:
            author_obj = commit.get("author")
            author_login = author_obj.get("login") if author_obj else "Unknown"
            commit_data = commit.get("commit", {})
            committer_name = commit_data.get("committer", {}).get("name", "Unknown")
            sha = commit.get("sha", "")[:7]
            message = commit_data.get("message", "").split("\n")[0]

            # Check if the commit author/login does not match your username
            if author_login and author_login.lower() != USERNAME.lower() and author_login != "Unknown":
                foreign_commits_found = True
                print(f"[!] Non-Owner Commit in {repo_name}:")
                print(f"    - SHA: {sha}")
                print(f"    - Author Login: {author_login}")
                print(f"    - Committer: {committer_name}")
                print(f"    - Message: {message}\n")

    if not foreign_commits_found:
        print("[+] Audit complete: Every reviewed commit across all repositories matches your account credentials.")
    else:
        print("[+] Audit complete: Review flagged entries above.")

if __name__ == "__main__":
    main()
