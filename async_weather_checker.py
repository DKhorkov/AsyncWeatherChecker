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
        """
        Startpoint function, which runs weather checker in event loop of asyncio.
        """
        asyncio.run(self.__check_weather_cycle())

    async def __check_weather_cycle(self) -> None:
        """
        Core logics function of Weather Checker.
        After cleaning last launch data and creating necessary data for current launch, function starts
        iteration cycle of getting weather a number of times, defined by user in according config file.
        After getting and processing received weather, sleeps for a period, also defined by user in according
        config file.
        """
        await self.__delete_last_launch_results()
        await self.__write_headers_to_file()

        iter_start_point: int = self.__config.iteration_start_point
        while iter_start_point < self.__config.customized_settings.times_to_check:
            await self.__check_weather()
            iter_start_point += self.__config.increment_value
            await asyncio.sleep(self.__config.customized_settings.check_interval_in_seconds)

    async def __delete_last_launch_results(self) -> None:
        """
        Deletes last launch results file (.csv) if it exists.
        """
        try:
            os.remove(self.__config.results_file_path)
        except FileNotFoundError as e:
            await self.__logger.error(
                msg=f'Could not delete last session results file.\n'
                    f'Error: {e}',
                exc_info=True
            )

    async def __write_headers_to_file(self) -> None:
        """
        Creates headers for results file (in .csv format) and writes it to a new results file.
        Headers is a list of sorted weather resources (APIs) names.
        Purpose of sorting headers is to write results in future in the same order as the according weather resource
        name was written.
        """
        async with aiofiles.open(
            file=self.__config.results_file_path,
            mode=self.__config.results_file_mode
        ) as file:

            headers: List[str] = sorted(
                [weather_resource.name for weather_resource in self.__config.weather_resources]
            )
            headers += self.__config.base_headers
            await file.write(self.__config.sep.join(headers) + self.__config.new_line_arg)

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

                    response_json = await response.json(content_type=None)

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
        """
        Sorts weather results by name of weather resource (API), from which the result was received for purpose of
        writing results in the same order, as headers with weather resources names were written to the result file.

        :param weather_results: Tuple of :py:class:`WeatherResult` objects, received from asyncio.gather() method.
        :return: List of sorted :py:class:`WeatherResult` objects.
        """

        # Processes every WeatherResult from received tuple and unites in to single dictionary for sorting next:
        united_weather_results = {}
        for result in weather_results:
            weather_resource_name, temperature = list(result.items())[0]
            united_weather_results[weather_resource_name] = temperature

        sorted_weather_results: List[WeatherResult] = [
            WeatherResult(
                {weather_result[0]: weather_result[1]}
            ) for weather_result in sorted(united_weather_results.items())
        ]

        return sorted_weather_results

    async def __get_weather_from_response(self, response_json: Dict, weather_attrs: List[AnyStr]) -> Temperature:
        """
        Dynamically parses response in JSON format from weather API and getting data from it by keys,
        which were provided by user in according configuration file.

        :param response_json: A JSON object with weather data from according API.
        :param weather_attrs: List of sorted keys for getting temperature from @response_json param.
        :return: :py:class:`Temperature`
        """
        result = None
        for attr in weather_attrs:
            weather_info: Dict = result if result else response_json
            result: Any = weather_info.get(attr, None)

        return Temperature(result) if result else Temperature(self.__config.default_temperature)

    async def __write_weather_results_to_file(self, weather_results: List[WeatherResult]) -> None:
        temperatures: List[Temperature] = [list(weather_result.values())[0] for weather_result in weather_results]
        average_temperature: Temperature = await self.__calculate_average_temperature(temperatures=temperatures)
        temperatures_to_write: List[str] = [str(temperature) for temperature in temperatures + [average_temperature]]

        async with aiofiles.open(
            file=self.__config.results_file_path,
            mode=self.__config.results_file_mode
        ) as file:

            await file.write(self.__config.sep.join(temperatures_to_write) + self.__config.new_line_arg)

    async def __calculate_average_temperature(self, temperatures: List[Temperature]) -> Temperature:
        """
        Calculate the average temperature based on all weather results from different weather resources.

        :param temperatures: List of :py:class:`Temperature` objects.
        :return: :py:class:`Temperature`
        """
        temperature_sum: float = 0
        results_counter: int = self.__config.default_counter_value
        for temperature in temperatures:
            if temperature != self.__config.default_temperature:
                temperature_sum += temperature
                results_counter += self.__config.increment_value

        # Avoiding ZeroDivisionError:
        if results_counter == self.__config.default_counter_value:
            results_counter = self.__config.increment_value

        average_temperature: float = temperature_sum / results_counter
        return Temperature(average_temperature)
