from unittest import TestCase
from envtypes.types import EnvTypes
from dotenv import load_dotenv

load_dotenv()


class ConfigTypes(TestCase):
    def setUp(self):
        self.custom = EnvTypes(field_del='---',
                               value_del='___',
                               prefix='pyTHON',
                               env_str='sTr',
                               env_int='INt',
                               env_bool='BOOl',
                               env_lists='LiSt',
                               list_del=',,',
                               env_tuples='TuPle',
                               tuple_del=',.,',
                               env_dict='DicT',
                               dict_del=':=:',
                               empty_value='naDa',
                               none_value='nONE')
        self.config = EnvTypes()

    def test_instance(self):
        self.assertIsInstance(self.custom, EnvTypes)
        self.assertIsInstance(self.config, EnvTypes)

    def test_custom(self):
        self.assertEqual(self.custom.field_del, '---')
        self.assertEqual(self.custom.value_del, '___')
        self.assertEqual(self.custom.prefix, 'PYTHON---')
        self.assertEqual(self.custom.env_str, 'str')
        self.assertEqual(self.custom.env_int, 'int')
        self.assertEqual(self.custom.env_bool, 'bool')
        self.assertEqual(self.custom.env_list, 'list')
        self.assertEqual(self.custom.list_del, ',,')
        self.assertEqual(self.custom.env_tuple, 'tuple')
        self.assertEqual(self.custom.tuple_del, ',.,')
        self.assertEqual(self.custom.env_dict, 'dict')
        self.assertEqual(self.custom.dict_del, ':=:')
        self.assertEqual(self.custom.empty_value, 'naDa')
        self.assertEqual(self.custom.none_value, 'nONE')

    def test_config(self):
        self.assertEqual(self.config.field_del, '_')
        self.assertEqual(self.config.value_del, '; _')
        self.assertEqual(self.config.prefix, 'DJANGO_')
        self.assertEqual(self.config.env_str, 'str')
        self.assertEqual(self.config.env_int, 'int')
        self.assertEqual(self.config.env_bool, 'bool')
        self.assertEqual(self.config.env_list, 'list')
        self.assertEqual(self.config.list_del, ', ')
        self.assertEqual(self.config.env_tuple, 'tuple')
        self.assertEqual(self.config.tuple_del, ', ')
        self.assertEqual(self.config.env_dict, 'dict')
        self.assertEqual(self.config.dict_del, ': ')
        self.assertEqual(self.config.empty_value, 'empty')
        self.assertEqual(self.config.none_value, 'none')

    def test_types(self):
        self.assertEqual(self.config.set_env('stR'), 'Just a test')
        self.assertEqual(self.config.set_env('iNt'), 13)
        self.assertEqual(self.config.set_env('bOOl'), False)
        self.assertEqual(self.config.set_env('bOOl_t'), True)
        self.assertFalse(self.config.set_env('bool'))
        self.assertTrue(self.config.set_env('booL_T'))
        self.assertEqual(self.config.set_env('list'), ['first', 'second'])
        self.assertEqual(self.config.set_env('Tuple'), ('third', 'fourth'))
        self.assertEqual(self.config.set_env('DicT'), {'key': 'value'})

    def test_bulk_envs(self):
        self.assertListEqual(self.config.bulk_envs('app', 5),
                             ['1', '2', '3', '4', '5'])

    def test_execptions(self):
        self.assertEqual(self.config.set_env(
            'inferior'), 'The field "inferior" was not found in .env file.')
        self.assertEqual(self.config.set_env(
            'test_value_del'), 'The delimiter "; _" was not found in field value.')
        self.assertEqual(self.config.set_env('test_env_type'),
                         'The "strr" was not defined as a type.')
