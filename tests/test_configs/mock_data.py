from typing import List, AnyStr, Dict, Any

from src import WeatherResource, CustomizedSettings, Temperature, WeatherResult
from .test_config import mock_data_config, test_config


class MockData:
    """
    Class, representing mocked data for testing, which will be compared to results of tested classes and methods.
    """

    def __init__(self) -> None:
        self.__create_mocked_customized_settings()
        self.__create_broken_customized_settings()

        self.__create_weather_resources()
        self.__weather_resource = self.__weather_resources[0]
        self.__create_broken_weather_resources()
        self.__broken_weather_resource = self.__broken_weather_resources[0]

        self.__create_list_of_temperatures()
        self.__average_temperature: Temperature = Temperature(mock_data_config.average_temperature_value)
        self.__default_average_temperature: Temperature = Temperature(test_config.default_average_temperature_value)
        self.__broken_temperature: Temperature = Temperature(None)
        self.__temperature_from_response: Temperature = Temperature(mock_data_config.temperature_from_response)

        self.__create_result_file_headers()

        self.__create_response_json()
        self.__result_keys: List[AnyStr] = self.__broken_weather_resource.result_keys

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

    def __create_weather_resources(self) -> None:
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
                    'firstKey',
                    'weather',
                    'temperature'
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

    def __create_result_file_headers(self) -> None:
        """
        Creates mocked headers for weather results file.

        weather_resources_names should be a list of all weather resources names provided
        in "tests/test_configs/test_yaml_configs/weather_resources.yaml" file.
        """

        weather_resources_names: List[AnyStr] = [weather_resource.name for weather_resource in self.__weather_resources]
        headers: AnyStr = test_config.sep.join(weather_resources_names + test_config.base_headers)
        self.__result_file_headers: AnyStr = headers + test_config.new_line_arg

    def __create_response_json(self) -> None:
        """
        Creates mocked response in JSON format with data, which will be gotten from it with @self.__result_keys.

        Mocked response MUST contain nested keys, equal to @self.__result_keys.
        This nesting MUST be in the same order, as the keys in @self.__result_keys.
        """

        self.__response_json: Dict[AnyStr, Any] = {
            'someKey': 'some value for the key',
            'resourceName': 'Some API',
            'system data': {
                'notForOurPurposes': 1234,
                'andThisToo': 5678
            },

            # Necessary data, which must be included in response json:
            'firstKey': {
                'notNecessaryInfo': 'something about region',
                'weather': {
                    'temperature': self.__temperature_from_response
                }
            }
        }

    @property
    def weather_resources(self) -> List[WeatherResource]:
        return self.__weather_resources

    @property
    def weather_resource(self) -> WeatherResource:
        return self.__weather_resource

    @property
    def broken_weather_resources(self) -> List[WeatherResource]:
        return self.__broken_weather_resources

    @property
    def broken_weather_resource(self) -> WeatherResource:
        return self.__broken_weather_resource

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

    @property
    def result_file_headers(self) -> AnyStr:
        return self.__result_file_headers

    @property
    def temperature_from_response(self) -> Temperature:
        return self.__temperature_from_response

    @property
    def response_json(self) -> Dict[AnyStr, Any]:
        return self.__response_json

    @property
    def result_keys(self) -> List[AnyStr]:
        return self.__result_keys
