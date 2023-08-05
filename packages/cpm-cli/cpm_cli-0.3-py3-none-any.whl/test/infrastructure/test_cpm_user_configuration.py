import unittest
from mock import MagicMock

from cpm.infrastructure.cpm_user_configuration import CpmUserConfiguration
from cpm.infrastructure.cpm_user_configuration import GLOBAL_CONFIGURATION_FILENAME


class TestCpmUserConfiguration(unittest.TestCase):
    def test_loading_configuration_uses_defaults_when_global_configuration_file_does_not_exist(self):
        filesystem = MagicMock()
        filesystem.file_exists.return_value = False
        filesystem.home_directory.return_value = '/home/cpmuser'
        yaml_handler = MagicMock()
        cpm_user_configuration = CpmUserConfiguration(yaml_handler, filesystem)

        cpm_user_configuration.load()

        assert cpm_user_configuration['cpm_hub_url'] == 'http://localhost:8000'
        yaml_handler.load.assert_not_called()
        filesystem.file_exists.assert_called_once_with(f'/home/cpmuser/{GLOBAL_CONFIGURATION_FILENAME}')

    def test_loading_configuration_loads_defaults_on_empty_global_configuration(self):
        filesystem = MagicMock()
        yaml_handler = MagicMock()
        yaml_handler.load.return_value = {}
        filesystem.file_exists.return_value = True
        filesystem.home_directory.return_value = '/home/cpmuser'
        cpm_user_configuration = CpmUserConfiguration(yaml_handler, filesystem)

        cpm_user_configuration.load()

        assert cpm_user_configuration['cpm_hub_url'] == 'http://localhost:8000'
        yaml_handler.load.assert_called_once_with(f'/home/cpmuser/{GLOBAL_CONFIGURATION_FILENAME}')

    def test_loading_configuration_updates_defaults_with_global_configuration_values(self):
        filesystem = MagicMock()
        yaml_handler = MagicMock()
        filesystem.file_exists.return_value = True
        yaml_handler.load.return_value = {'cpm_hub_url': 'http://otherserver.com:8000'}
        cpm_user_configuration = CpmUserConfiguration(yaml_handler, filesystem)

        cpm_user_configuration.load()

        assert cpm_user_configuration['cpm_hub_url'] == 'http://otherserver.com:8000'

