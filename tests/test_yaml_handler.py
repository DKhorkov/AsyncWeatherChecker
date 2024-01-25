from typing import List

from src import YamlHandler, CustomizedSettings, WeatherResource
from .configs import MockData, yaml_config


class TestYamlHandler:

    def test_get_customized_settings(self) -> None:
        customized_settings: CustomizedSettings = YamlHandler(yaml_config=yaml_config).get_customized_settings()
        mocked_customized_settings: CustomizedSettings = MockData().customized_settings
        error_message: str = f'{customized_settings} != {mocked_customized_settings}'
        assert customized_settings == mocked_customized_settings, error_message

    def test_get_weather_resources(self) -> None:
        weather_resources: List[WeatherResource] = YamlHandler(yaml_config=yaml_config).get_weather_resources()
        mocked_weather_resources: List[WeatherResource] = MockData().weather_resources
        error_message: str = f'{weather_resources} != {mocked_weather_resources}'
        assert weather_resources == mocked_weather_resources, error_message
