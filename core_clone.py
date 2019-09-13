import os
import subprocess

TRAVIS_BUILD_DIR = os.path.dirname(os.environ.get('TRAVIS_BUILD_DIR'))

repo_name = 'MCSDK-Automation-Framework-Core'

# Command to clone the repo
cmd = 'git clone https://{owner}:{token}@github.com/{owner}/{repo}.git {repo_folder}'.format(
    owner="salesforce-marketingcloud",
    token=os.environ.get("GITHUB_TOKEN"),
    repo=repo_name,
    repo_folder=os.path.join(TRAVIS_BUILD_DIR, repo_name)
)

result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)

print(result.stdout)