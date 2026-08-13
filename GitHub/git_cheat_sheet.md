# Git Command Cheat Sheet (Daily & Interview Reference)

This document contains a quick reference list of daily Git commands and a specialized list of advanced commands frequently asked in SRE and DevOps technical interviews.

---

## 📋 Table of Contents
1.  [Daily Usage Git Commands](#1-daily-usage-git-commands)
2.  [Git Commands Frequently Asked in Interviews](#2-git-commands-frequently-asked-in-interviews)
3.  [Common Troubleshooting Scenarios](#3-common-troubleshooting-scenarios)

---

## 1. Daily Usage Git Commands

### Local Workspace Status & Changes
```bash
# View modified, staged, and untracked files
git status

# Stage specific file changes for the next commit
git add main.py

# Stage all changes (new, modified, and deleted files)
git add .

# Record staged changes as a new commit snapshot
git commit -m "feat: add oauth authentication"

# Show unstaged modifications since the last commit
git diff

# Unstage a file while retaining its modifications on disk
git restore --staged main.py

# Discard local changes in a file (revert to last committed state)
git restore main.py
```

### Branching & Collaborations
```bash
# Create a new local branch and switch to it immediately
git switch -c feature/login

# List all local branches
git branch

# Switch back to an existing branch
git switch main

# Fetch updates from remote and merge them into the current branch
git pull

# Push local commits on the active branch to the remote repository
git push origin feature/login

# Stash uncommitted changes to clean the working directory
git stash

# Re-apply the latest stashed changes and remove them from the stash stack
git stash pop
```

---

## 2. Git Commands Frequently Asked in Interviews

### Rewriting History
```bash
# Modify the message or contents of the latest commit
git commit --amend -m "fix: resolve correct token authentication"

# Start an interactive rebase to squash, edit, or reorder commits (last 3 commits)
git rebase -i HEAD~3
```

### Reverting & Resetting
```bash
# Create a new commit that records the exact opposite changes of a target commit
git revert a1b2c3d

# Reset branch pointer to a specific commit, keeping modifications in the staging index
git reset --soft a1b2c3d

# Reset branch pointer and discard all local changes since that commit
git reset --hard a1b2c3d
```

### Copying & Recovering Commits
```bash
# Copy a specific commit from another branch onto the current branch
git cherry-pick e4f5g6h

# Display the local reference updates log (history of HEAD switches and resets)
git reflog
```

### Advanced Diagnostics
```bash
# Start a binary search to find the exact commit that introduced a bug
git bisect start
git bisect bad                 # Mark current commit as broken
git bisect good a1b2c3d        # Mark a known working commit
# Git checks out intermediate commits; mark each as "good" or "bad"
git bisect reset               # Terminate bisect session when done

# Remove all untracked files and directories from the working directory
git clean -fd
```

---

## 3. Common Troubleshooting Scenarios

### Scenario A: "I committed changes to the wrong branch!"
To move the latest commit to a new branch and restore the current branch:
```bash
# 1. Create a new branch pointing to the current commit
git branch feature/new-logic

# 2. Reset the active branch to the previous commit
git reset --hard HEAD~1

# 3. Switch to the new branch containing your commit
git switch feature/new-logic
```

### Scenario B: "I accidentally ran a hard reset and lost my work!"
You can recover lost commits using the local reflog:
```bash
# 1. List all recent commits, including reset ones
git reflog

# 2. Locate the commit hash before the reset and checkout to a new branch
git checkout -b recover-branch a1b2c3d
```

### Scenario C: "How do I squashing multiple commits into one?"
Use interactive rebase:
```bash
# 1. Start rebase on the last 4 commits
git rebase -i HEAD~4

# 2. In the text editor, change 'pick' to 'squash' (or 's') for commits 2-4.
# 3. Save and close the editor. Edit the final combined commit message.
```
