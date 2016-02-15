import settings_composer


RECURSION = {
    'LOADED': True
}
RECURSION_TEST_LIST = [1, 2, 3]


def recursion_cleaner(settings):

    def inner(settings):
        settings_composer.set(RECURSION_SUCCESS=True)
        settings_composer.load('settings_composer.tests.settings.recursion.switch_definitions')
        settings_composer.apply_switch('recursive', 'loading')

    settings_composer.clean(inner)
    settings_composer.exclude_from_setting('RECURSION_TEST_LIST', [3, 4])
    settings_composer.update_setting('RECURSION', SUCCESS=True)


settings_composer.clean(recursion_cleaner)
settings_composer.extend_setting('RECURSION_TEST_LIST', [4, 5, 6])
