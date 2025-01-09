# Git Branch Auto Exported in ZSH

In your `.zshrc` add the following:

```
# Function to determine the current git branch and export it to an env variable
function set_git_branch() {
  # Attempt to retrieve the current branch name
  local branch
  branch=$(git rev-parse --abbrev-ref HEAD 2>/dev/null)

  # If we're in a Git repository (branch name is non-empty), set the variable
  if [[ -n "$branch" && "$branch" != "HEAD" ]]; then
    export GIT_BRANCH="$branch"
  else
    # Unset it if not in a Git repo
    unset GIT_BRANCH
  fi
}

# Make sure we have add-zsh-hook available
autoload -U add-zsh-hook

# Register the function to run just before each new prompt
add-zsh-hook precmd set_git_branch
```
