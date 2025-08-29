import os
import subprocess


def run_command(command, working_dir):
    """A helper function to run a command and check for errors."""
    print(f"-> Running: {' '.join(command)}")
    result = subprocess.run(command, cwd=working_dir, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        return False
    print("Success!")
    return True


# --- Main Script ---
print("--- Obsidian & GitHub Setup Helper ---")

# 1. Get user input
vault_path = input("Enter the full path to your Obsidian vault: ")
github_user = input("Enter your GitHub username: ")
repo_name = input(
    f"Enter the name for your new GitHub repo (e.g., {os.path.basename(vault_path)}-vault): "
)

# 2. Validate the path exists
if not os.path.isdir(vault_path):
    print("\nError: The vault path you entered does not exist.")
    exit()

# 3. Define the commands to run
repo_url = f"https://github.com/{github_user}/{repo_name}.git"
commands_to_run = [
    ["git", "init"],
    ["git", "config", "--local", "commit.gpgsign", "false"],
    ["git", "remote", "add", "origin", repo_url],
    ["git", "branch", "-M", "main"],
]

# 4. Run the commands
print("\nInitializing your vault. This will not affect your notes.")
for cmd in commands_to_run:
    if not run_command(cmd, working_dir=vault_path):
        print("\nSetup failed at a critical step. Please review the error above.")
        exit()

# 5. Provide final, clear instructions for the user
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
