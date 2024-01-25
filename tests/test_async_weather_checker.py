from pathlib import Path

from src import AsyncWeatherChecker, logger
from .async_metaclass import AsyncMetaclass
from .configs import config


class TestAsyncWeatherChecker(metaclass=AsyncMetaclass):

    @classmethod
    def setup_class(cls):
        """
        PyTest setup method as __init__ analogy.
        """
        cls.async_weather_checker = AsyncWeatherChecker(logger=logger, config=config)

    async def test_delete_last_launch_results(self) -> None:
        with open(config.results_file_path, config.results_file_mode) as file:
            file.write('')
        assert Path(config.results_file_path).exists()

        # breaking Encapsulation for testing private method:
        await self.async_weather_checker._AsyncWeatherChecker__delete_last_launch_results()
        assert not Path(config.results_file_path).exists()


