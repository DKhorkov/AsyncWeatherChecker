import asyncio
import aiofiles
import aiohttp
import os

from typing import List, Dict, AnyStr, Tuple, Any

from configs import WeatherResource, Config, config
from async_logging_system import logger, Logger
from custom_types import Temperature, WeatherResult


class AsyncWeatherChecker:

    def __init__(self):
        self.__logger: Logger = logger
        self.__config: Config = config

    def run(self) -> None:
        asyncio.run(self.__check_weather_cycle())

    async def __check_weather_cycle(self) -> None:
        await self.__delete_last_session_results()
        await self.__write_headers_to_file()
        while self.__config.iteration_start_point < self.__config.customized_settings.times_to_check:
            await self.__check_weather()
            await asyncio.sleep(self.__config.customized_settings.check_interval_in_seconds)

    async def __delete_last_session_results(self) -> None:
        try:
            os.remove(self.__config.results_file_path)
        except FileNotFoundError as e:
            self.__logger.exception(
                f'Could not delete last session results file.\n'
                f'Error: {e}'
            )

    async def __write_headers_to_file(self) -> None:
        async with aiofiles.open(
                file=self.__config.results_file_path,
                mode=self.__config.results_file_mode
        ) as file:

            # Sorting list for purposes of writing weather results in the same order later
            headers: List[str] = sorted(
                [weather_resource.name for weather_resource in self.__config.weather_resources]
            )
            await file.write(self.__config.sep.join(headers))

    async def __check_weather(self) -> None:
        tasks: List = []
        for weather_resource in self.__config.weather_resources:
            tasks.append(asyncio.create_task(self.__make_weather_request(weather_resource=weather_resource)))

        weather_results: Tuple[WeatherResult] = await asyncio.gather(*tasks)
        sorted_weather_results: List[WeatherResult] = await self.__sort_weather_results(weather_results=weather_results)
        await self.__write_weather_results_to_file(weather_results=sorted_weather_results)

    async def __make_weather_request(self, weather_resource: WeatherResource) -> WeatherResult:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    url=weather_resource.url,
                    params=weather_resource.params,
                    headers=weather_resource.headers
                ) as response:

                    response_json = await response.json()

        except Exception as e:
            await self.__logger.error(
                msg=f'Failed to get weather from {weather_resource.name}.\n'
                    f'Error: {e}\n',
                exc_info=True
            )

        else:
            temperature: Temperature = await self.__get_weather_from_response(
                response_json=response_json,
                weather_attrs=weather_resource.weather_attrs
            )

            return WeatherResult({weather_resource.name: temperature})

    @staticmethod
    async def __sort_weather_results(weather_results: Tuple[WeatherResult]) -> List[WeatherResult]:
        united_weather_results = {}
        for result in weather_results:
            weather_resource_name, temperature = result.items()
            united_weather_results[weather_resource_name] = temperature

        sorted_weather_results: List[WeatherResult] = [
            WeatherResult(
                {weather_result[0]: weather_result[1]}
            ) for weather_result in sorted(united_weather_results.items())
        ]

        return sorted_weather_results

    @staticmethod
    async def __get_weather_from_response(response_json: Dict, weather_attrs: List[AnyStr]) -> Temperature:
        result = None
        for attr in weather_attrs:
            result: Any = response_json.get(attr, None)

        return Temperature(result) if result else Temperature()

    async def __write_weather_results_to_file(self, weather_results: List[WeatherResult]) -> None:
        temperatures: List[Temperature] = [list(weather_result.values())[0] for weather_result in weather_results]
        average_temp: Temperature = await self.__calculate_average_temp(weather_results=weather_results)
        temperatures_to_write: List[str] = [str(temperature) for temperature in temperatures + [average_temp]]

        async with aiofiles.open(
                file=self.__config.results_file_path,
                mode=self.__config.results_file_mode
        ) as file:

            await file.write(self.__config.sep.join(temperatures_to_write))

    @staticmethod
    async def __calculate_average_temp(weather_results: List[WeatherResult]) -> Temperature:
        temp_sum: float = 0
        for weather_result in weather_results:
            temp_sum += list(weather_result.values())[0]

        average_temp: float = temp_sum / len(weather_results)
        return Temperature(average_temp)
