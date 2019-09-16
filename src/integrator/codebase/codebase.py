import os
from mcsdk.codebase import codebase
from mcsdk.integration.os.process import Command
from mcsdk.integration.os.utils import chdir


class Setup(codebase.AbstractCodeSetup):
    """ Handles the code setup processes """

    def install_dependencies(self):
        chdir(self._package_folder)

        command = Command(['php', '-f', self._config['repos']['core']['composer_cli'], 'install'])
        command.run()

        output = command.get_output()

        chdir(self._root_dir)  # Get back to previous directory

        print('----- Dependencies install log -----')
        print(output)

        if command.returned_errors():
            return 255

        if output.find('You may be getting outdated dependencies. Run update to update them.') != -1:
            return self.update_dependencies()

        return 0

    def update_dependencies(self):
        chdir(self._package_folder)

        command = Command(['php', '-f', self._config['repos']['core']['composer_cli'], 'update'])
        command.run()

        chdir(self._root_dir)  # Get back to previous directory

        print('----- Dependencies update log -----')
        print(command.get_output())

        if command.returned_errors():
            return 255

        return 0


class Integration(codebase.AbstractCodeIntegration):
    """ Handles the code integration processes """

    def run_tests(self):
        chdir(self._package_folder)

        # Vars
        config_file = os.path.join(self._package_folder, 'phpunit.xml.dist')
        test_suite = ','.join(self._config['repos']['sdk']['tests'])

        # logging the working directory for debug
        print('----- Tests: -----')
        print('Configuration file: ' + config_file)

        # Command to run the unit tests
        cmd = '{phpunit} -c {config_file} --testsuite={testsuite}'.format(
            phpunit=os.path.join(self._package_folder, os.sep.join('vendor/bin/phpunit'.split('/'))),
            config_file=config_file,
            testsuite=test_suite
        )

        command = Command(cmd)
        command.run()

        chdir(self._root_dir)  # Get back to previous directory

        if command.returned_errors():
            print('Unit tests FAILED')
            print(command.get_output())
            return 255

        return 0
