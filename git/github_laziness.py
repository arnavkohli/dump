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
def clone_and_filter_branch(url, git_author_name, git_author_email, git_committer_name, git_committer_email):
	'''
		Clones the repo locally, filters the branch, pushes the changes, deletes the cloned dir.
	'''
	NAME = url.split('/')[-1].split('.')[0]

	# Clone the repo
	os.system(f"git clone {url}")

	# cd inside dir
	os.chdir(NAME)

	# filter the branch and push the changes
	os.system(f'''git filter-branch -f --env-filter "GIT_AUTHOR_NAME='{git_author_name}'; \
		GIT_AUTHOR_EMAIL='{git_author_email}'; \
		GIT_COMMITTER_NAME='{git_committer_name}'; \
		GIT_COMMITTER_EMAIL='{git_committer_email}';"''')

	os.system("git push --force --tags origin HEAD:master")

	# cd back to parent dir and rm cloned repo
	os.chdir("..")
	os.system(f"rm -rf {NAME}")

# Mains
@time_that_shit
def update_author_and_committer(repo_names, github_info):
	'''
		Constructs clone urls for each repo and updates them.
	'''
	urls = [f"https://github.com/{github_info.get('GITHUB_USERNAME')}/{repo_name}" for repo_name in repo_names]
	for index, url in enumerate(urls):
		print (f"[{index + 1} / {len(urls)}]")
		clone_and_filter_branch(
			url=url,
			git_author_name=github_info.get('GIT_AUTHOR_NAME'),
			git_author_email=github_info.get('GIT_AUTHOR_EMAIL'),
			git_committer_name=github_info.get('GIT_COMMITTER_NAME'),
			git_committer_email=github_info.get('GIT_COMMITTER_EMAIL')
		)

	print (f"[INFO] update_author_and_committer has finished running")

@time_that_shit
def update_author_and_committer_for_public_repos(github_info):
	'''
		Scrapes clone urls of the public repos (fork=False) of the user and updates them.
	'''
	url = f"https://api.github.com/users/{github_info.get('GITHUB_USERNAME')}/repos"
	all_repos = requests.get(url).json()

	count = 0
	for index, repo in enumerate(all_repos):
		print (repo)
		if not repo.get('fork'):
			clone_url = repo.get("clone_url")
			print ("[***********] Starting", clone_url)
			clone_and_filter_branch(
				url=clone_url,
				git_author_name=github_info.get('GIT_AUTHOR_NAME'),
				git_author_email=github_info.get('GIT_AUTHOR_EMAIL'),
				git_committer_name=github_info.get('GIT_COMMITTER_NAME'),
				git_committer_email=github_info.get('GIT_COMMITTER_EMAIL')
			)
			print (f"[***********] Count: {count + 1} / {len(all_repos)}")
			count += 1

	print (f"[INFO] update_author_and_committer_for_public_repos has finished running")

if __name__ == '__main__':
	GITHUB_INFO = {
		"GITHUB_USERNAME" : "arnavkohli",
		"GIT_AUTHOR_NAME"     : "Arnav Kohli",
		"GIT_AUTHOR_EMAIL"    : "arnavkohli@gmail.com",
		"GIT_COMMITTER_NAME"  : "Arnav Kohli",
		"GIT_COMMITTER_EMAIL" : "arnavkohli@gmail.com"
	}
	REPO_NAMES = [
		"QuizApp"
	]

	update_author_and_committer(REPO_NAMES, GITHUB_INFO)
	#update_author_and_committer_for_public_repos(GITHUB_INFO)
