import importlib
import sys
import types

from . import environment


def output_if_verbose(headline, *list_items):
    if environment.is_verbose():
        sys.stdout.write('Django Settings Composer: ')
        sys.stdout.write(headline + '\n')
        for list_item in list_items:
            sys.stdout.write('  - ')
            sys.stdout.write(list_item + '\n')


def load_settings_module(module):
    if isinstance(module, types.ModuleType):
        return module
    else:
        output_if_verbose("Loading settings module", module)
        return importlib.import_module(module)


def get_settings_from_module(module):
    settings = {}
    for name in dir(module):
        if name.isupper():  # As per Django convention
            settings[name] = getattr(module, name)
    return settings
