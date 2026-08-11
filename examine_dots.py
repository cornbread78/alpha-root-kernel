import os

def scan_directories():
    current_dir = os.getcwd()
    print(f"[*] Scanning Current Directory: {current_dir}")
    
    # List hidden dotfiles in the current directory
    dotfiles = [f for f in os.listdir(current_dir) if f.startswith('.')]
    print(f"\n[+] Hidden Dotfiles Found ({len(dotfiles)}):")
    for df in dotfiles:
        print(f"    - {df}")
        
    # Inspect parent directory structures (dot-dot files/directories)
    parent_dir = os.path.abspath(os.path.join(current_dir, '..'))
    print(f"\n[*] Scanning Parent Directory: {parent_dir}")
    try:
        parent_items = os.listdir(parent_dir)
        for item in parent_items:
            item_path = os.path.join(parent_dir, item)
            if os.path.isdir(item_path):
                print(f"    [DIR]  {item}")
            else:
                print(f"    [FILE] {item}")
    except Exception as e:
        print(f"    Error reading parent directory: {e}")

if __name__ == "__main__":
    scan_directories()
