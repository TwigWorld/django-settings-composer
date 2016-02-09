import os

from django.core.exceptions import ImproperlyConfigured

from . import constants


def get_settings_module_name():
    settings_module = os.environ.get(constants.SETTINGS_MODULE_VARIABLE_NAME)
    if settings_module is None:
        raise ImproperlyConfigured(
            "Django settings composer: settings module not defined in environment variable."
        )
    if not settings_module:
        raise ImproperlyConfigured(
            "Django settings composer: settings module environment variable cannot be blank."
        )
    return settings_module


def get_site_name():
    return os.environ.get(constants.SITE_VARIABLE_NAME, '')


def get_env_name():
    return os.environ.get(constants.ENV_VARIABLE_NAME, '')


def get_switches():
    switches = {}
    env_switches = os.environ.get(constants.SWITCHES_VARIABLE_NAME, '')
    for env_switch in env_switches.split(','):
        env_swtich = env_switch.strip()
        if not env_switch:
            continue  # Simply ignore blanks
        try:
            group_name, switch_name = env_switch.split(':')
        except ValueError:
            raise ImproperlyConfigured(
                "Settings Composer: '{env_switch}' is not a valid switch reference".format(
                    env_switch=env_switch
                )
            )
        group_name = group_name.strip()
        switch_name = switch_name.strip()
        if group_name in switches:
            raise ImproperlyConfigured(
                "Settings Composer: Switch group access multiple times through environmental variable"
            )
        switches[group_name] = switch_name
    return switches

def is_verbose():
    return os.environ.get(constants.VERBOSE_VARIABLE_NAME, '').lower() in constants.TRUE_VALUES
