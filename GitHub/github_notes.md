# GitHub Platform & Collaboration Reference Notes

This document covers GitHub authentication, collaboration models (PRs, Forking), repository settings, environments, secret keys management, and the GitHub CLI (`gh`).

---

## 📋 Table of Contents
*   [Authentication & Security](#authentication--security)
*   [Collaboration Models (Pull Requests & Forking)](#collaboration-models-pull-requests--forking)
*   [Environments, Secrets & Variables](#environments-secrets--variables)
*   [GitHub CLI (`gh`) Reference](#github-cli-gh-reference)
*   [Repository Features & Packages](#repository-features--packages)

---

## Authentication & Security

GitHub requires secure authentication methods to connect local Git commands to remote repositories.

### SSH Authentication
Uses asymmetric public-private key pairs to authenticate without passwords.
1.  **Generate SSH Key locally**:
    ```bash
    ssh-keygen -t ed25519 -C "your.email@example.com"
    ```
2.  **Start ssh-agent and add key**:
    ```bash
    eval "$(ssh-agent -s)"
    ssh-add ~/.ssh/id_ed25519
    ```
3.  **Add public key to GitHub**: Copy the content of `~/.ssh/id_ed25519.pub` and add it under GitHub **Settings -> SSH and GPG keys**.

### Personal Access Tokens (PATs)
Used for token-based HTTPS authentication. Always prefer **Fine-Grained Personal Access Tokens**, which allow you to set specific expiration times and limit permissions to designated repositories.

### GPG Commit Signing
Configuring GPG keys allows GitHub to sign commits, verifying that they originate from you.
```bash
# Set Git to sign all commits automatically
git config --global commit.gpgsign true
```

---

## Collaboration Models (Pull Requests & Forking)

### Shared Repository Branching Model
Used by internal or small project teams.
1.  Developers clone the primary repository directly.
2.  Create feature branches (e.g., `feature/login`).
3.  Push branches to the origin and open a **Pull Request (PR)** to merge into the `main` branch.

### Fork-and-Pull Model
Commonly used for public open-source contributions.
1.  **Fork**: Creates a personal copy of another user's repository under your own GitHub account.
2.  Clone your fork locally, make changes, and push them to your fork.
3.  Open a Pull Request from your fork back to the upstream parent repository.

### Syncing a Fork with Upstream Changes
```bash
# Add upstream parent remote target repository link
git remote add upstream https://github.com/original-owner/original-repo.git

# Fetch latest upstream commits
git fetch upstream

# Merge upstream main commits into your local main branch
git checkout main
git merge upstream/main

# Push updates to your origin fork on GitHub
git push origin main
```

---

## Environments, Secrets & Variables

### Repository Secrets
Encrypted variables used to store sensitive data (like API tokens or SSH keys) for GitHub Actions. They are injected at runtime and masked in logs.
*   Configure under: **Settings -> Secrets and variables -> Actions**.

### Environments & Deployment Gates
Environments are used to model target deployment destinations (like `development`, `staging`, or `production`).
*   **Protection Rules**: You can require manual approval from designated users before a workflow run can proceed in that environment.
*   **Environment Secrets**: Secrets restricted to specific environments, overriding repository-wide secrets with the same name.

### Configuration Variables
Non-sensitive variables (like region names or config flags) that can be stored in plain text and accessed in workflows using `${{ vars.VARIABLE_NAME }}`.

---

## GitHub CLI (`gh`) Reference

The official command-line interface for GitHub, allowing you to manage issues, pull requests, and releases directly from your terminal.

```bash
# Authenticate the CLI tool with your GitHub account
gh auth login

# List open Pull Requests in the current repository
gh pr list

# Create a new Pull Request interactively
gh pr create --title "feat: add user auth" --body "Implements OAuth2 login"

# Review and merge a Pull Request
gh pr merge 123 --merge

# Create a new GitHub issue
gh issue create --title "bug: database connection timeout" --body "Logs show 504 gateway timeouts"

# Clone a repository using its GitHub shorthand name
gh repo clone bgiriaicloud/Agentic-ai-projects
```

---

## Repository Features & Packages

### GitHub Issues & Projects
*   **Issues**: Used to track bugs, tasks, and feature requests.
*   **Projects**: A Kanban-style planning tool that organizes issues and PRs into custom columns (e.g., "To Do", "In Progress", "Done").

### Releases & Tags
*   **Git Tags**: Static pointers to specific commits in history, typically matching version names (e.g., `v1.0.0`).
*   **GitHub Releases**: Packages containing release notes and binary assets built from a Git tag.

### GitHub Packages (GHCR)
The GitHub Container Registry, used to host Docker container images, npm packages, or NuGet dependencies directly within GitHub. Can be authenticated in workflows using the automatic `${{ secrets.GITHUB_TOKEN }}`.
