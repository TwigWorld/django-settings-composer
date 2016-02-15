import settings_composer

settings_composer.apply_switch('debug', 'off')
settings_composer.apply_switch('thing', 'on')


LOADED_PRODUCTION_SETTINGS = True
LOADED_LOCAL_SETTINGS = False
DEBUG = False
