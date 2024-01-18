import asyncio
import aiofiles
import aiohttp

from typing import Any, List

from configs import WeatherResource, Config, config
from async_logging_system import logger, Logger


class AsyncWeatherChecker:

    def __init__(self):
        self.__logger: Logger = logger
        self.__config: Config = config

    async def main(self) -> None:
        asyncio.run(self.__check_weather_cycle())

    async def __check_weather_cycle(self) -> None:
        await self.__write_headers_to_file()
        while self.__config.iteration_start_point < self.__config.customized_settings_data.times_to_check:
            await self.__check_weather()
            await asyncio.sleep(self.__config.customized_settings_data.check_interval_in_seconds)

    async def __write_headers_to_file(self) -> None:
        async with aiofiles.open(
                file=self.__config.results_filename,
                mode=self.__config.results_file_mode
        ) as file:

            headers_list: List[str] = [
                weather_resource.name for weather_resource in self.__config.weather_resources
            ]
            await file.write(self.__config.sep.join(headers_list))

    async def __check_weather(self) -> None:
        tasks: List = []
        for weather_resource in self.__config.weather_resources:
            tasks.append(asyncio.create_task(self.__make_weather_request(weather_resource=weather_resource)))

        weather_results = await asyncio.gather(*tasks)
        await self.__write_weather_results_to_file(weather_results=weather_results)

    async def __make_weather_request(self, weather_resource: WeatherResource) -> str:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url=weather_resource.url, params=weather_resource.params) as response:
                    response_json = await response.json()

        except Exception as e:
            await self.__logger.error(
                msg=f'Failed to get weather for city {self.__config.customized_settings_data.city} '
                    f'from {weather_resource.name}.\n'
                    f'Error: {e}\n',
                exc_info=True
            )

        else:
            return response_json[weather_resource.weather_attr]

    async def __write_weather_results_to_file(self, weather_results: tuple[Any]) -> None:
        async with aiofiles.open(
                file=self.__config.results_filename,
                mode=self.__config.results_file_mode
        ) as file:

            pass
