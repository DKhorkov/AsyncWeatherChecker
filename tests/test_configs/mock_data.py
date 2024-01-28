from typing import List

from src import WeatherResource, CustomizedSettings, Temperature, WeatherResult
from .test_config import mock_data_config, test_config


class MockData:
    """
    Class, representing mocked data for testing, which will be compared to results of tested classes and methods.
    """

    def __init__(self) -> None:
        self.__create_mocked_customized_settings()
        self.__create_broken_customized_settings()

        self.__create_mocked_weather_resources()
        self.__create_broken_weather_resources()

        self.__create_list_of_temperatures()
        self.__average_temperature: Temperature = Temperature(mock_data_config.average_temperature_value)
        self.__default_average_temperature: Temperature = Temperature(test_config.default_average_temperature_value)
        self.__broken_temperature: Temperature = Temperature(None)

    def __create_mocked_customized_settings(self) -> None:
        self.__customized_settings = CustomizedSettings(
            times_to_check=mock_data_config.times_to_check_weather,
            check_interval_in_seconds=mock_data_config.check_weather_interval_in_seconds
        )

    def __create_broken_customized_settings(self) -> None:
        self.__broken_customized_settings = CustomizedSettings(
            times_to_check=mock_data_config.broken_times_to_check_weather,
            check_interval_in_seconds=mock_data_config.broken_check_weather_interval_in_seconds
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

    def __create_broken_weather_resources(self) -> None:
        """
        Incorrect weather resources for negative testing of YamlHandler.
        """

        self.__broken_weather_resources = [
            WeatherResource(
                name='NonExistentWeatherResource',
                url='https://does-not-exist',
                params={
                    'latitude': '59.9386300',
                    'longitude': '30.31413001'
                },
                headers={},
                result_keys=[
                    'noMatterWhat'
                ]
            )
        ]

    def __create_list_of_temperatures(self) -> None:
        """
        Creates list of temperatures, each of which has random float value in diapason of provided min and max
        temperatures up to number decimal places.
        All these input data is provided in "tests/test_configs/test_config.py"
        """

        self.__list_of_temperatures: List[Temperature] = []
        for value in mock_data_config.temperature_values:
            rounded_value: float = round(value, ndigits=test_config.temperature_decimal_places)
            temperature: Temperature = Temperature(rounded_value)
            self.__list_of_temperatures.append(temperature)

    @property
    def weather_resources(self) -> List[WeatherResource]:
        return self.__weather_resources

    @property
    def broken_weather_resources(self) -> List[WeatherResource]:
        return self.__broken_weather_resources

    @property
    def customized_settings(self) -> CustomizedSettings:
        return self.__customized_settings

    @property
    def broken_customized_settings(self) -> CustomizedSettings:
        return self.__broken_customized_settings

    @property
    def list_of_temperatures(self) -> List[Temperature]:
        return self.__list_of_temperatures

    @property
    def average_temperature(self) -> Temperature:
        return self.__average_temperature

    @property
    def broken_temperature(self) -> Temperature:
        return self.__broken_temperature

    @property
    def default_average_temperature(self) -> Temperature:
        return self.__default_average_temperature

