from collections import deque
from unittest import TestCase

import mock

from settings_composer.manager import (
    ACTION_NAMES,
    ActionContextManager,
    SettingsManager
)


class TestActionContextManager(TestCase):

    def setUp(self):
        self.manager = ActionContextManager(['action_1', 'action_2', 'action_3'])

    def test_init(self):
        self.assertEqual(
            self.manager.action_context_layers,
            {
                'action_1': [],
                'action_2': [],
                'action_3': [],
            }
        )

    def test_create_context_layer(self):
        self.manager.create_context_layer('foo')
        self.manager.create_context_layer('bar')
        self.assertEqual(
            self.manager.action_context_layers,
            {
                'action_1': [('foo', deque()), ('bar', deque())],
                'action_2': [('foo', deque()), ('bar', deque())],
                'action_3': [('foo', deque()), ('bar', deque())]
            }
        )

    def test_add_action(self):
        self.manager.create_context_layer('layer_1')
        self.manager.add_action('action_1', foo=1, bar=2)
        self.manager.create_context_layer('layer_2')
        self.manager.add_action('action_2', FOO=1)
        self.manager.add_action('action_2', BAR=2)
        self.assertEqual(
            self.manager.action_context_layers,
            {
                'action_1': [
                    (
                        'layer_1',
                        deque([{'foo': 1, 'bar': 2}])
                    ),
                    (
                        'layer_2',
                        deque()
                    )
                ],
                'action_2': [
                    (
                        'layer_1',
                        deque()
                    ),
                    (
                        'layer_2',
                        deque([{'BAR': 2}, {'FOO': 1}])
                    )
                ],
                'action_3': [('layer_1', deque()), ('layer_2', deque())]
            }
        )

    def test_consume_actions(self):
        self.manager.create_context_layer('test_1')
        self.manager.add_action('action_3', a='a')
        self.manager.create_context_layer('test_2')
        self.manager.add_action('action_3', b='b')
        self.manager.add_action('action_3', c='c')
        self.assertEqual(
            list(self.manager.consume_actions('action_1')),
            []
        )
        self.assertEqual(
            list(self.manager.consume_actions('action_3')),
            [('test_2', {'b': 'b'}), ('test_2', {'c': 'c'})]
        )
        self.assertEqual(
            self.manager.action_context_layers,
            {
                'action_1': [('test_1', deque())],
                'action_2': [('test_1', deque()), ('test_2', deque())],
                'action_3': [
                    (
                        'test_1',
                        deque([{'a': 'a'}])
                    ),
                ]
            }
        )

    def test_consume_all_actions(self):
        self.manager.create_context_layer('A')
        self.manager.add_action('action_1', one=1, two=2)
        self.manager.add_action('action_1', three=3)
        self.manager.create_context_layer('B')
        self.manager.add_action('action_1', four=4)
        self.manager.create_context_layer('C')
        self.manager.add_action('action_1', five=5)
        self.assertEqual(
            list(self.manager.consume_all_actions('action_1')),
            [
                ('C', {'five': 5}),
                ('B', {'four': 4}),
                ('A', {'one': 1, 'two': 2}),
                ('A', {'three': 3})
            ]
        )
        self.assertEqual(
            self.manager.action_context_layers,
            {
                'action_1': [],
                'action_2': [('A', deque()), ('B', deque()), ('C', deque())],
                'action_3': [('A', deque()), ('B', deque()), ('C', deque())]
            }
        )


class TestSettingsManager(TestCase):

    def setUp(self):
        self.settings = {}
        self.manager = SettingsManager()
        self.manager.bind(self.settings)

    def test_binding(self):
        self.assertEqual(self.manager.is_bound, True)
        self.manager.unbind()
        self.assertEqual(self.manager.is_bound, False)
        with self.assertRaises(AttributeError):
            self.manager.unbind()
        with self.assertRaises(AttributeError):
            self.manager.add_action('load', ['this'])
        with self.assertRaises(AttributeError):
            self.manager.set_source_name('FOO', 'bar')

    def test_create_action_context(self):
        with mock.patch.object(self.manager, 'actions') as action_manager:
            self.manager.create_action_context('test')
            action_manager.create_context_layer.assert_called_with('test')

    def test_add_action(self):
        with mock.patch.object(self.manager, 'actions') as action_manager:
            self.manager.add_action('load', modules=['this', 'that'])
            action_manager.add_action.assert_called_with(
                'load', modules=['this', 'that']
            )

    def test_get_current_actions(self):
        with mock.patch.object(self.manager, 'actions') as action_manager:
            value = self.manager.get_current_actions('load')
            action_manager.consume_actions.assert_called_with('load')
            self.assertEqual(value, action_manager.consume_actions.return_value)

    def test_get_all_actions(self):
        with mock.patch.object(self.manager, 'actions') as action_manager:
            value = self.manager.get_all_actions('load')
            action_manager.consume_all_actions.assert_called_with('load')
            self.assertEqual(value, action_manager.consume_all_actions.return_value)

    # Further testing of manager occurs within acceptance tests in test_settings
