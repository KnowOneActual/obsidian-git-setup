import os
import subprocess
import shutil
from colorama import init, Fore, Style

# Initialize colorama to work on all platforms
init(autoreset=True)


def run_command(command, working_dir):
    """A helper function to run a command and check for errors."""
    print(f"{Style.DIM}-> Running: {' '.join(command)}{Style.RESET_ALL}")
    result = subprocess.run(command, cwd=working_dir, capture_output=True, text=True)
    if result.returncode != 0:
        # Print the error in red
        print(f"{Fore.RED}Error: {result.stderr.strip()}")
        return False
    # Print success in green
    print(f"{Fore.GREEN}Success!")
    return True


# --- Main Script ---
print(f"{Style.BRIGHT}--- Obsidian & GitHub Setup Helper ---{Style.RESET_ALL}")
print(
    "This script will initialize a Git repository in your vault and prepare it for GitHub.\n"
)

# 1. Prerequisite Check: Is Git installed?
if not shutil.which("git"):
    print(
        f"{Fore.RED}❌ Error: Git is not installed or not found in your system's PATH."
    )
    print(
        f"{Fore.YELLOW}Please install Git and try again. You can download it from https://git-scm.com/"
    )
    exit()
else:
    print(f"{Fore.GREEN}✅ Git installation found.")

# 2. Get user input
vault_path = input(
    f"{Fore.YELLOW}Enter the full path to your Obsidian vault: {Style.RESET_ALL}"
)
github_user = input(f"{Fore.YELLOW}Enter your GitHub username: {Style.RESET_ALL}")
repo_name = input(
    f"{Fore.YELLOW}Enter the name for your new GitHub repo (e.g., {os.path.basename(vault_path) or 'obsidian-vault'}): {Style.RESET_ALL}"
)

# 3. Validate the path exists
if not os.path.isdir(vault_path):
    print(
        f"\n{Fore.RED}❌ Error: The vault path you entered does not exist: {vault_path}"
    )
    exit()

# 4. User Confirmation Step
print(f"\n{Fore.CYAN}--- Configuration Summary ---")
print(f"{Fore.CYAN}Obsidian Vault Path: {vault_path}")
print(f"{Fore.CYAN}GitHub Username:       {github_user}")
print(f"{Fore.CYAN}New Repository Name:   {repo_name}")
print(f"{Fore.CYAN}-----------------------------")

confirm = input(f"{Fore.YELLOW}Is this correct? (y/n): {Style.RESET_ALL}").lower()
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
print(
    f"\n{Style.BRIGHT}🚀 Initializing your vault. This will not affect your notes.{Style.RESET_ALL}"
)
for cmd in commands_to_run:
    if not run_command(cmd, working_dir=vault_path):
        print(
            f"\n{Fore.RED}Setup failed at a critical step. Please review the error above."
        )
        exit()

# 7. Provide final, clear instructions for the user
print(f"\n{Fore.GREEN}✅ Local setup complete!")
print(f"{Style.BRIGHT}--- Your Final Manual Steps ---{Style.RESET_ALL}")
print(
    f"1. On GitHub.com, create a new {Fore.YELLOW}PRIVATE{Style.RESET_ALL} repository named: {repo_name}"
)
print(
    "2. Go to your GitHub Developer Settings to create a Personal Access Token (PAT)."
)
print(f"   - Direct Link: {Fore.CYAN}https://github.com/settings/tokens/new")
print(
    f"   - In 'Select scopes', check the box for '{Fore.YELLOW}repo{Style.RESET_ALL}'."
)
print("   - Click 'Generate token' and copy it immediately!")
print("\n3. Finally, in a terminal inside your vault, run these three commands:")
print(f"   {Style.BRIGHT}git add .")
print(f'   {Style.BRIGHT}git commit -m "Initial commit"')
print(
    f"   {Style.BRIGHT}git push -u origin main{Style.NORMAL}  (Use your new PAT as the password when prompted)"
)
