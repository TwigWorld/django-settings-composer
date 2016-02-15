import settings_composer

settings_composer.apply_switch('debug', 'on')
settings_composer.apply_switch('thing', 'off')


LOADED_LOCAL_SETTINGS = True
LOADED_PRODUCTION_SETTINGS = False