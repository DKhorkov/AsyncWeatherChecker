from typing import List

from src import YamlHandler, CustomizedSettings, WeatherResource
from .test_configs import MockData, test_yaml_config


class TestYamlHandler:
    """
    Class for testing YamlHandler methods.
    """

    def test_get_customized_settings(self) -> None:
        """
        Creates exemplars of CustomizedSettings and compares it to mocked CustomizedSettings.
        """

        customized_settings: CustomizedSettings = YamlHandler(yaml_config=test_yaml_config).get_customized_settings()
        mocked_customized_settings: CustomizedSettings = MockData().customized_settings
        error_message: str = f'{customized_settings} != {mocked_customized_settings}'
        assert customized_settings == mocked_customized_settings, error_message

    def test_get_broken_customized_settings(self) -> None:
        """
        Creates exemplars of CustomizedSettings and compares it to broken CustomizedSettings.
        """

        customized_settings: CustomizedSettings = YamlHandler(yaml_config=test_yaml_config).get_customized_settings()
        broken_customized_settings: CustomizedSettings = MockData().broken_customized_settings
        error_message: str = f'{customized_settings} == {broken_customized_settings}'
        assert customized_settings != broken_customized_settings, error_message

    def test_get_weather_resources(self) -> None:
        """
        Creates exemplars of Weather Resources and compares it to mocked Weather Resources.
        """

        weather_resources: List[WeatherResource] = YamlHandler(yaml_config=test_yaml_config).get_weather_resources()
        mocked_weather_resources: List[WeatherResource] = MockData().weather_resources
        error_message: str = f'{weather_resources} != {mocked_weather_resources}'
        assert weather_resources == mocked_weather_resources, error_message

    def test_get_broken_weather_resources(self) -> None:
        """
        Creates exemplars of Weather Resources and compares it to broken Weather Resources.
        """

        weather_resources: List[WeatherResource] = YamlHandler(yaml_config=test_yaml_config).get_weather_resources()
        broken_weather_resources: List[WeatherResource] = MockData().broken_weather_resources
        error_message: str = f'{weather_resources} == {broken_weather_resources}'
        assert weather_resources != broken_weather_resources, error_message
