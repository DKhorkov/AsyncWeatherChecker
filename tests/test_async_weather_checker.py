from pathlib import Path

import aiofiles

from src import AsyncWeatherChecker, logger
from .async_metaclass import AsyncMetaclass
from .test_configs import test_config


class TestAsyncWeatherChecker(metaclass=AsyncMetaclass):
    """
    Class for testing AsyncWeatherChecker methods.
    """

    @classmethod
    def setup_class(cls):
        """
        PyTest setup method as __init__ analogy.
        """

        cls.async_weather_checker = AsyncWeatherChecker(logger=logger, config=test_config)

    async def test_delete_last_launch_results(self) -> None:
        """
        Creates empty results file, makes sure, that file is created.
        Then deletes the file and makes sure, that now it doesn't exist.
        """

        await self.__create_test_results_file()
        assert Path(test_config.results_file_path).exists()

        # breaking Encapsulation for testing private method:
        await self.async_weather_checker._AsyncWeatherChecker__delete_last_launch_results()

        assert not Path(test_config.results_file_path).exists()

    @staticmethod
    async def __create_test_results_file() -> None:
        async with aiofiles.open(test_config.results_file_path, test_config.results_file_mode) as file:
            await file.write('')

