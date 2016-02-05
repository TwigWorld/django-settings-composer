import os

from django.core.exceptions import ImproperlyConfigured

from . import constants


def get_project_name():
    project_name = os.environ.get(constants.PROJECT_VARIABLE_NAME)
    if project_name is None:
        raise ImproperlyConfigured(
            "Django settings composer: project not defined in environment variable."
        )
    if not project_name:
        raise ImproperlyConfigured(
            "Django settings composer: project environment variable cannot be blank."
        )
    return project_name


def get_site_name():
    return os.environ.get(constants.SITE_VARIABLE_NAME, '')


def get_env_name():
    return os.environ.get(constants.ENV_VARIABLE_NAME, '')


def get_switch_names():
    return [
        switch.strip() for switch in os.environ.get(
            constants.SWITCHES_VARIABLE_NAME, ''
        ).split(',')
        if switch.strip()
    ]


def is_verbose():
    return os.environ.get(constants.VERBOSE_VARIABLE_NAME).lower() in constants.TRUE_VALUES
