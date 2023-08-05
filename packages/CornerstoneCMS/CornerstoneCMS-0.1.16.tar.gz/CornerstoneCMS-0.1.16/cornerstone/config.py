import json
from pathlib import Path
from configparser import ConfigParser

import yaml
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader


BOOLEAN_VALUES = ['yes', 'true', 'on', 'no', 'false', 'off']
DEFAULT_CONFIG = {
    # SQLAlchemy
    'SQLALCHEMY_DATABASE_URI': 'sqlite:///cornerstonecms.sqlite',
    'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    # User settings
    'USER_ENABLE_EMAIL': False,
    'USER_ENABLE_USERNAME': False,
    'USER_REQUIRE_RETYPE_PASSWORD': True,
    # CornerstoneCMS settings
    'CORNERSTONE_TITLE': 'ZineMan',
    'CORNERSTONE_SWATCH': 'default',
    'CORNERSTONE_SUPERUSER': {
        'email': 'info@example.com',
        'name': 'Superuser',
        'password': 'P@ssw0rd'
    }
}


def _load_from_ini_file(filename):
    """
    Load from a config file
    """
    config = {}
    parser = ConfigParser()
    parser.read(str(filename))
    for section in parser.sections():
        for option in parser.options(section):
            # Get the value, skip it if it is blank
            string_value = parser.get(section, option)
            if not string_value:
                continue
            # Try to figure out what type it is
            if string_value.isnumeric() and '.' in string_value:
                value = parser.getfloat(section, option)
            elif string_value.isnumeric():
                value = parser.getint(section, option)
            elif string_value.lower() in BOOLEAN_VALUES:
                value = parser.getboolean(section, option)
            elif string_value.startswith('{'):
                # Try to load string values beginning with '{' as JSON
                try:
                    value = json.loads(string_value)
                except ValueError:
                    # If this is not JSON, just use the string
                    value = string_value
            else:
                value = string_value
            # Set up the configuration key
            if section == 'flask':
                # Options in the flask section don't need FLASK_*
                key = option.upper()
            else:
                key = '{}_{}'.format(section, option).upper()
            # Save this into our config dictionary
            config[key] = value
    return config


def _load_from_yaml_file(filename):
    """
    Load the configuration from a yaml file
    """
    with filename.open() as yaml_file:
        config = yaml.load(yaml_file.read(), Loader=Loader)
    return config


def _load_from_json_file(filename):
    """
    Load the Flask configuration from a config file
    """
    with filename.open() as json_file:
        config = json.loads(json_file.read())
    return config


def config_from_file(app, filename):
    """
    Load configuration from a file
    """
    # Get the default configuration
    config = dict(**DEFAULT_CONFIG)
    # Set up the filename
    filename = Path(filename)
    if not filename.exists:
        # log a warning
        print('No config file found')
        return
    # Load from the file based on the extension
    if filename.suffix in ['.ini', '.conf', '.cfg']:
        config.update(_load_from_ini_file(filename))
    elif filename.suffix in ['.yaml', '.yml']:
        config.update(_load_from_yaml_file(filename))
    elif filename.suffix in ['.json']:
        config.update(_load_from_json_file(filename))
    # Set the app name everywhere it is needed so that the deployer doesn't need to
    config['USER_APP_NAME'] = config['CORNERSTONE_TITLE']
    config['USER_SWATCH_THEME'] = config['CORNERSTONE_SWATCH']
    config['FLASK_ADMIN_SWATCH'] = config['CORNERSTONE_SWATCH']
    app.config.update(config)
