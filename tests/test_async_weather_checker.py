import aiofiles

from pathlib import Path
from typing import AnyStr

from src import AsyncWeatherChecker, logger, Temperature
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
