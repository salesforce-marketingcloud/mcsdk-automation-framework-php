import os
from validator.Environment import check_env
from utils.Config import Config

# Check if the environment if properly set up
check_env()

# Define constants
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')
TRAVIS_BUILD_DIR = os.path.dirname(os.environ.get('TRAVIS_BUILD_DIR'))
BUILDER_REPO_DIR = os.path.dirname(os.path.dirname(os.getcwd()))

# Define global vars
root_dir = os.sep.join(os.path.abspath(__file__).split(os.sep)[:-3])
resources_dir = os.path.join(root_dir, 'resources')
config_dir = os.path.join(resources_dir, 'config')
templates_dir = os.path.join(resources_dir, 'templates')

# Loading the configuration
config = Config.from_yaml(config_dir)
config['repos']['core']['dir'] = os.path.abspath(os.path.join(TRAVIS_BUILD_DIR, config['repos']['core']['name']))
config['repos']['sdk']['dir'] = os.path.abspath(os.path.join(TRAVIS_BUILD_DIR, config['repos']['sdk']['name']))

# Custom stuff...manual work for now
rep = ['{%repos_core_dir%}', config['repos']['core']['dir']]

# Fix paths
config['repos']['core']['swagger_cli'] = os.sep.join(str(config['repos']['core']['swagger_cli']).split("/"))
config['repos']['core']['swagger_spec'] = os.sep.join(str(config['repos']['core']['swagger_spec']).split("/"))
config['repos']['core']['composer_cli'] = os.sep.join(str(config['repos']['core']['composer_cli']).split("/"))

# Replace placeholder
config['repos']['core']['swagger_cli'] = str(config['repos']['core']['swagger_cli']).replace(rep[0], rep[1])
config['repos']['core']['swagger_spec'] = str(config['repos']['core']['swagger_spec']).replace(rep[0], rep[1])
config['repos']['core']['composer_cli'] = str(config['repos']['core']['composer_cli']).replace(rep[0], rep[1])

print('----- Bootstrap debug: -----')
print('Travis build directory is: ' + TRAVIS_BUILD_DIR + '\n')
