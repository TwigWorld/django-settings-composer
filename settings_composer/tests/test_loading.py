from unittest import TestCase

import mock

from settings_composer import constants, loading


class TestLoadingFunctions(TestCase):

    def setUp(self):
        self.environment = {
            constants.SETTINGS_MODULE_VARIABLE_NAME: 'test_module.settings',
            constants.SITE_VARIABLE_NAME: 'test_site',
            constants.ENV_VARIABLE_NAME: 'test_env',
            constants.SWITCHES_VARIABLE_NAME: 'switch_1:off,switch_2:on',
        }

    def test_collate_settings_modules(self):
        with mock.patch('settings_composer.environment.os') as _os:
            _os.environ = self.environment
            self.assertEqual(
                loading.collate_settings_modules(),
                [
                    'test_module.settings',
                    'test_module.settings.env.test_env',
                    'test_module.settings.sites.test_site',
                    'test_module.settings.sites.test_site.env.test_env',
                ]
            )

    @mock.patch('settings_composer.loading.output_if_verbose')
    def test_collate_settings_module_output(self, output_if_verbose):
        with mock.patch('settings_composer.environment.os') as _os:
            _os.environ = self.environment
            loading.collate_settings_modules()
            output_if_verbose.assert_has_calls(
                [
                    mock.call(
                        "Reading environmental variables from OS",
                        "Settings: test_module.settings",
                        "Env: test_env",
                        "Site: test_site",
                        "Switches: switch_1: off, switch_2: on"
                    ),
                    mock.call(
                        "Compiling settings modules based on environmental variables",
                        'test_module.settings',
                        'test_module.settings.env.test_env',
                        'test_module.settings.sites.test_site',
                        'test_module.settings.sites.test_site.env.test_env'
                    )
                ]
            )

    def test_collate_settings_modules_no_site(self):
        with mock.patch('settings_composer.environment.os') as _os:
            del self.environment[constants.ENV_VARIABLE_NAME]
            _os.environ = self.environment
            self.assertEqual(
                loading.collate_settings_modules(),
                [
                    'test_module.settings',
                    'test_module.settings.sites.test_site',
                ]
            )

    def test_collate_settings_modules_no_env(self):
        with mock.patch('settings_composer.environment.os') as _os:
            del self.environment[constants.SITE_VARIABLE_NAME]
            _os.environ = self.environment
            self.assertEqual(
                loading.collate_settings_modules(),
                [
                    'test_module.settings',
                    'test_module.settings.env.test_env'
                ]
            )

    def test_collate_settings_modules_no_site_or_env(self):
        with mock.patch('settings_composer.environment.os') as _os:
            del self.environment[constants.ENV_VARIABLE_NAME]
            del self.environment[constants.SITE_VARIABLE_NAME]
            _os.environ = self.environment
            self.assertEqual(
                loading.collate_settings_modules(),
                [
                    'test_module.settings',
                ]
            )
