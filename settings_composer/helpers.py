import importlib
import sys

from . import environment


def output_if_verbose(headline, *list_items):
    if environment.is_verbose():
        if headline:
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
    try:
        module = importlib.import_module(module_name)
        if reload_module:
            reload(module)
    except ImportError:
        module = None
    output_if_verbose(
        None,
        "{module_name}{status}".format(
            module_name=module_name,
            status=' (not present)' if module is None else ' (forced reload)' if reload_module else ''
        )
    )
    return module


def get_settings_from_module(module):
    settings = {}
    for name in dir(module):
        if name.isupper():  # As per Django convention
            settings[name] = getattr(module, name)
    return settings
