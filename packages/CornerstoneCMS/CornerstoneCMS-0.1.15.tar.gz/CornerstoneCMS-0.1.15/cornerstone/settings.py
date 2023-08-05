import json
from collections import OrderedDict

from cornerstone.db import db
from cornerstone.db.models import Setting
from cornerstone.util import get_bool

SETTINGS = [
    {
        'title': 'Show sermons on the home page',
        'key': 'sermons-on-home-page',
        'type': 'bool',
        'group': 'home page',
        'allowed_values': None,
        'initial_value': False
    },
    {
        'title': 'Number of sermons to show on the home page',
        'key': 'sermons-home-page-count',
        'type': 'int',
        'group': 'home page',
        'allowed_values': None,
        'initial_value': 10
    },
    {
        'title': 'Include pages in menu automatically',
        'key': 'pages-in-menu',
        'type': 'bool',
        'group': 'menu',
        'allowed_values': None,
        'initial_value': True
    },
    {
        'title': 'Theme',
        'key': 'theme',
        'type': 'str',
        'group': 'theme',
        'allowed_values': None,
        'initial_value': 'bootstrap4'
    },
    {
        'title': 'Enable contact form',
        'key': 'contact-form-enable',
        'type': 'bool',
        'group': 'contact form',
        'allowed_values': None,
        'initial_value': False
    },
    {
        'title': 'E-mail address',
        'key': 'contact-form-email',
        'type': 'str',
        'group': 'contact form',
        'allowed_values': None,
        'initial_value': ''
    },
    {
        'title': 'Hostname',
        'key': 'email-hostname',
        'type': 'str',
        'group': 'e-mail',
        'allowed_values': None,
        'initial_value': ''
    },
    {
        'title': 'From address',
        'key': 'email-from',
        'type': 'str',
        'group': 'e-mail',
        'allowed_values': None,
        'initial_value': ''
    },
    {
        'title': 'Encryption',
        'key': 'email-encryption',
        'type': 'list',
        'group': 'e-mail',
        'allowed_values': ['None', 'STARTSSL', 'SSL/TLS'],
        'initial_value': 'None'
    },
    {
        'title': 'Port',
        'key': 'email-port',
        'type': 'int',
        'group': 'e-mail',
        'allowed_values': None,
        'initial_value': 25
    },
    {
        'title': 'Needs authentication',
        'key': 'email-needs-auth',
        'type': 'bool',
        'group': 'e-mail',
        'allowed_values': None,
        'initial_value': False
    },
    {
        'title': 'Username',
        'key': 'email-username',
        'type': 'str',
        'group': 'e-mail',
        'allowed_values': None,
        'initial_value': ''
    },
    {
        'title': 'Password',
        'key': 'email-password',
        'type': 'str',
        'group': 'e-mail',
        'allowed_values': None,
        'initial_value': ''
    },
    {
        'title': 'Enable Live Stream page',
        'key': 'live-stream-enable',
        'type': 'bool',
        'group': 'live stream',
        'allowed_values': None,
        'initial_value': False
    },
    {
        'title': 'Type',
        'key': 'live-stream-type',
        'type': 'list',
        'group': 'live stream',
        'allowed_values': ['YouTube'],
        'initial_value': 'YouTube'
    },
    {
        'title': 'Stream ID',
        'key': 'live-stream-id',
        'type': 'str',
        'group': 'live stream',
        'allowed_values': None,
        'initial_value': ''
    },
    {
        'title': 'General text',
        'key': 'live-stream-general',
        'type': 'str',
        'group': 'live stream',
        'allowed_values': None,
        'initial_value': ''
    },
    {
        'title': 'Before stream text',
        'key': 'live-stream-before',
        'type': 'str',
        'group': 'live stream',
        'allowed_values': None,
        'initial_value': ''
    },
    {
        'title': 'After stream text',
        'key': 'live-stream-after',
        'type': 'str',
        'group': 'live stream',
        'allowed_values': None,
        'initial_value': ''
    },
    {
        'title': 'Start date/time',
        'key': 'live-stream-start',
        'type': 'str',
        'group': 'live stream',
        'allowed_values': None,
        'initial_value': ''
    }
]


def has_setting(key):
    """
    Check if a setting exists

    :param key: The key of the setting
    """
    return Setting.query.get(key) is not None


def add_setting(title, key, type_, group='core', allowed_values=None):
    """
    Add a setting

    :param title: The visible title of the setting
    :param key: The unique key used to look up the setting in the database
    :param type_: The type of this setting. Can be one of "bool", "int", "str".
    :param allowed_values: Restrict values to only those in this list (renders as a dropdown)
    """
    setting = Setting(title=title, key=key, type=type_, group=group, allowed_values=json.dumps(allowed_values))
    db.session.add(setting)
    db.session.commit()
    return setting


def get_all_settings():
    """
    Get all the settings
    """
    grouped_settings = {}
    settings = Setting.query.all()
    for setting in settings:
        setting.value = json.loads(setting.value)
        setting.allowed_values = json.loads(setting.allowed_values)
        try:
            grouped_settings[setting.group].append(setting)
        except KeyError:
            grouped_settings[setting.group] = [setting]
    return OrderedDict({group: grouped_settings[group] for group in sorted(grouped_settings.keys())})


def get_setting(key, default=None):
    """
    Get a setting
    """
    setting = Setting.query.get(key)
    if not setting:
        return default
    return json.loads(setting.value)


def save_setting(key, value):
    setting = Setting.query.get(key)
    if not setting:
        raise Exception('Cannot save setting without running add_setting: {}'.format(key))
    if setting.type == 'bool':
        value = get_bool(value)
    setting.value = json.dumps(value)
    db.session.add(setting)
    db.session.commit()


def create_settings():
    """
    Create all the settings
    """
    # Add some settings, if they don't already exist
    for setting in SETTINGS:
        if not has_setting(setting['key']):
            add_setting(setting['title'], setting['key'], setting['type'], setting['group'], setting['allowed_values'])
            save_setting(setting['key'], setting['initial_value'])
