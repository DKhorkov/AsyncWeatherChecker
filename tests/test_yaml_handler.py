from typing import List

from src import YamlHandler, CustomizedSettings, WeatherResource
from .configs import MockData, yaml_config


class TestYamlHandler:

    def test_read_customized_settings_yaml(self) -> None:
        customized_settings: CustomizedSettings = YamlHandler(yaml_config=yaml_config).read_customized_settings_yaml()
        mocked_customized_settings: CustomizedSettings = MockData().customized_settings
        error_message: str = f'{customized_settings} != {mocked_customized_settings}'
        assert customized_settings == mocked_customized_settings, error_message

    def test_read_weather_resources_yaml(self) -> None:
        weather_resources: List[WeatherResource] = YamlHandler(yaml_config=yaml_config).read_weather_resources_yaml()
        mocked_weather_resources: List[WeatherResource] = MockData().weather_resources
        error_message: str = f'{weather_resources} != {mocked_weather_resources}'
        assert weather_resources == mocked_weather_resources, error_message
