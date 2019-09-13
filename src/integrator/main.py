from mcsdk.integration import runner
from bootstrap import *
from code.generator import CodeGenerator
from code.codebase import Setup as CodeSetup
from code.codebase import Integration as CodeIntegration

# Vars for the integration run
repo_core_dir = cfg['repos']['core']['dir']
repo_sdk_dir = cfg['repos']['sdk']['dir']

# code generation components
generator = CodeGenerator(current_dir, cfg, config_dir, templates_dir, repo_sdk_dir)
setup = CodeSetup(TRAVIS_REPO_OWNER_DIR, cfg, repo_sdk_dir)
integration = CodeIntegration(TRAVIS_REPO_OWNER_DIR, cfg, repo_sdk_dir)

# Run the integration
runner.run(config=cfg, code_generator=generator, code_setup=setup, code_integration=integration)
