from pathlib import Path

import aiofiles

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
        PyTest setup method as __init__ analogy.
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
        error_message: str = f'{Path(test_config.results_file_path)} path still exists!'
        assert not Path(test_config.results_file_path).exists(), error_message

    @staticmethod
    async def __create_test_results_file() -> None:
        async with aiofiles.open(test_config.results_file_path, test_config.results_file_mode) as file:
            await file.write('')

    async def test_calculate_average_temperature(self) -> None:
        """
        Checks if the average temperature is equal to mocked correct average temperature.
        """

        average_temperature: Temperature = await self.async_weather_checker._AsyncWeatherChecker__calculate_average_temperature(
            temperatures=self.mock_data.list_of_temperatures
        )
        error_message: str = f'{average_temperature} != {self.mock_data.average_temperature}!'
        assert average_temperature == self.mock_data.average_temperature, error_message

    async def test_calculate_average_temperature_with_broken_temperature(self) -> None:
        """
        Checks if the average temperature, calculated based on temperatures list with broken temperature,
        equal to average temperature.
        """

        average_temperature: Temperature = await self.async_weather_checker._AsyncWeatherChecker__calculate_average_temperature(
            temperatures=self.mock_data.list_of_temperatures + [self.mock_data.broken_temperature]
        )
        error_message: str = f'{average_temperature} != {self.mock_data.average_temperature}!'
        assert average_temperature == self.mock_data.average_temperature, error_message

    async def test_calculate_average_temperature_empty_temperatures_list(self) -> None:
        """
        Checks if the average temperature, calculated based on empty temperatures list,
        equal to default average temperature.
        """

        average_temperature: Temperature = await self.async_weather_checker._AsyncWeatherChecker__calculate_average_temperature(
            temperatures=[]
        )
        error_message: str = f'{average_temperature} != {self.mock_data.default_average_temperature}!'
        assert average_temperature == self.mock_data.default_average_temperature, error_message
