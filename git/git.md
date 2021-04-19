## Git Cheatsheet


# Get current branch / Get branch and most recent commit
git branch / git show-branch 

# Clear cache
git rm -r --cached .

# Check history
git log --format=fuller

# Change Author & Committer
git filter-branch -f --env-filter "GIT_AUTHOR_NAME='Arnav Kohli'; GIT_AUTHOR_EMAIL='arnavkohli@gmail.com'; GIT_COMMITTER_NAME='Arnav Kohli'; GIT_COMMITTER_EMAIL='arnavkohli@gmail.com';"

## Force push
git push --force --tags origin HEAD:master

## Alternative

### Added Alias:
git config --global alias.change-commits '!'"f() { VAR=\$1; OLD=\$2; NEW=\$3; shift 3; git filter-branch --env-filter \"if [[ \\\"\$\`echo \$VAR\`\\\" = '\$OLD' ]]; then export \$VAR='\$NEW'; fi\" \$@; }; f"

### Change Author Email from commits in current branch
git change-commits GIT_AUTHOR_EMAIL "old" "new"

git change-commits GIT_AUTHOR_NAME "old" "new"

git change-commits GIT_COMMITTER_NAME "old" "new" 

git change-commits GIT_COMMITTER_EMAIL "old" "new" 

### Force push
git push --force --tags origin HEAD:master

