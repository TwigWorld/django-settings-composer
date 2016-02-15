import settings_composer


LOADED_SWITCH_DEFINITIONS = True


# Change debug mode

settings_composer.create_switch(
    'debug', 'off', {
        'DEBUG': False,
        'TEMPLATE_DEBUG': False,
        'DEBUG_PROPAGATE_EXCEPTIONS': False
    }
)

settings_composer.create_switch(
    'debug', 'on', {
        'DEBUG': True,
        'TEMPLATE_DEBUG': True,
        'DEBUG_PROPAGATE_EXCEPTIONS': False
    }
)

settings_composer.create_switch(
    'debug', 'propagate', {
        'DEBUG': True,
        'TEMPLATE_DEBUG': True,
        'DEBUG_PROPAGATE_EXCEPTIONS': True
    }
)


# Turn Thing on and off

settings_composer.create_switch(
    'thing', 'off', 'settings_composer.tests.settings.switches.thing_off'
)

settings_composer.create_switch(
    'thing', 'on', 'settings_composer.tests.settings.switches.thing_off'
)
