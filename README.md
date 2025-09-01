
# Obsidian Git Setup
[![Project Status: WIP – Initial development in progress.](https://img.shields.io/badge/Project%20Status-WIP-orange.svg)](https://github.com/knowoneactual/obsidian-git-setup)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Language: Python](https://img.shields.io/badge/Language-Python-blue.svg)](https://www.python.org/)
[![GitHub issues](https://img.shields.io/github/issues/knowoneactual/obsidian-git-setup.svg)](https://github.com/knowoneactual/obsidian-git-setup/issues)
[![GitHub stars](https://img.shields.io/github/stars/knowoneactual/obsidian-git-setup.svg)](https://github.com/knowoneactual/obsidian-git-setup/stargazers)

# Still in testing. Use with care.

A simple command-line utility to quickly and safely initialize an Obsidian vault as a Git repository and connect it to a new private GitHub repository for syncing and backup.

This script is designed to automate the tedious and sometimes error-prone process of setting up Git for your Obsidian notes, especially for users who want a reliable, free, cross-platform sync solution for their desktop machines.


## The Problem It Solves

Setting up Git for Obsidian manually involves a series of specific commands. It's easy to miss a step or run into common issues, such as:



* Forgetting to initialize the repository in the correct folder.
* Encountering gpg failed to sign the data errors if you have GPG signing enabled globally.
* Mistyping the remote repository URL.

This script aims to handle all of that for you with a simple, interactive prompt.


## Current Status

🚧 **Work in Progress** 🚧

This project is in the very early stages of development. The core concept is defined, and the initial script is being built.


## How to Use (Planned)

The final script will guide you through a series of prompts:



1. Run the script from your terminal: python main.py
2. Enter the full path to your Obsidian vault.
3. Provide your GitHub username.
4. Choose a name for your new remote repository.

The script will then perform the necessary setup and provide you with the final manual steps (like creating the repository on GitHub and generating a Personal Access Token).


## Project Roadmap



* [ X ] Create the core Python script to run Git commands.
* [ X ] Add interactive user prompts for vault path, username, and repo name.
* [ X ] Implement a prerequisite check to ensure git is installed.
* [ X ] Add validation to make sure the user-provided vault path exists.
* [ ] Include clear, user-friendly instructions for the final manual steps.
* [ X ] Add color-coded output for better readability (e.g., green for success, red for errors).


## Contributing

This is currently a personal project, but suggestions and contributions will be welcome once the initial version is complete. Please feel free to open an issue to discuss any ideas.
