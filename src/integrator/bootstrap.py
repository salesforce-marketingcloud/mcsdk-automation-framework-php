from mcsdk.bootstrap import *

# directories
current_dir = os.path.join(TRAVIS_REPO_OWNER_DIR, cfg['repos']['current']['name'])

# Fix paths
cfg['repos']['core']['composer_cli'] = os.sep.join(str(cfg['repos']['core']['composer_cli']).split("/"))

# Replace placeholder
cfg['repos']['core']['composer_cli'] = str(cfg['repos']['core']['composer_cli']).replace(rep[0], rep[1])

print('----- Bootstrap log: -----')
print('Current directory: ' + current_dir + '\n')
