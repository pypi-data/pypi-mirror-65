import os
import yaml
from typing import List, IO
from gwx_telehealth import config


class ConfigParserService:
    """Parser service dedicated to translate the specified config file from the consumer's app,
    accepts a variety of config formats such as:

    - .yaml
    - .conf
    - .ini

    Note: As of this initial version (0.0.1) we only support .yaml file type.
    """

    # Config file string provided.
    config_file = ''

    # Where the configuration path_values will be defined.
    service_config = []

    def __init__(self, service_config_path: str, service_config_file: str):
        self.config_map = {
            '.yaml': self.__parse_yaml
        }
        self.__set_config_file(service_config_path, service_config_file)

        self.service_config = self.__parser(self.__get_config_file())

    def __set_config_file(self, service_config_path: str, service_config_file: str) -> None:
        """Build the config_parser path and config_parser file.

        :param service_config_path: string value of the directory of where the config_parser file is stored.
        :param service_config_file: string value provided config_parser file.
        :return: None
        """

        service_config_file = os.path.join(service_config_path, service_config_file)

        try:
            open(service_config_file, 'r').close()
        except FileNotFoundError:
            raise FileNotFoundError([config['package_name'], f'File {service_config_file} does not exists'])

        self.config_file = service_config_file

    def __get_config_file(self) -> str:
        """Return the defined config_parser file within the config_parser path.

        :return: string value of the defined config_parser file.
        """
        return self.config_file

    def get_config(self) -> dict:
        """Return the parsed config_parser.

        :return: the parsed config_parser as dictionary.
        """
        return self.__provider_identifier(self.service_config['provider'])

    def get_provider_name(self) -> str:
        """Return the provider service's name, from the parsed config_parser.

        :return:
        """

        return self.service_config['provider']

    def __parser(self, config_path: str) -> List or None:
        """Parse the given config_parser to usable configuration path_values.

        :param config_path: string value of the config_parser files location

        :return: the parsed configuration.
        """
        file = None

        try:
            file = open(config_path, 'r')

        except FileNotFoundError:
            FileNotFoundError(['gwx-telehealth', f'File {config_path} not found.'])
            return None

        _, extension = os.path.splitext(config_path)

        try:
            parsed_file = self.config_map[extension](file)
        except IndexError:
            raise IndexError(['gwx-payment', f'Extension {extension} is not supported yet.'])

        return parsed_file

    def __provider_identifier(self, provider_name: str) -> dict:
        """Locate's the provider by it's name / index.

        :param provider_name: string name of the provider ie: paypal, stripe etc..
        :return: the parsed config_parser object in dictionary format
        """
        return self.service_config[provider_name]

    @staticmethod
    def __parse_yaml(config_io: IO or None) -> dict or None:
        """The yaml file format parser.

        :param config_io: The current file in stream io.
        :return: list of config_parser path_values.
        """
        if config_io is None:
            return None

        return yaml.load(config_io, Loader=yaml.BaseLoader)
