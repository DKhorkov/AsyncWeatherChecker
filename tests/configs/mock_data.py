from typing import List

from src.configs.config import WeatherResource, CustomizedSettings
from .config import test_config


class MockData:

    def __init__(self) -> None:
        self.__customized_settings = CustomizedSettings(
            times_to_check=test_config.times_to_check_weather,
            check_interval_in_seconds=test_config.check_weather_interval_in_seconds
        )

        # Params below should be equal to provided in "tests/configs/yaml_configs/weather_resources.yaml" file:
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
