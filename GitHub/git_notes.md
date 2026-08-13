# Git Comprehensive Reference Notes

This document covers Git concepts, internal mechanics, branching workflows, stash, reflog, revert strategies, and command operations.

---

## 📋 Table of Contents
*   [Core Architecture & States](#core-architecture--states)
*   [Essential Repository Lifecycle](#essential-repository-lifecycle)
*   [Branching, Merging & Rebasing](#branching-merging--rebasing)
*   [Advanced Git Control (Stash, Reflog, Reset)](#advanced-git-control-stash-reflog-reset)
*   [Git Diagnostics & Conflict Resolution](#git-diagnostics--conflict-resolution)

---

## Core Architecture & States

Git is a **distributed version control system (DVCS)**. Unlike centralized systems (like SVN) that rely on a single server, every Git clone contains a full backup of the project history, metadata, and objects.

### The Three Git Areas
Git manages code lifecycle transitions across three main logical stages:

```
[ Working Directory ] -- (git add) --> [ Staging Area / Index ] -- (git commit) --> [ Local Repository (.git) ]
```

1.  **Working Directory**: The actual files on your local disk that you are editing.
2.  **Staging Area (Index)**: A preparation buffer file (`.git/index`) containing a snapshot of the changes that will be packaged in the next commit.
3.  **Local Repository**: The `.git` directory containing all committed versions, branches, configuration settings, and historic objects.

### Git File States
*   **Untracked**: New local files not yet monitored by Git.
*   **Unmodified**: Files in the working directory matching the latest commit.
*   **Modified**: Tracked files with local changes that are not staged.
*   **Staged**: Modified files added to the index, ready to be committed.

---

## Essential Repository Lifecycle

### Configuration
Set user details globally (saved in `~/.gitconfig`):
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### Initializing and Cloning
```bash
# Initialize a new local Git repository in the current folder
git init

# Clone an existing remote repository onto your local disk
git clone https://github.com/user/repo.git
```

### Recording Changes
```bash
# Stage a specific file for commit
git add main.py

# Stage all changes (new, modified, and deleted files) recursively
git add .

# Record staged changes as a new commit snapshot
git commit -m "feat: integrate bigquery data agent"

# Stage all tracked files and commit them in a single command
git commit -am "fix: correct API authorization keys"
```

### Reviewing History
```bash
# Show status of working directory (staged, unstaged, untracked files)
git status

# Display a flat commit history log
git log

# Display commit log formatted as a single line per commit with a graph
git log --oneline --graph --decorate
```

---

## Branching, Merging & Rebasing

A branch in Git is simply a lightweight, mutable pointer to a specific commit. The default branch name is typically `main` or `master`.

### Branch Management
```bash
# List all local branches (active branch is marked with *)
git branch

# Create a new local branch
git branch feature/auth

# Switch the working directory to a specific branch
git checkout feature/auth

# Create a new branch and switch to it immediately (modern command)
git switch -c feature/auth
```

### Merging vs. Rebasing

#### Merging
Integrates changes from a source branch into a target branch by creating a **Merge Commit**. This preserves history but can result in complex graph paths.
```bash
# Switch to target branch and merge source branch
git checkout main
git merge feature/auth
```

#### Rebasing
Re-applies commits from the current branch on top of another base tip, creating a **linear commit history**. It rewrites history by generating new commits.
```bash
# Switch to feature branch and rebase it onto main
git checkout feature/auth
git rebase main
```
> [!WARNING]
> **Never rebase commits that have been pushed to a public remote repository**. Rebasing rewrites commit histories, which can disrupt other developers working on the same branch.

---

## Advanced Git Control (Stash, Reflog, Reset)

### Git Stash
Temporarily shelves (saves) uncommitted local changes to clear the working directory without committing, allowing you to switch branches quickly.
```bash
# Save active uncommitted changes to the stash stack
git stash save "work-in-progress on login"

# List all saved stashes
git stash list

# Re-apply the latest stashed changes and remove them from the stash stack
git stash pop

# Re-apply a specific stash (e.g., stash@{1}) without removing it from the stack
git stash apply stash@{1}

# Clear the entire stash stack
git stash clear
```

### Git Reflog
Logs every local reference modification (checkout, commit, rebase, reset). Useful for recovering lost commits or branches.
```bash
# Display the local reference updates log
git reflog

# Restore a branch to a specific historic state using a reflog pointer (e.g., HEAD@{5})
git reset --hard HEAD@{5}
```

### Git Reset vs. Revert

#### Reset
Moves the current branch pointer to a specific commit. This changes history.
*   `--soft`: Retains local changes in the staging area.
*   `--mixed` (default): Retains local changes in the working directory but unstages them.
*   `--hard`: Discards all staged and local working directory changes completely.
```bash
# Discard all changes since a specific commit
git reset --hard a1b2c3d
```

#### Revert
Creates a new commit that records the exact opposite changes of a target commit, preserving history without altering past logs.
```bash
# Revert changes introduced by a specific commit
git revert a1b2c3d
```

---

## Git Diagnostics & Conflict Resolution

### Resolving Merge Conflicts
Merge conflicts occur when changes are made to the same lines of a file on different branches, and Git cannot merge them automatically.

1.  Identify conflicting files using `git status`.
2.  Open the files and locate conflict markers:
    ```
    <<<<<<< HEAD
    Local changes on target branch
    =======
    Incoming changes from source branch
    >>>>>>> source_branch
    ```
3.  Edit the file to resolve the conflict, remove the markers, and save.
4.  Stage and commit the resolved files:
    ```bash
    git add resolved_file.py
    git commit -m "merge: resolve authorization conflict"
    ```

### Cherry-Picking
Applies the changes from a specific commit on another branch to your current branch.
```bash
git cherry-pick e4f5g6h
```
