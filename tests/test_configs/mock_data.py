from typing import List

from src.configs.config import WeatherResource, CustomizedSettings
from .test_config import mock_data_config


class MockData:
    """
    Class, representing mocked data for testing, which will be compared to results of tested classes and methods.
    """

    def __init__(self) -> None:
        self.__create_mocked_customized_settings()
        self.__create_mocked_weather_resources()

    def __create_mocked_customized_settings(self) -> None:
        self.__customized_settings = CustomizedSettings(
            times_to_check=mock_data_config.times_to_check_weather,
            check_interval_in_seconds=mock_data_config.check_weather_interval_in_seconds
        )

    def __create_mocked_weather_resources(self) -> None:
        """
        Params below should be equal to provided in "tests/test_configs/test_yaml_configs/weather_resources.yaml" file.
        """

        self.__weather_resources = [
            WeatherResource(
                name='OpenMeteo',
                url='https://api.open-meteo.com/v1/forecast',
                params={
                    'latitude': '59.9386300',
                    'longitude': '30.31413001',
                    'current': 'temperature_2m'
                },
                headers={},
                result_keys=[
                    'current',
                    'temperature_2m'
                ]
            )
        ]

    @property
    def weather_resources(self) -> List[WeatherResource]:
        return self.__weather_resources

    @property
    def customized_settings(self) -> CustomizedSettings:
        return self.__customized_settings
