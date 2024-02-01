import aiofiles

from pathlib import Path
from typing import AnyStr, List

from src import AsyncWeatherChecker, logger, Temperature, WeatherResult
from .async_metaclass import AsyncMetaclass
from .test_configs import test_config, MockData


class TestAsyncWeatherChecker(metaclass=AsyncMetaclass):
    """
    Class for testing AsyncWeatherChecker methods.

    Test methods breaks Encapsulation of tested class for testing private methods purpose.
    """

    @classmethod
    def setup_class(cls):
        """
        PyTest setup method similar to __init__ in base class.
        """

        cls.async_weather_checker: AsyncWeatherChecker = AsyncWeatherChecker(logger=logger, config=test_config)
        cls.mock_data: MockData = MockData()

    async def test_delete_last_launch_results(self) -> None:
        """
        Creates empty results file, makes sure, that file is created.
        Then deletes the file and makes sure, that now it doesn't exist.
        """

        await self.__create_test_results_file()
        assert Path(test_config.results_file_path).exists()

        await self.async_weather_checker._AsyncWeatherChecker__delete_last_launch_results()
        error_message: AnyStr = f'{Path(test_config.results_file_path)} path still exists!'
        assert not Path(test_config.results_file_path).exists(), error_message

    async def test_delete_last_launch_results_with_no_existing_file(self) -> None:
        """
        Trys to delete the results file, which doesn't exist.
        """

        assert not Path(test_config.results_file_path).exists()
        await self.async_weather_checker._AsyncWeatherChecker__delete_last_launch_results()
        error_message: AnyStr = f'{Path(test_config.results_file_path)} path still exists!'
        assert not Path(test_config.results_file_path).exists(), error_message

    @staticmethod
    async def __create_test_results_file() -> None:
        async with aiofiles.open(test_config.results_file_path, test_config.results_file_writing_mode) as file:
            await file.write('')

    async def test_calculate_average_temperature(self) -> None:
        """
        Checks if the average temperature is equal to mocked correct average temperature.
        """

        average_temperature: Temperature = await self.async_weather_checker._AsyncWeatherChecker__calculate_average_temperature(
            temperatures=self.mock_data.list_of_temperatures
        )
        error_message: AnyStr = f'{average_temperature} != {self.mock_data.average_temperature}!'
        assert average_temperature == self.mock_data.average_temperature, error_message

    async def test_calculate_average_temperature_with_broken_temperature(self) -> None:
        """
        Checks if the average temperature, calculated based on temperatures list with broken temperature,
        equal to average temperature.
        """

        average_temperature: Temperature = await self.async_weather_checker._AsyncWeatherChecker__calculate_average_temperature(
            temperatures=self.mock_data.list_of_temperatures + [self.mock_data.broken_temperature]
        )
        error_message: AnyStr = f'{average_temperature} != {self.mock_data.average_temperature}!'
        assert average_temperature == self.mock_data.average_temperature, error_message

    async def test_calculate_average_temperature_with_empty_temperatures_list(self) -> None:
        """
        Checks if the average temperature, calculated based on empty temperatures list,
        equal to default average temperature.
        """

        average_temperature: Temperature = await self.async_weather_checker._AsyncWeatherChecker__calculate_average_temperature(
            temperatures=[]
        )
        error_message: AnyStr = f'{average_temperature} != {self.mock_data.default_average_temperature}!'
        assert average_temperature == self.mock_data.default_average_temperature, error_message

    async def test_write_headers_to_results_file(self) -> None:
        """
        Checks, that results file will be created and weather headers will be written to it.
        After confirming correct work of method, deletes tested results file.
        """

        assert not Path(test_config.results_file_path).exists()
        await self.async_weather_checker._AsyncWeatherChecker__write_headers_to_results_file()
        assert Path(test_config.results_file_path).exists()

        results_file_data: AnyStr = await self.__read_test_results_file()
        error_message: AnyStr = f'{results_file_data} != {self.mock_data.result_file_headers}!'
        assert results_file_data == self.mock_data.result_file_headers, error_message

        await self.async_weather_checker._AsyncWeatherChecker__delete_last_launch_results()

    @staticmethod
    async def __read_test_results_file() -> AnyStr:
        async with aiofiles.open(test_config.results_file_path, test_config.results_file_reading_mode) as file:
            results_file_data: AnyStr = await file.read()

        return results_file_data

    async def test_get_result_from_response(self) -> None:
        """
        Checks, that necessary information will be correctly retrieved from mocked weather API response,
        using provided result keys for retrieving data from the response.
        """

        result: Temperature = await self.async_weather_checker._AsyncWeatherChecker__get_result_from_response(
            response_json=self.mock_data.response_json,
            result_keys=self.mock_data.result_keys
        )

        error_message: AnyStr = f'{result} != {self.mock_data.temperature_from_response}!'
        assert result == self.mock_data.temperature_from_response, error_message

    async def test_get_result_from_empty_response(self) -> None:
        """
        Checks, that default information will be received, if empty weather API response will be provided.
        """

        result: Temperature = await self.async_weather_checker._AsyncWeatherChecker__get_result_from_response(
            response_json=dict(),
            result_keys=self.mock_data.result_keys
        )

        error_message: AnyStr = f'{result} != {test_config.default_temperature_value}!'
        assert result == test_config.default_temperature_value, error_message

    async def test_get_result_from_response_with_empty_result_keys(self) -> None:
        """
        Checks, that default information will be received, if mocked weather API response and
        empty list of result keys will be provided.
        """

        result: Temperature = await self.async_weather_checker._AsyncWeatherChecker__get_result_from_response(
            response_json=self.mock_data.response_json,
            result_keys=[]
        )

        error_message: AnyStr = f'{result} != {test_config.default_temperature_value}!'
        assert result == test_config.default_temperature_value, error_message

    async def test_get_result_from_empty_response_and_result_keys(self) -> None:
        """
        Checks, that default information will be received, if empty weather API response and
        empty list of result keys will be provided.
        """

        result: Temperature = await self.async_weather_checker._AsyncWeatherChecker__get_result_from_response(
            response_json=dict(),
            result_keys=[]
        )

        error_message: AnyStr = f'{result} != {test_config.default_temperature_value}!'
        assert result == test_config.default_temperature_value, error_message

    async def test_sort_weather_results(self) -> None:
        """
        Checks that sorting weather results working correct.
        """

        sorted_weather_results: List[WeatherResult] = await self.async_weather_checker._AsyncWeatherChecker__sort_weather_results(
            weather_results=self.mock_data.shuffled_weather_results
        )

        error_message: AnyStr = f'{sorted_weather_results} != {self.mock_data.weather_results}!'
        assert sorted_weather_results == self.mock_data.weather_results, error_message

    async def test_write_results_to_file(self) -> None:
        """
        Checks that writing weather results for results file working correct.
        """

        await self.async_weather_checker._AsyncWeatherChecker__write_results_to_file(
            weather_results=self.mock_data.weather_results
        )

        results_file_data: AnyStr = await self.__read_test_results_file()
        error_message: AnyStr = f'{results_file_data} != {self.mock_data.result_file_values_line}!'
        assert results_file_data == self.mock_data.result_file_values_line, error_message

        await self.async_weather_checker._AsyncWeatherChecker__delete_last_launch_results()
