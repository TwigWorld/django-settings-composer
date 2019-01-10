from .manager import ACTION_NAMES, SettingsManager

__all__ = ACTION_NAMES


settings_manager = SettingsManager()


# These actions can be used anywhere within a module. They will be exectuted
# in the order they are defined here. 'load' actions will be processed before
# any module definitions or other actions are applied to the settings. All
# other actions are applied after module definitions, with the exception of
# 'clean' actions which are only executed once all of the primary modules have
# been loaded.

def load(*module_names):
    """
    Load one or more modules and apply settings from them.
    """
    settings_manager.add_action(
        'load',
        module_names=module_names
    )


def set(**settings):
    """
    Apply keyword settings directly (useful within function scope). Can also be
    used if you need to be sure something is set before modifying it.
    """
    settings_manager.add_action(
        'set',
        **settings
    )


def create_switch(group_name, switch_name, module_or_settings):
    """
    Define a switch as either a settings dict or a settings module to load.
    """
    settings_manager.add_action(
        'create_switch',
        group_name=group_name,
        switch_name=switch_name,
        module_or_settings=module_or_settings
    )


def apply_switch(group_name, switch_name):
    """
    Apply a previously defined switch to the current settings.
    """
    settings_manager.add_action(
        'apply_switch',
        group_name=group_name,
        switch_name=switch_name
    )


def extend_setting(setting_name, values):
    """
    Extend the supplied values to a list-style setting.
    """
    settings_manager.add_action(
        'extend_setting',
        setting_name=setting_name,
        values=values
    )


def update_setting(setting_name, **values):
    """
    Update an existing dictionary setting with the supplied values.
    """
    settings_manager.add_action(
        'update_setting',
        setting_name=setting_name,
        values=values
    )


def exclude_from_setting(setting_name, items):
    """
    Exclude the supplied items from a list or dict setting. If the setting is a
    dict, the items are the keys to exclude.
    """
    settings_manager.add_action(
        'exclude_from_setting',
        setting_name=setting_name,
        items=items
    )


def clean(function):
    """
    Execute a function after all primary modules have been loaded. The function
    must take the current settings dictionary as an argument.

    Use this to perform clean-up actions or logic-based decisions, such as
    checking whether DEBUG is turned on once all settings have been loaded.
    """
    settings_manager.add_action(
        'clean',
        function=function
    )
