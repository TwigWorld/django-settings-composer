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


def load_settings_module(module_name):
    reload_module = False
    if module_name in sys.modules:
        # Ensure the module is loaded fresh
        reload_module = True
    output_if_verbose(
        "Loading settings module",
        "{module_name}{reloaded}".format(
            module_name=module_name,
            reloaded='' if not reload_module else ' (forced reload)'
        )
    )
    module = importlib.import_module(module_name)
    if reload_module:
        reload(module)
    return module


def get_settings_from_module(module):
    settings = {}
    for name in dir(module):
        if name.isupper():  # As per Django convention
            settings[name] = getattr(module, name)
    return settings
