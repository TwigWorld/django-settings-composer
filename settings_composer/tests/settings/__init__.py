import settings_composer


LOADED_CORE_SETTINGS = True

STUFF = {
    'something': 'other thing',
    'nothing': 'not a thing'
}


settings_composer.load(
    'settings_composer.tests.settings.switch_definitions',
    'settings_composer.tests.settings.cleaning',
)
