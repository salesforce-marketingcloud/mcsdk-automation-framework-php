import os
from bootstrap import config, config_dir, templates_dir, GITHUB_TOKEN
from processes.Git import Git
from processes.CodeGenerator import CodeGenerator
from processes.Codebase import Codebase

# Vars for the integration run
repo_core_owner = config['repos']['core']['owner']
repo_core_name = config['repos']['core']['name']
repo_core_dir = config['repos']['core']['dir']

repo_sdk_owner = config['repos']['sdk']['owner']
repo_sdk_name = config['repos']['sdk']['name']
repo_sdk_dir = config['repos']['sdk']['dir']

branch_name = '1.0'
auto_branch = branch_name + '_automation'

# Cloning the CORE repository in order to have access to swagger
core_repo = Git(GITHUB_TOKEN, repo_core_owner, repo_core_name, repo_core_dir)
clone_status_code = core_repo.clone()

# Check if repo folder exists or the clone just failed
if 0 != clone_status_code and not os.path.isdir(repo_core_dir):
    print('Could not clone repository')
    exit(255)

core_repo.checkout(branch_name)

# Cloning the SDK repo
sdk_repo = Git(GITHUB_TOKEN, repo_sdk_owner, repo_sdk_name, repo_sdk_dir)
clone_status_code = sdk_repo.clone()

# Check if repo folder exists or the clone just failed
if 0 != clone_status_code and not os.path.isdir(repo_sdk_dir):
    print('Could not clone repository')
    exit(255)

if sdk_repo.checkout(branch_name) != 0:
    print("Could not checkout the base branch for the SDK")
    exit(255)

if sdk_repo.checkout(auto_branch) != 0:
    print("Could not checkout the integration branch for the SDK")
    exit(255)

# code generation
generator = CodeGenerator(config, config_dir, templates_dir, repo_sdk_dir)
generator.generate_sdk()
generator.generate_client()

# code base operations
codebase = Codebase(config, repo_sdk_dir)
if codebase.install_dependencies() != 0:
    print('Dependencies failed to install')
    exit(255)

if codebase.run_tests() != 0:
    print("Unit tests failed")
    exit(255)

# Finishing touches
if sdk_repo.stage_changes() == 0 and sdk_repo.commit('Auto-update') == 0:
    # Doing the push & PR (cascaded for readability)
    if sdk_repo.push('origin', auto_branch, True) == 0:
        sdk_repo.make_pull_request(branch_name, auto_branch)

exit(0)
