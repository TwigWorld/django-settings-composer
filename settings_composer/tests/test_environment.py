from django.core.exceptions import ImproperlyConfigured

from unittest import TestCase

import mock

from settings_composer import constants, environment


class TestEnvironmentFunctions(TestCase):

    def test_get_settings_module_name_error_if_none(self):
        with mock.patch('settings_composer.environment.os') as _os:
            _os.environ = {}
            with self.assertRaises(ImproperlyConfigured):
                environment.get_settings_module_name()

    def test_get_settings_module_name_error_if_empty(self):
        with mock.patch('settings_composer.environment.os') as _os:
            _os.environ = {
                constants.SETTINGS_MODULE_VARIABLE_NAME: ''
            }
            with self.assertRaises(ImproperlyConfigured):
                environment.get_settings_module_name()

    def test_get_settings_module_name(self):
        with mock.patch('settings_composer.environment.os') as _os:
            _os.environ = {
                constants.SETTINGS_MODULE_VARIABLE_NAME: 'my.settings.module'
            }
            self.assertEqual(
                environment.get_settings_module_name(),
                'my.settings.module'
            )

    def test_get_site_name_blank(self):
        with mock.patch('settings_composer.environment.os') as _os:
            _os.environ = {}
            self.assertEqual(
                environment.get_site_name(),
                ''
            )

    def test_get_site_name(self):
        with mock.patch('settings_composer.environment.os') as _os:
            _os.environ = {
                constants.SITE_VARIABLE_NAME: 'mysite'
            }
            self.assertEqual(
                environment.get_site_name(),
                'mysite'
            )

    def test_get_env_name_blank(self):
        with mock.patch('settings_composer.environment.os') as _os:
            _os.environ = {}
            self.assertEqual(
                environment.get_env_name(),
                ''
            )

    def test_get_env_name(self):
        with mock.patch('settings_composer.environment.os') as _os:
            _os.environ = {
                constants.ENV_VARIABLE_NAME: 'testenv'
            }
            self.assertEqual(
                environment.get_env_name(),
                'testenv'
            )

    def test_get_switches_blank_if_none(self):
        with mock.patch('settings_composer.environment.os') as _os:
            _os.environ = {}
            self.assertEqual(environment.get_switches(), {})

    def test_get_switches_blank_if_empty(self):
        with mock.patch('settings_composer.environment.os') as _os:
            _os.environ = {
                constants.SWITCHES_VARIABLE_NAME: '   '
            }
            self.assertEqual(environment.get_switches(), {})

    def test_get_switches_error_if_malformed(self):
        with mock.patch('settings_composer.environment.os') as _os:
            _os.environ = {
                constants.SWITCHES_VARIABLE_NAME: 'bad_switch'
            }
            with self.assertRaises(ImproperlyConfigured):
                environment.get_switches()

    def test_get_switches_error_if_malformed_in_list(self):
        with mock.patch('settings_composer.environment.os') as _os:
            _os.environ = {
                constants.SWITCHES_VARIABLE_NAME: 'good:switch,bad_switch'
            }
            with self.assertRaises(ImproperlyConfigured):
                environment.get_switches()

    def test_get_switches_single_switch(self):
        with mock.patch('settings_composer.environment.os') as _os:
            _os.environ = {
                constants.SWITCHES_VARIABLE_NAME: 'good:switch'
            }
            self.assertEqual(
                environment.get_switches(),
                {'good': 'switch'}
            )

    def test_get_switches_multiple_switches_and_blankspace(self):
        with mock.patch('settings_composer.environment.os') as _os:
            _os.environ = {
                constants.SWITCHES_VARIABLE_NAME: 'good : switch, another:switch, switch_number: three  '
            }
            self.assertEqual(
                environment.get_switches(),
                {
                    'good': 'switch',
                    'another': 'switch',
                    'switch_number': 'three'
                }
            )

    def test_get_switches_error_if_same_switch_used(self):
        with mock.patch('settings_composer.environment.os') as _os:
            _os.environ = {
                constants.SWITCHES_VARIABLE_NAME: 'good:switch,good:switch'
            }
            with self.assertRaises(ImproperlyConfigured):
                environment.get_switches()

    def test_verbose_none(self):
        with mock.patch('settings_composer.environment.os') as _os:
            _os.environ = {}
            self.assertFalse(environment.is_verbose())

    def test_verbose_false(self):
        with mock.patch('settings_composer.environment.os') as _os:
            _os.environ = {
                constants.VERBOSE_VARIABLE_NAME: ''
            }
            self.assertFalse(environment.is_verbose())
            _os.environ = {
                constants.VERBOSE_VARIABLE_NAME: 'False'
            }
            self.assertFalse(environment.is_verbose())
            _os.environ = {
                constants.VERBOSE_VARIABLE_NAME: '12345'
            }
            self.assertFalse(environment.is_verbose())

    def test_verbose_true(self):
        with mock.patch('settings_composer.environment.os') as _os:
            _os.environ = {
                constants.VERBOSE_VARIABLE_NAME: 'True'
            }
            self.assertTrue(environment.is_verbose())
            _os.environ = {
                constants.VERBOSE_VARIABLE_NAME: 'yes'
            }
            self.assertTrue(environment.is_verbose())
            _os.environ = {
                constants.VERBOSE_VARIABLE_NAME: 'Y'
            }
            self.assertTrue(environment.is_verbose())
            _os.environ = {
                constants.VERBOSE_VARIABLE_NAME: ' 1 '
            }
            self.assertTrue(environment.is_verbose())
