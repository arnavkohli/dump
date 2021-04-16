import os, requests, json
from datetime import datetime

# My Wrappers
def time_that_shit(func):
	def not_good_with_names(*args, **kwargs):
		timeStart = datetime.now()
		func(*args, **kwargs)
		timeEnd = datetime.now()
		print (f"[{func.__name__}] duration: {(timeEnd - timeStart).seconds / 60} minutes")
	return not_good_with_names

# Helper functions
def clone_and_filter_branch(URL):
	'''
		Clones the repo locally, filters the branch, pushes the changes, deletes the cloned dir.
	'''
	NAME = URL.split('/')[-1].split('.')[0]

	# Clone the repo
	os.system(f"git clone {URL}")

	# cd inside dir
	os.chdir(NAME)

	# filter the branch and push the changes
	os.system(f'''git filter-branch -f --env-filter "GIT_AUTHOR_NAME='{GIT_AUTHOR_NAME}'; GIT_AUTHOR_EMAIL='{GIT_AUTHOR_EMAIL}'; GIT_COMMITTER_NAME='{GIT_COMMITTER_NAME}'; GIT_COMMITTER_EMAIL='{GIT_COMMITTER_EMAIL}';"''')
	os.system("git push --force --tags origin HEAD:master")

	# cd back to parent dir and rm cloned repo
	os.chdir("..")
	os.system(f"rm -rf {NAME}")

# Mains
@time_that_shit
def update_author_and_committer(repo_names, github_username):
	'''
		Constructs clone URLs for each repo and updates them.
	'''
	urls = [f"https://github.com/{GITHUB_USERNAME}/{repo_name}" for repo_name in repo_names]
	for index, URL in enumerate(urls):
		print (f"[{index + 1} / {len(urls)}]")
		clone_and_filter_branch(URL)

	print (f"[INFO] update_author_and_committer has finished running")

@time_that_shit
def update_author_and_committer_for_public_repos(github_username):
	'''
		Scrapes clone URLs of the public repos (fork=False) of the user and updates them.
	'''
	URL = f"https://api.github.com/users/{github_username}/repos"
	all_repos = requests.get(URL).json()

	count = 0
	for index, repo in enumerate(all_repos):
		if not repo.get('fork'):
			clone_url = repo.get("clone_url")
			print ("[***********] Starting", clone_url)
			clone_and_filter_branch(clone_url)
			print (f"[***********] Count: {count + 1} / {len(all_repos)}")
			count += 1

	print (f"[INFO] update_author_and_committer_for_public_repos has finished running")

if __name__ == '__main__':
	GIT_AUTHOR_NAME     = ""
	GIT_AUTHOR_EMAIL    = ""
	GIT_COMMITTER_NAME  = ""
	GIT_COMMITTER_EMAIL = ""
	GITHUB_USERNAME = ""
	REPO_NAMES = [
		GITHUB_USERNAME
	]
	
	# update_author_and_committer(repo_names=REPO_NAMES, github_username=GITHUB_USERNAME)
	# update_author_and_committer_for_public_repos(github_username=GITHUB_USERNAME)
