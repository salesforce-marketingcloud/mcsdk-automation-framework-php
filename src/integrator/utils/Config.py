import os
import yaml


class Config:
    """ The configuration class """

    @staticmethod
    def from_yaml(root_dir):
        """ Config class constructor """
        with open(os.path.join(root_dir, 'integrator-config.yml'), 'r') as file:
            return yaml.safe_load(file)
