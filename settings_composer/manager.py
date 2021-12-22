from collections import deque

from .helpers import (
    load_settings_module,
    get_settings_from_module,
    output_if_verbose
)
from . import environment


ACTION_NAMES = [
    'load',
    'create_switch',
    'apply_switch',
    'set',
    'extend_setting',
    'update_setting',
    'exclude_from_setting',
    'clean'
]


class ActionContextManager(object):
    """
    Maintains a collection of named action queues, which are stored in a series
    of context layers.

    Contexts can be added, creating a new set of action queues.

    Actions are consumed by removing the most recent context layer (FILO), and
    returning the actions in the order they were added (FIFO).

    Actions are always added to the current context layer.
    """

    def __init__(self, action_names):
        self.action_names = action_names
        self.action_context_layers = {
            action_name: []
            for action_name in self.action_names
        }

    def create_context_layer(self, context_name):
        for action_name in self.action_names:
            self.action_context_layers[action_name].append((context_name, deque()))

    def add_action(self, name, **kwargs):
        self.action_context_layers[name][-1][1].appendleft(kwargs)

    def consume_actions(self, name):
        if len(self.action_context_layers[name]):
            context_name, action_queue = self.action_context_layers[name].pop()
            while len(action_queue):
                yield context_name, action_queue.pop()

    def consume_all_actions(self, name):
        while len(self.action_context_layers[name]):
            for context_name, action in self.consume_actions(name):
                yield context_name, action


class SettingsManager(object):
    """
    When bound to a settings dictionary, allows settings to be composed either
    through direct definition in modules, or by processing actions executed
    within those modules.
    """
    def __init__(self):
        self.is_bound = False

    def __getattribute__(self, name):
        if name not in ('bind', 'is_bound') and not self.is_bound:
            raise AttributeError(
                "Settings manager must be bound before accessing its attributes."
            )
        return super(SettingsManager, self).__getattribute__(name)

    # Setup / Teardown

    def bind(self, target_settings):
        """
        Bind the settings manager to a settings dictionary.
        """
        self.is_bound = True
        self.target_settings = target_settings
        self.definitions = {}
        self.settings_source = {}
        self.actions = ActionContextManager(ACTION_NAMES)

    def unbind(self):
        """
        Prevent further modification to the settings dictionary.
        """
        self.target_settings['SETTINGS_COMPOSER_SOURCE'] = self.settings_source
        self.is_bound = False
        del self.target_settings
        del self.definitions
        del self.settings_source
        del self.actions

    # Actions

    def create_action_context(self, context_name):
        self.actions.create_context_layer(context_name)

    def add_action(self, name, **kwargs):
        self.actions.add_action(name, **kwargs)

    def get_current_actions(self, name):
        return self.actions.consume_actions(name)

    def get_all_actions(self, name):
        return self.actions.consume_all_actions(name)

    # Main logic

    def apply_settings_modules(self, module_names):
        output_if_verbose("Loading settings modules")
        for module_name in module_names:
            self.apply_settings_module(module_name)
        self.apply_env_switches()
        self.process_clean_actions()

    def apply_settings_module(self, module_name, source_name=None):
        source_name = source_name or module_name
        self.create_action_context(source_name)
        module = load_settings_module(module_name)
        self.process_load_actions()
        # Apply settings directly from module
        self.update_settings(
            get_settings_from_module(module),
            source_name
        )
        self.process_standard_actions()

    def apply_env_switches(self):
        self.create_action_context('[Environment]')
        for group_name, switch_name in environment.get_switches().items():
            self.add_action('apply_switch', group_name=group_name, switch_name=switch_name)
        self.process_load_actions()
        self.process_standard_actions()

    def apply_function(self, function, source_name):
        source_name = u"FUNCTION '{function_name}' CALLED FROM {source_name}".format(
            function_name=function.__name__,
            source_name=source_name
        )
        self.create_action_context(source_name)
        function(self.target_settings)
        self.process_load_actions()
        self.process_standard_actions()

    # Settings

    def update_settings(self, settings, source_name):
        for name, value in settings.items():
            self.target_settings[name] = value
            self.set_source_name(name, source_name)

    def set_source_name(self, name, source_name):
        self.settings_source.setdefault(name, [])
        self.settings_source[name].append(source_name)

    # Process actions

    def process_standard_actions(self):
        self.process_set_actions()
        self.process_create_switch_actions()
        self.process_apply_switch_actions()
        self.process_extend_setting_actions()
        self.process_update_setting_actions()
        self.process_exclude_from_setting_actions()

    def process_load_actions(self):
        for source_name, kwargs in self.get_current_actions('load'):
            for module_name in kwargs['module_names']:
                self.apply_settings_module(
                    module_name,
                    source_name='{module_name} LOADED BY {source_name}'.format(
                        module_name=module_name,
                        source_name=source_name
                    )
                )

    def process_set_actions(self):
        for source_name, kwargs in self.get_current_actions('set'):
            self.update_settings(kwargs, source_name)

    def process_create_switch_actions(self):
        for source_name, kwargs in self.get_current_actions('create_switch'):
            group_name = kwargs['group_name']
            switch_name = kwargs['switch_name']
            definition = kwargs['module_or_settings']
            self.definitions.setdefault(group_name, {})
            if switch_name in self.definitions[group_name]:
                raise ValueError(
                    "Settings Composer: Encountered re-definition of {group_name}: {switch_value}".format(
                        group_name=group_name,
                        switch_name=switch_name
                    )
                )
            self.definitions[group_name][switch_name] = {
                'definition': definition,
                'source_name': source_name
            }

    def process_apply_switch_actions(self):
        for source_name, kwargs in self.get_current_actions('apply_switch'):
            group_name = kwargs['group_name']
            switch_name = kwargs['switch_name']
            try:
                switch = self.definitions[group_name][switch_name]
            except KeyError:
                raise ValueError(
                    "Settings Composer: No such definition {group_name}: {switch_name}".format(
                        group_name=group_name,
                        switch_name=switch_name
                    )
                )
            switch_source_name = u'[SWITCH <{group_name}: {swtich_name}> DEFINED IN {switch_source_name}] SET BY {source_name}'.format(
                group_name=group_name,
                swtich_name=switch_name,
                switch_source_name=switch['source_name'],
                source_name=source_name
            )
            definition = switch['definition']
            if hasattr(definition, 'keys'):  # dictionary
                self.update_settings(definition, switch_source_name)
            else:
                self.apply_settings_module(definition, switch_source_name)

    def process_extend_setting_actions(self):
        for source_name, kwargs in self.get_current_actions('extend_setting'):
            setting_name = kwargs['setting_name']
            values = kwargs['values']
            if setting_name not in self.settings_source:
                raise ValueError(
                    "Settings Composer: Can't extend {setting_name} (not defined)".format(
                        setting_name=setting_name
                    )
                )
            self.target_settings[setting_name].extend(values)
            self.settings_source[setting_name][-1] = u'{set_by} EXTENDED BY {source_name}'.format(
                set_by=self.settings_source[setting_name][-1],
                source_name=source_name
            )

    def process_update_setting_actions(self):
        for source_name, kwargs in self.get_current_actions('update_setting'):
            setting_name = kwargs['setting_name']
            values = kwargs['values']
            if setting_name not in self.settings_source:
                raise ValueError(
                    "Settings Composer: Can't update {setting_name} (not defined)".format(
                        setting_name=setting_name
                    )
                )
            self.target_settings[setting_name].update(values)
            self.settings_source[setting_name][-1] = u'{set_by} UPDATED BY {source_name}'.format(
                set_by=self.settings_source[setting_name][-1],
                source_name=source_name
            )

    def process_exclude_from_setting_actions(self):
        for source_name, kwargs in self.get_current_actions('exclude_from_setting'):
            setting_name = kwargs['setting_name']
            items = kwargs['items']
            if setting_name not in self.settings_source:
                raise ValueError(
                    "Settings Composer: Can't exclude from {setting_name} (not defined)".format(
                        setting_name=setting_name
                    )
                )
            changed = False
            if isinstance(self.target_settings[setting_name], dict):
                for item in items:
                    try:
                        del self.target_settings[setting_name][item]
                        changed = True
                    except KeyError:
                        pass  # May already have been excluded
            else:
                new_setting = list(
                    filter(
                        lambda item: item not in items,
                        self.target_settings[setting_name]
                    )
                )
                changed = len(new_setting) < len(self.target_settings[setting_name])
                self.target_settings[setting_name] = new_setting
            if changed:
                self.settings_source[setting_name][-1] = u'{set_by} EXCLUDED WITH {source_name}'.format(
                    set_by=self.settings_source[setting_name][-1],
                    source_name=source_name
                )

    def process_clean_actions(self):
        for source_name, kwargs in self.get_all_actions('clean'):
            function = kwargs['function']
            self.apply_function(function, source_name)
