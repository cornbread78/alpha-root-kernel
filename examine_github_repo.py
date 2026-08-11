import urllib.request
import json

REPO_API_URL = "https://api.github.com/repos/cornbread78/alpha-root-kernel/contents"

def fetch_repo_contents(url):
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "AlphaRootKernel-Inspector"}
    )
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode())
    except Exception as e:
        print(f"[!] Error fetching from {url}: {e}")
        return []

def main():
    print("==================================================inton")
    print("   ALPHA ROOT KERNEL - GITHUB REPOSITORY AUDIT    ")
    print("   Target: cornbread78/alpha-root-kernel          ")
    print("==================================================\n")

    items = fetch_repo_contents(REPO_API_URL)
    if not items:
        print("[!] No items retrieved or repository not accessible via API.")
        return

    print(f"[+] Successfully connected to GitHub API.")
    print(f"[+] Total root items found: {len(items)}\n")

    print("--------------------------------------------------")
    print("   FILE MANIFEST & STRUCTURE                      ")
    print("--------------------------------------------------")

    for item in items:
        item_type = item.get("type")
        item_name = item.get("name")
        item_size = item.get("size", 0)
        print(f"[{item_type.upper()}] {item_name} ({item_size} bytes)")

    print("\n[+] REPOSITORY AUDIT COMPLETE.")

if __name__ == "__main__":
    main()
