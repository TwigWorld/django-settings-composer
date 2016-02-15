import settings_composer


LOADED_SITE_LOCAL_SETTINGS = True


def check_recursion(settings):
    settings_composer.load('settings_composer.tests.settings.recursion.main')


settings_composer.clean(check_recursion)
