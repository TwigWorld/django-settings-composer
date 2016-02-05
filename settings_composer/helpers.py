import importlib
import sys

from django.core.exceptions import ImproperlyConfigured

from . import environment, constants


def output_if_verbose(headline, *list_items):
    if environment.is_verbose():
        sys.stdout.write('Django Settings Composer: ')
        sys.stdout.write(headline + '\n')
        for list_item in list_items:
            sys.stdout.write('    ')
            sys.stdout.write(list_item + '\n')


def collate_settings_modules():
    """
    Create a list of of settings modules to load, in order, based on project,
    site, environment and switch variables.
    """
    project = environment.get_project_name()
    env = environment.get_env_name()
    site = environment.get_site_name()
    switches = environment.get_switch_names()

    output_if_verbose(
        "Reading environmental variables from OS",
        u"Project: " + project,
        u"Env: " + env,
        u"Site: " + site,
        u"Switches: " + u', '.join(switches)
    )

    settings_files = [u'{project}.settings']
    if env:
        settings_files.append(u'{project}.settings.env.{env}')
    if site:
        settings_files.append(u'{project}.settings.sites.{site}')
    if env and site:
        settings_files.append(u'{project}.settings.sites.{site}.env.{env}')
    for switch in switches:
        settings_files.append(
            u'{{project}}.settings.switches.{switch}'.format(
                switch=switch.strip()
            )
        )
    settings_files.append(
        '{project}.settings.finally'
    )
    settings_files = map(
        lambda module_name: module_name.format(
            project=project,
            site=site,
            env=env
        ),
        settings_files
    )

    output_if_verbose(
        "Compiling settings modules based on environmental variables",
        *settings_files
    )

    return settings_files


def apply_settings_module(module_name, existing_settings, previously_applied_settings=None):
    """
    Attempt to apply a settings module to the passed in dictionary. Return
    None if the module can't be imported, or a dictionary mapping each setting
    to the loaded module.
    """
    try:
        module = importlib.import_module(module_name)
    except ImportError as e:
        output_if_verbose(
            "Failed to load settings module {name}".format(name=module_name),
            e.message
        )
        return None

    applied_settings = {}
    for name in dir(module):
        if name.isupper():  # As per Django settings convention
            value = getattr(module, name)
            if (
                name.startswith(constants.EXCLUDE_PREFIX) or
                name.startswith(constants.UPDATE_PREFIX)
            ):
                # These are special cases: we always combine them
                if value:
                    existing_settings.setdefault(name, [])
                    applied_settings[name] = previously_applied_settings.get(name, [])
                    existing_settings[name].append(value)
                    applied_settings[name].append(module_name)
            else:
                existing_settings[name] = value
                applied_settings[name] = module_name

    output_if_verbose(
        "Loaded settings module {name}".format(
            name=module_name,
        ),
        "({count} definitions parsed)".format(
            count=len(applied_settings.keys())
        )
    )

    return applied_settings


def apply_updates(settings):
    """
    Apply Settings Composer update entries to settings if target settings are
    present, or create them if not. Each update is a list of either lists or
    dictionaries, dependant on the target setting's type.
    """
    update_setting_names = filter(
        lambda key: key.startswith(constants.UPDATE_PREFIX),
        settings.keys()
    )
    for update_setting_name in update_setting_names:
        target_setting_name = update_setting_name[len(constants.UPDATE_PREFIX):]
        updates = settings[update_setting_name]
        verbose_message_items = []
        for update_items in updates:
            if target_setting_name not in settings:
                raise ImproperlyConfigured(
                    "Django settings composer: Attempted to update an "
                    "undefined setting ({setting})".format(
                        setting=target_setting_name
                    )
                )

            elif hasattr(update_items, 'keys'):
                # Expect target to be a dict
                if not hasattr(settings[target_setting_name], 'update'):
                    raise ImproperlyConfigured(
                        "Django settings composer: Attempted to update "
                        "non-dictionary setting {setting} with a dictionary".format(
                            setting=target_setting_name
                        )
                    )
                settings[target_setting_name].update(update_items)
                verbose_message_items.append(update_items.keys())

            else:
                # Expect list-like iterable, but may be immutable so convert to list
                if hasattr(settings[target_setting_name], 'keys'):
                    raise ImproperlyConfigured(
                        "Django settings composer: Attempted to update "
                        "dictionary setting {setting} with a non-dictionary".format(
                            setting=target_setting_name
                        )
                    )
                settings[target_setting_name] = (
                    list(settings[target_setting_name]) + update_items
                )
                verbose_message_items.append(update_items)

        output_if_verbose(
            "Applying updates to {setting}".format(setting=target_setting_name),
            *[
                u', '.join(update_items)
                for update_items in verbose_message_items
            ]
        )


def apply_exclusions(settings):
    """
    Apply Settings Composer exclude entries to settings if target settings are
    present. Exclusions should be a list of items or keys, and target setting
    should either be an iterable or a dict.
    """
    exclusion_setting_names = filter(
        lambda key: key.startswith(constants.EXCLUDE_PREFIX),
        settings.keys()
    )
    for exclusion_setting_name in exclusion_setting_names:
        target_setting_name = exclusion_setting_name[len(constants.EXCLUDE_PREFIX):]
        if target_setting_name not in settings:
            output_if_verbose(
                "Cannot apply exclusions to {setting} (not defined)".format(
                    setting=target_setting_name
                )
            )
            continue
        exclusions = settings[exclusion_setting_name]
        verbose_message_items = []
        for exclusion_items in exclusions:
            verbose_message_items.append(exclusion_items)
            setting_obj = settings[target_setting_name]
            if hasattr(setting_obj, 'keys'):
                # setting is a dict, so exclude on key match
                for item in exclusion_items:
                    try:
                        del setting_obj[item]
                    except KeyError:
                        pass
            else:
                # Assume iterable, but may be immutable so use a filter
                settings[target_setting_name] = list(
                    filter(
                        lambda s: s not in exclusion_items,
                        setting_obj
                    )
                )

        output_if_verbose(
            "Applying exclusions to {setting}".format(setting=target_setting_name),
            *[
                u', '.join(exclusion_items)
                for exclusion_items in verbose_message_items
            ]
        )
