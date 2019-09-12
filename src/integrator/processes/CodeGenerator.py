import os
from bootstrap import BUILDER_REPO_DIR
from utils.Command import Command


class CodeGenerator:
    """ Swagger processes class """

    def __init__(self, config, config_dir, templates_dir, repo_dir):
        """ Swagger class constructor """
        self.__config = config
        self.__config_dir = config_dir
        self.__templates_dir = templates_dir
        self.__repo_dir = repo_dir

    def generate_sdk(self):
        """ Generates the SDK code using the swagger codegen library """
        cmd = [
            'java',
            '-jar',
            '{swagger_exec}'.format(swagger_exec=self.__config['repos']['core']['swagger_cli']),
            'generate',
            '-l',
            'php',
            '-i',
            '{spec_file}'.format(spec_file=self.__config['repos']['core']['swagger_spec']),
            '-t',
            '{templates_dir}'.format(templates_dir=os.path.join(self.__templates_dir, 'mustache')),
            '-c',
            '{config_file}'.format(config_file=os.path.join(self.__config_dir, 'swagger-codegen-config.json')),
            '-o',
            '{sdk_folder}'.format(sdk_folder=self.__repo_dir)
        ]

        command = Command(cmd)
        command.run()

        return command.returned_errors()

    def generate_client(self):
        """ Generates the SDK code custom PHP code generator """
        cmd = [
            'php',
            '-f',
            os.path.join(BUILDER_REPO_DIR, 'src', 'generator', self.__config['generators']['php']),
            os.path.join(self.__templates_dir, 'phtml'),
            os.path.join(self.__config_dir, 'swagger-codegen-config.json')
        ]

        command = Command(cmd)
        command.run()

        print(command.get_output())

        return command.returned_errors()
