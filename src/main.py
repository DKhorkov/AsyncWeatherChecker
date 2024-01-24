from async_weather_checker import AsyncWeatherChecker
from async_logging_system import logger
from configs import config


if __name__ == '__main__':
    AsyncWeatherChecker(config=config, logger=logger).run()
