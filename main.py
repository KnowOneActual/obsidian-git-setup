import os
import subprocess
import shutil


def run_command(command, working_dir):
    """A helper function to run a command and check for errors."""
    print(f"-> Running: {' '.join(command)}")
    result = subprocess.run(command, cwd=working_dir, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr.strip()}")
        return False
    print("Success!")
    return True


# --- Main Script ---
print("--- Obsidian & GitHub Setup Helper ---")
print(
    "This script will initialize a Git repository in your vault and prepare it for GitHub.\n"
)

# 1. Prerequisite Check: Is Git installed?
if not shutil.which("git"):
    print("❌ Error: Git is not installed or not found in your system's PATH.")
    print(
        "Please install Git and try again. You can download it from https://git-scm.com/"
    )
    exit()
else:
    print("✅ Git installation found.")

# 2. Get user input
vault_path = input("Enter the full path to your Obsidian vault: ")
github_user = input("Enter your GitHub username: ")
repo_name = input(
    f"Enter the name for your new GitHub repo (e.g., {os.path.basename(vault_path) or 'obsidian-vault'}): "
)

# 3. Validate the path exists
if not os.path.isdir(vault_path):
    print(f"\n❌ Error: The vault path you entered does not exist: {vault_path}")
    exit()

# 4. User Confirmation Step
print("\n--- Configuration Summary ---")
print(f"Obsidian Vault Path: {vault_path}")
print(f"GitHub Username:       {github_user}")
print(f"New Repository Name:   {repo_name}")
print("-----------------------------")

confirm = input("Is this correct? (y/n): ").lower()
if confirm != "y":
    print("Setup cancelled by user.")
    exit()

# 5. Define the commands to run
repo_url = f"https://github.com/{github_user}/{repo_name}.git"
commands_to_run = [
    ["git", "init"],
    ["git", "config", "--local", "commit.gpgsign", "false"],
    ["git", "remote", "add", "origin", repo_url],
    ["git", "branch", "-M", "main"],
]

# 6. Run the commands
print("\n🚀 Initializing your vault. This will not affect your notes.")
for cmd in commands_to_run:
    if not run_command(cmd, working_dir=vault_path):
        print("\nSetup failed at a critical step. Please review the error above.")
        exit()

# 7. Provide final, clear instructions for the user
print("\n✅ Local setup complete!")
print("--- Your Final Manual Steps ---")
print(f"1. On GitHub.com, create a new PRIVATE repository named: {repo_name}")
print(
    "2. Go to your GitHub Developer Settings to create a Personal Access Token (PAT)."
)
print("   - Direct Link: https://github.com/settings/tokens/new")
print("   - In 'Select scopes', check the box for 'repo'.")
print("   - Click 'Generate token' and copy it immediately!")
print("\n3. Finally, in a terminal inside your vault, run these three commands:")
print("   git add .")
print('   git commit -m "Initial commit"')
print("   git push -u origin main  (Use your new PAT as the password when prompted)")
