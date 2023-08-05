import os
import configparser
import itertools

config = {}


def create_config() -> dict:
    """Parse the config file to a dict value.

    :return: dict value of the resolved package config file.
    """
    config_parser = configparser.ConfigParser()
    package_path = os.path.dirname(os.path.realpath(__file__))

    config_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'config', 'gwx_telehealth_config.ini')

    with open(config_file) as fp:
        config_parser.read_file(itertools.chain(['[global]'], fp), source=config_file)

    for index, config_path in config_parser.items('gwx_telehealth_paths'):
        config.update([(index, f'{package_path}{eval(config_path)}')])

    for index, config_value in config_parser.items('gwx'):
        config.update([(index, eval(config_value))])

    return config


# Assemble the config values.
create_config()
