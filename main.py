import os
import subprocess
import shutil
import getpass
import requests
from colorama import init, Fore, Style

# Initialize colorama to work on all platforms
init(autoreset=True)

# --- Helper Functions ---


def run_command(command, working_dir):
    """A helper function to run a command and check for errors."""
    print(f"{Style.DIM}-> Running: {' '.join(command)}{Style.RESET_ALL}")
    result = subprocess.run(command, cwd=working_dir, capture_output=True, text=True)
    if result.returncode != 0:
        # A special check for 'git remote remove origin' which might fail harmlessly
        if command[1] == "remote" and command[2] == "remove":
            print(
                f"{Style.DIM}(Ignoring error for remote removal, as it may not have existed. Continuing...)"
            )
            return True  # Return True to not halt the script
        print(f"{Fore.RED}Error: {result.stderr.strip()}")
        return False
    print(f"{Fore.GREEN}Success!")
    return True


def create_gitignore(vault_path):
    """Creates a standard .gitignore file for Obsidian if one doesn't exist."""
    gitignore_path = os.path.join(vault_path, ".gitignore")
    if os.path.exists(gitignore_path):
        print(f"{Fore.YELLOW}A .gitignore file already exists. Skipping creation.")
        return True

    print(
        f"{Style.DIM}-> Creating a standard .gitignore file for Obsidian...{Style.RESET_ALL}"
    )
    gitignore_content = """
# Obsidian specific ignores
.obsidian/workspace.json
.obsidian/workspaces.json
.obsidian/publish.json
.obsidian/hotkeys.json
.obsidian/core-plugins.json
.obsidian/community-plugins.json
.obsidian/graph.json
.obsidian/local-graph.json
.obsidian/appearance.json
.obsidian/bookmarks.json
.obsidian/spellcheck.json
.obsidian/templates.json
.obsidian/types.json

# Cache files
.obsidian/cache/
"""
    try:
        with open(gitignore_path, "w") as f:
            f.write(gitignore_content.strip())
        print(f"{Fore.GREEN}Success! Created .gitignore")
        return True
    except IOError as e:
        print(f"{Fore.RED}Error creating .gitignore file: {e}")
        return False


def create_github_repo(repo_name, token):
    """Creates a new private repository on GitHub using the API."""
    api_url = "https://api.github.com/user/repos"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
    }
    data = {
        "name": repo_name,
        "description": "Obsidian vault for personal notes, created by obsidian-git-setup.",
        "private": True,
    }

    print(
        f"\n{Style.BRIGHT}📡 Creating new private repository '{repo_name}' on GitHub...{Style.RESET_ALL}"
    )

    try:
        response = requests.post(api_url, headers=headers, json=data)
        response.raise_for_status()
        print(f"{Fore.GREEN}✅ Success! Repository created on GitHub.")
        return True
    except requests.exceptions.HTTPError as err:
        if err.response.status_code == 422:
            print(
                f"{Fore.RED}❌ Error: Could not create repository. A repository with this name likely already exists on your GitHub account."
            )
        elif err.response.status_code == 401:
            print(
                f"{Fore.RED}❌ Error: Authentication failed. Your Personal Access Token is likely invalid, expired, or missing the 'repo' scope."
            )
        else:
            print(f"{Fore.RED}❌ Error creating GitHub repository: {err}")
        return False
    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}❌ A network error occurred: {e}")
        return False


# --- Main Script ---
def main():
    print(
        f"{Style.BRIGHT}--- Obsidian & GitHub Setup Helper (v2.0) ---{Style.RESET_ALL}"
    )
    print(
        "This script will create a private GitHub repo and set up your local vault to sync with it.\n"
    )

    # 1. Prerequisite Checks
    if not shutil.which("git"):
        print(
            f"{Fore.RED}❌ Error: Git is not installed. Please install it from https://git-scm.com/ and try again."
        )
        exit()
    print(f"{Fore.GREEN}✅ Git installation found.")

    # 2. Get User Input
    print(f"\n{Fore.CYAN}--- Step 1: Provide Your Details ---")
   # In the "Get User Input" section
vault_path = input(f"{Fore.YELLOW}Enter the FULL, absolute path to your Obsidian vault: {Style.RESET_ALL}")
    github_user = input(f"{Fore.YELLOW}Enter your GitHub username: {Style.RESET_ALL}")
    default_repo_name = (
        os.path.basename(os.path.normpath(vault_path)) or "obsidian-vault"
    )
    repo_name = input(
        f"{Fore.YELLOW}Enter the name for your new GitHub repo (e.g., {default_repo_name}): {Style.RESET_ALL}"
    )
    if not repo_name:
        repo_name = default_repo_name

    # 3. Get Personal Access Token
    print(f"\n{Fore.CYAN}--- Step 2: Provide Your GitHub Token ---")
    print(
        f"To create the repository, this script needs a GitHub Personal Access Token (PAT)."
    )
    print(f"1. Go to: {Fore.CYAN}https://github.com/settings/tokens/new")
    print(f"2. Create a token with the '{Fore.YELLOW}repo{Style.RESET_ALL}' scope.")
    print(f"3. Copy the token and paste it below (it will not be visible as you type).")
    try:
        github_token = getpass.getpass(
            f"{Fore.YELLOW}Enter your GitHub PAT: {Style.RESET_ALL}"
        )
    except getpass.GetPassWarning:
        github_token = input(f"{Fore.YELLOW}Enter your GitHub PAT: {Style.RESET_ALL}")

    # 4. Validate Path
    if not os.path.isdir(vault_path):
        print(f"\n{Fore.RED}❌ Error: The vault path does not exist: {vault_path}")
        exit()

    # 5. Create GitHub Repo via API
    if not create_github_repo(repo_name, github_token):
        print(f"\n{Fore.RED}Setup cannot continue. Please resolve the API error above.")
        exit()

    # 6. Local Git Setup
    print(f"\n{Style.BRIGHT}⚙️  Setting up your local vault...{Style.RESET_ALL}")

    is_git_repo = os.path.isdir(os.path.join(vault_path, ".git"))
    repo_url = f"https://github.com/{github_user}/{repo_name}.git"

    if is_git_repo:
        print(f"{Fore.YELLOW}Vault is already a Git repo. Reconfiguring remote...")
        if not (
            run_command(["git", "remote", "remove", "origin"], vault_path)
            and run_command(["git", "remote", "add", "origin", repo_url], vault_path)
            and run_command(
                ["git", "config", "--local", "commit.gpgsign", "false"], vault_path
            )
        ):
            print(f"{Fore.RED}Failed to reconfigure the existing Git repository.")
            exit()
    else:
        if not (
            run_command(["git", "init"], vault_path)
            and run_command(
                ["git", "config", "--local", "commit.gpgsign", "false"], vault_path
            )
            and run_command(["git", "remote", "add", "origin", repo_url], vault_path)
            and run_command(["git", "branch", "-M", "main"], vault_path)
            and create_gitignore(vault_path)
        ):
            print(f"{Fore.RED}Failed to initialize the local Git repository.")
            exit()

    # 7. Offer to create first commit
    print(f"\n{Fore.CYAN}--- Step 3: Finalize Setup ---")
    initial_commit = input(
        f"{Fore.YELLOW}Would you like to create an initial commit with all your current notes? (y/n): {Style.RESET_ALL}"
    ).lower()
    if initial_commit == "y":
        print("Creating initial commit...")
        if run_command(["git", "add", "."], vault_path) and run_command(
            ["git", "commit", "-m", "Initial commit of vault"], vault_path
        ):
            print(
                f"\n{Fore.GREEN}✅ All done! Your vault is set up and your first commit is ready."
            )
            print(
                f"   To upload your notes to GitHub, run this command from inside your vault:"
            )
            print(f"   {Style.BRIGHT}git push --set-upstream origin main{Style.NORMAL}")
            print(
                f"   (You will need to use your Personal Access Token as the password one last time)."
            )
        else:
            print(
                f"{Fore.RED}Could not create the initial commit. You may need to do it manually."
            )
    else:
        print(f"\n{Fore.GREEN}✅ All done! Your vault is configured.")
        print("   Remember to create your first commit and push it to GitHub manually.")


if __name__ == "__main__":
    main()
