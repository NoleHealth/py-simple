# Git Commands & Workflow

This document outlines common Git commands and a simple workflow for contributing to the project.

## Basic Commands

### Repository Status & Information
```bash
git status                  # Show working tree status
git log --oneline          # Show commit history (compact)
git log --graph --oneline  # Show commit history with branch visualization
git diff                   # Show unstaged changes
git diff --staged          # Show staged changes
```

### Staging & Committing
```bash
git add <file>             # Stage specific file
git add .                  # Stage all changes
git add -A                 # Stage all changes including deletions
git commit -m "message"    # Commit with message
git commit -am "message"   # Stage all tracked files and commit
```

### Branch Management
```bash
git branch                 # List local branches
git branch -r              # List remote branches
git branch -a              # List all branches
git branch <branch-name>   # Create new branch
git checkout <branch-name> # Switch to branch
git checkout -b <branch>   # Create and switch to new branch
git branch -d <branch>     # Delete branch (safe)
git branch -D <branch>     # Delete branch (force)
```

### Remote Operations
```bash
git remote -v              # Show remote repositories
git fetch                  # Fetch changes from remote
git pull                   # Fetch and merge changes
git push                   # Push changes to remote
git push -u origin <branch> # Push and set upstream
git push origin --delete <branch> # Delete remote branch
```

## Simple Git Workflow

### 1. Start New Feature
```bash
# Ensure you're on main and up to date
git checkout main
git pull origin main

# Create feature branch
git checkout -b feature/your-feature-name
```

### 2. Make Changes
```bash
# Make your code changes...

# Check what's changed
git status
git diff

# Stage and commit changes
git add .
git commit -m "Add: implement your feature description"
```

### 3. Push Changes
```bash
# Push feature branch to remote
git push -u origin feature/your-feature-name
```

### 4. Create Pull Request
```bash
# Using GitHub CLI (if available)
gh pr create --title "Add your feature" --body "Description of changes"

# Or visit GitHub web interface to create PR
```

### 5. After PR is Merged
```bash
# Switch back to main
git checkout main

# Pull latest changes
git pull origin main

# Delete local feature branch
git branch -d feature/your-feature-name
```

## Commit Message Conventions

Use clear, descriptive commit messages with these prefixes:

- `Add:` New feature or functionality
- `Fix:` Bug fixes
- `Update:` Improvements to existing features
- `Refactor:` Code refactoring without functionality changes
- `Docs:` Documentation changes
- `Test:` Adding or updating tests
- `Style:` Code formatting, no functionality changes

### Examples
```bash
git commit -m "Add: user authentication with JWT tokens"
git commit -m "Fix: handle empty API response gracefully"
git commit -m "Update: improve error logging with more context"
git commit -m "Docs: update installation instructions for uv"
```

## Useful Shortcuts

### Undo Changes
```bash
git checkout -- <file>     # Discard changes in working directory
git reset HEAD <file>      # Unstage file
git reset --soft HEAD~1    # Undo last commit, keep changes staged
git reset --hard HEAD~1    # Undo last commit, discard changes
```

### Stash Changes
```bash
git stash                  # Stash current changes
git stash pop              # Apply and remove latest stash
git stash list             # List all stashes
git stash apply stash@{n}  # Apply specific stash
```

### View History
```bash
git blame <file>           # Show who changed each line
git show <commit-hash>     # Show specific commit details
git log --grep="keyword"   # Search commits by message
git log --author="name"    # Show commits by author
```