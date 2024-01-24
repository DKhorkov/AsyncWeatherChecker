import pytest

from src import AsyncWeatherChecker, logger
from .configs import config


@pytest.fixture
def async_weather_checker() -> AsyncWeatherChecker:
    async_weather_checker: AsyncWeatherChecker = AsyncWeatherChecker(logger=logger, config=config)
    return async_weather_checker


@pytest.mark.usefixtures("async_weather_checker")
class TestAsyncWeatherChecker:
    pass
