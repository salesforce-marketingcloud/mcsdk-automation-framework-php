import os
from bootstrap import TRAVIS_BUILD_DIR
from utils.Command import Command
from utils.Filesystem import chdir


class Codebase:
    """ Codebase processes class """

    def __init__(self, config, folder):
        """ Codebase class constructor """
        self.__config = config
        self.__repo_folder = folder
        self.__package_folder = os.path.join(self.__repo_folder, self.__config['repos']['sdk']['packageName'])

    def install_dependencies(self):
        chdir(self.__package_folder)

        command = Command(['php', '-f', self.__config['repos']['core']['composer_cli'], 'install'])
        command.run()

        output = command.get_output()

        chdir(TRAVIS_BUILD_DIR)  # Get back to previous directory

        print('----- Dependencies install log -----')
        print(output)

        if command.returned_errors():
            return 255

        if output.find('You may be getting outdated dependencies. Run update to update them.'):
            return self.update_dependencies()

        return 0

    def update_dependencies(self):
        chdir(self.__package_folder)

        command = Command(['php', '-f', self.__config['repos']['core']['composer_cli'], 'update'])
        command.run()

        chdir(TRAVIS_BUILD_DIR)  # Get back to previous directory

        print('----- Dependencies install log -----')
        print(command.get_output())

        if command.returned_errors():
            return 255

        return 0

    def run_tests(self):
        chdir(self.__package_folder)

        # Vars
        config_file = os.path.join(self.__package_folder, 'phpunit.xml.dist')
        test_suite = ','.join(self.__config['repos']['sdk']['tests'])

        # logging the working directory for debug
        print('----- Tests: -----')
        print('Configuration file: ' + config_file)

        # Command to run the unit tests
        cmd = '{phpunit} -c {config_file} --testsuite={testsuite}'.format(
            phpunit=os.path.join(self.__package_folder, os.sep.join('vendor/bin/phpunit'.split('/'))),
            config_file=config_file,
            testsuite=test_suite
        )

        command = Command(cmd)
        command.run()

        chdir(TRAVIS_BUILD_DIR)  # Get back to previous directory

        if command.returned_errors():
            print('Unit tests FAILED')
            print(command.get_output())

        return 0
