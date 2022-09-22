try:
    # Python 2
    from StringIO import StringIO
except ImportError:
    #  Python 3
    from io import StringIO

from unittest import TestCase

import mock

from settings_composer import helpers


class TestHelperFunctions(TestCase):

    @mock.patch.multiple(
        'settings_composer.helpers',
        environment=mock.DEFAULT,
        sys=mock.DEFAULT
    )
    def test_output_if_verbose_not_verbose(self, environment, sys):
        environment.is_verbose.return_value = False
        helpers.output_if_verbose('headline text', 'line 1', 'line 2')
        self.assertEqual(
            sys.stdout.write.call_count,
            0
        )

    @mock.patch.multiple(
        'settings_composer.helpers',
        environment=mock.DEFAULT,
        sys=mock.DEFAULT
    )
    def test_output_if_verbose_headline(self, environment, sys):
        environment.is_verbose.return_value = True
        sys.stdout = StringIO()
        helpers.output_if_verbose('headline text')
        self.assertEqual(
            sys.stdout.getvalue(),
            'Django Settings Composer: headline text\n'
        )

    @mock.patch.multiple(
        'settings_composer.helpers',
        environment=mock.DEFAULT,
        sys=mock.DEFAULT
    )
    def test_output_if_verbose_headline_and_items(self, environment, sys):
        environment.is_verbose.return_value = True
        sys.stdout = StringIO()
        helpers.output_if_verbose('headline text', 'line 1', 'line 2')
        self.assertEqual(
            sys.stdout.getvalue(),
            'Django Settings Composer: headline text\n'
            '  - line 1\n'
            '  - line 2\n'
        )

    def test_load_settings_module(self):
        from . import sample_settings
        loaded_sample_settings = helpers.load_settings_module(
            'settings_composer.tests.sample_settings'
        )
        self.assertEqual(sample_settings, loaded_sample_settings)

    def test_load_settings_module_reload(self):
        sample_settings = helpers.load_settings_module(
            'settings_composer.tests.sample_settings'
        )
        self.assertTrue(sample_settings.THIS_IS_A_SETTING)
        sample_settings.THIS_IS_A_SETTING = False
        helpers.load_settings_module('settings_composer.tests.sample_settings')
        self.assertTrue(sample_settings.THIS_IS_A_SETTING)

    # Not testing for import errors as we are allowing them to propagate

    def test_get_settings_from_module(self):
        module = helpers.load_settings_module(
            'settings_composer.tests.sample_settings'
        )
        self.assertEqual(
            helpers.get_settings_from_module(module),
            {
                'THIS_IS_A_SETTING': True
            }
        )
