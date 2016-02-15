from unittest import TestCase

import mock

from settings_composer.loading import collect_settings


class SettingsAcceptanceTests(TestCase):

    def setUp(self):
        self.settings = {}

    @mock.patch('settings_composer.loading.collate_settings_modules')
    def test_local(self, collate_settings_modules):
        collate_settings_modules.return_value = [
            'settings_composer.tests.settings',
            'settings_composer.tests.settings.env.local',
            'settings_composer.tests.settings.sites.test_site',
            'settings_composer.tests.settings.sites.test_site.env.local'
        ]
        collect_settings(self.settings)
        self.assertEquals(
            self.settings,
            {
                'DEBUG': True,
                'DEBUG_PROPAGATE_EXCEPTIONS': False,
                'LOADED_CLEANING_FUNCTIONS': True,
                'LOADED_CORE_SETTINGS': True,
                'LOADED_LOCAL_SETTINGS': True,
                'LOADED_PRODUCTION_SETTINGS': False,
                'LOADED_SITE_LOCAL_SETTINGS': True,
                'LOADED_SWITCH_DEFINITIONS': True,
                'RECURSION': {'LOADED': True, 'SUCCESS': True},
                'RECURSION_SUCCESS': True,
                'RECURSION_TEST_LIST': [1, 2, 5, 6],
                'RECURSIVE_LOADING': True,
                'STUFF': {'something': 'anything'},
                'TEMPLATE_DEBUG': True,
                'SETTINGS_COMPOSER_SOURCE': {
                    'DEBUG': ['[SWITCH <debug: on> DEFINED IN settings_composer.tests.settings.switch_definitions LOADED BY settings_composer.tests.settings] SET BY settings_composer.tests.settings.env.local'],
                    'DEBUG_PROPAGATE_EXCEPTIONS': ['[SWITCH <debug: on> DEFINED IN settings_composer.tests.settings.switch_definitions LOADED BY settings_composer.tests.settings] SET BY settings_composer.tests.settings.env.local'],
                    'LOADED_CLEANING_FUNCTIONS': ['settings_composer.tests.settings.cleaning LOADED BY settings_composer.tests.settings'],
                    'LOADED_CORE_SETTINGS': ['settings_composer.tests.settings'],
                    'LOADED_LOCAL_SETTINGS': ['settings_composer.tests.settings.env.local'],
                    'LOADED_PRODUCTION_SETTINGS': ['settings_composer.tests.settings.env.local'],
                    'LOADED_SITE_LOCAL_SETTINGS': ['settings_composer.tests.settings.sites.test_site.env.local'],
                    'LOADED_SWITCH_DEFINITIONS': ['settings_composer.tests.settings.switch_definitions LOADED BY settings_composer.tests.settings'],
                    'RECURSION': ["settings_composer.tests.settings.recursion.main LOADED BY FUNCTION 'check_recursion' CALLED FROM settings_composer.tests.settings.sites.test_site.env.local UPDATED BY FUNCTION 'recursion_cleaner' CALLED FROM settings_composer.tests.settings.recursion.main LOADED BY FUNCTION 'check_recursion' CALLED FROM settings_composer.tests.settings.sites.test_site.env.local"],
                    'RECURSION_SUCCESS': ["FUNCTION 'inner' CALLED FROM FUNCTION 'recursion_cleaner' CALLED FROM settings_composer.tests.settings.recursion.main LOADED BY FUNCTION 'check_recursion' CALLED FROM settings_composer.tests.settings.sites.test_site.env.local"],
                    'RECURSION_TEST_LIST': ["settings_composer.tests.settings.recursion.main LOADED BY FUNCTION 'check_recursion' CALLED FROM settings_composer.tests.settings.sites.test_site.env.local EXTENDED BY settings_composer.tests.settings.recursion.main LOADED BY FUNCTION 'check_recursion' CALLED FROM settings_composer.tests.settings.sites.test_site.env.local EXCLUDED WITH FUNCTION 'recursion_cleaner' CALLED FROM settings_composer.tests.settings.recursion.main LOADED BY FUNCTION 'check_recursion' CALLED FROM settings_composer.tests.settings.sites.test_site.env.local"],
                    'RECURSIVE_LOADING': ["[SWITCH <recursive: loading> DEFINED IN settings_composer.tests.settings.recursion.switch_definitions LOADED BY FUNCTION 'inner' CALLED FROM FUNCTION 'recursion_cleaner' CALLED FROM settings_composer.tests.settings.recursion.main LOADED BY FUNCTION 'check_recursion' CALLED FROM settings_composer.tests.settings.sites.test_site.env.local] SET BY FUNCTION 'inner' CALLED FROM FUNCTION 'recursion_cleaner' CALLED FROM settings_composer.tests.settings.recursion.main LOADED BY FUNCTION 'check_recursion' CALLED FROM settings_composer.tests.settings.sites.test_site.env.local"],
                    'STUFF': ["settings_composer.tests.settings UPDATED BY FUNCTION 'clean' CALLED FROM settings_composer.tests.settings.cleaning LOADED BY settings_composer.tests.settings EXCLUDED WITH FUNCTION 'clean' CALLED FROM settings_composer.tests.settings.cleaning LOADED BY settings_composer.tests.settings"],
                    'TEMPLATE_DEBUG': ['[SWITCH <debug: on> DEFINED IN settings_composer.tests.settings.switch_definitions LOADED BY settings_composer.tests.settings] SET BY settings_composer.tests.settings.env.local']
                },
            }
        )

    @mock.patch('settings_composer.loading.collate_settings_modules')
    def test_production(self, collate_settings_modules):
        collate_settings_modules.return_value = [
            'settings_composer.tests.settings',
            'settings_composer.tests.settings.env.production',
            'settings_composer.tests.settings.sites.test_site',
            'settings_composer.tests.settings.sites.test_site.env.production'
        ]
        collect_settings(self.settings)
        self.assertEquals(
            self.settings,
            {
                'DEBUG': False,
                'DEBUG_PROPAGATE_EXCEPTIONS': False,
                'LOADED_CLEANING_FUNCTIONS': True,
                'LOADED_CORE_SETTINGS': True,
                'LOADED_LOCAL_SETTINGS': False,
                'LOADED_PRODUCTION_SETTINGS': True,
                'LOADED_SITE_PRODUCTION_SETTINGS': True,
                'LOADED_SWITCH_DEFINITIONS': True,
                'STUFF': {'something': 'anything'},
                'TEMPLATE_DEBUG': False,
                'SETTINGS_COMPOSER_SOURCE': {
                    'DEBUG': [
                        'settings_composer.tests.settings.env.production',
                        '[SWITCH <debug: off> DEFINED IN settings_composer.tests.settings.switch_definitions LOADED BY settings_composer.tests.settings] SET BY settings_composer.tests.settings.env.production'
                    ],
                    'DEBUG_PROPAGATE_EXCEPTIONS': ['[SWITCH <debug: off> DEFINED IN settings_composer.tests.settings.switch_definitions LOADED BY settings_composer.tests.settings] SET BY settings_composer.tests.settings.env.production'],
                    'LOADED_CLEANING_FUNCTIONS': ['settings_composer.tests.settings.cleaning LOADED BY settings_composer.tests.settings'],
                    'LOADED_CORE_SETTINGS': ['settings_composer.tests.settings'],
                    'LOADED_LOCAL_SETTINGS': ['settings_composer.tests.settings.env.production'],
                    'LOADED_PRODUCTION_SETTINGS': ['settings_composer.tests.settings.env.production'],
                    'LOADED_SITE_PRODUCTION_SETTINGS': ['settings_composer.tests.settings.sites.test_site.env.production'],
                    'LOADED_SWITCH_DEFINITIONS': ['settings_composer.tests.settings.switch_definitions LOADED BY settings_composer.tests.settings'],
                    'STUFF': ["settings_composer.tests.settings UPDATED BY FUNCTION 'clean' CALLED FROM settings_composer.tests.settings.cleaning LOADED BY settings_composer.tests.settings EXCLUDED WITH FUNCTION 'clean' CALLED FROM settings_composer.tests.settings.cleaning LOADED BY settings_composer.tests.settings"],
                    'TEMPLATE_DEBUG': ['[SWITCH <debug: off> DEFINED IN settings_composer.tests.settings.switch_definitions LOADED BY settings_composer.tests.settings] SET BY settings_composer.tests.settings.env.production']
                },
            }
        )
