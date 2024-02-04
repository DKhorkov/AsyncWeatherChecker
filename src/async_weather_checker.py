import asyncio
import aiofiles
import aiohttp
import os

from typing import List, Dict, AnyStr, Tuple, Any, Optional, Union

from configs import WeatherResource, Config
from async_logging_system import Logger
from custom_types import Temperature, WeatherResult


class AsyncWeatherChecker:
    """
    Asynchronous weather checker, which makes requests to multiple weather resources (API),
    processing responses from them and saving information into a result file.
    """

    def __init__(self, logger: Logger, config) -> None:
        self.__logger: Logger = logger
        self.__config: Config = config

    def run(self) -> None:
        """
        Startpoint function, which runs weather checker in event loop of asyncio.
        """

        asyncio.run(self.__check_weather())

    async def __check_weather(self) -> None:
        """
        Core logics function of Weather Checker.

        After cleaning last launch data and creating necessary data for current launch, function starts
        iteration cycle of getting weather a number of times, defined by user in according config file.

        After getting and processing received weather, sleeps for a period, also defined by user in according
        config file.
        """

        await self.__delete_last_launch_results()
        await self.__write_headers_to_results_file()

        iterations_number: int = self.__config.iteration_start_point
        while iterations_number < self.__config.customized_settings.times_to_check:
            await self.__poll_weather_resources()
            iterations_number += self.__config.increment_value
            await asyncio.sleep(self.__config.customized_settings.check_interval_in_seconds)

    async def __delete_last_launch_results(self) -> None:
        """
        Deletes last launch results file (.csv) if it exists.
        """

        try:
            os.remove(self.__config.results_file_path)
        except FileNotFoundError:
            pass

    async def __write_headers_to_results_file(self) -> None:
        """
        Creates headers for results file (in .csv format) and writes it to a new results file.
        Headers is a list of sorted weather resources (API) names.

        Purpose of sorting headers is to write results in future in the same order as the according weather resource
        name was written.
        """

        async with aiofiles.open(
            file=self.__config.results_file_path,
            mode=self.__config.results_file_writing_mode
        ) as file:

            headers: List[str] = sorted(
                [weather_resource.name for weather_resource in self.__config.weather_resources]
            )
            headers += self.__config.base_headers
            await file.write(self.__config.sep.join(headers) + self.__config.new_line_arg)

    async def __poll_weather_resources(self) -> None:
        """
        Poll each weather resource (API) for weather.
        Received results will be sorted and written to the results file in .csv format.
        """

        tasks: List = []
        for weather_resource in self.__config.weather_resources:
            task: asyncio.Task = asyncio.create_task(
                coro=self.__make_request_to_weather_resource(weather_resource=weather_resource)
            )
            tasks.append(task)

        weather_results: Tuple[WeatherResult] = await asyncio.gather(*tasks)
        sorted_weather_results: List[WeatherResult] = await self.__sort_weather_results(weather_results=weather_results)
        await self.__write_results_to_file(weather_results=sorted_weather_results)

    async def __make_request_to_weather_resource(self, weather_resource: WeatherResource) -> WeatherResult:
        """
        Trys to receive weather from the resource (API) according params, provided by user in
        corresponding config file.

        After making request to weather resource, awaits until results of response from it will be processed and
        temperature will be got for creating :py:class:`WeatherResult` object purpose.

        :param weather_resource: :py:class:`WeatherResource` object, which contents info about weather resource (API).
        :return: :py:class:`WeatherResult`, which represents weather resource (API) name and temperature,
        which was provided by the resource.
        """

        response_json: Optional[Dict] = None

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

        finally:
            temperature: Temperature = await self.__get_result_from_response(
                response_json=response_json,
                result_keys=weather_resource.result_keys
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

    async def __get_result_from_response(
            self,
            response_json: Optional[Dict],
            result_keys: List[AnyStr]
    ) -> Temperature:
        """
        if response in JSON format from weather API was  NOT received, returns :py:class:`Temperature`
        with default value.

        If response in JSON format from weather API was received, dynamically parses and getting data from it by keys,
        which were provided by user in according configuration file.

        :param response_json: A JSON object with weather data from according API.
        :param result_keys: List of sorted keys for getting temperature from @response_json param.
        :return: :py:class:`Temperature`
        """

        temperature_value: Any = self.__config.default_temperature_value

        if not response_json:
            return Temperature(temperature_value)

        for key in result_keys:
            weather_info: Union[Dict | float | int] = temperature_value if temperature_value else response_json
            temperature_value = weather_info.get(key, None)

        return Temperature(temperature_value)

    async def __write_results_to_file(self, weather_results: List[WeatherResult]) -> None:
        """
        Processes list of :py:class:`WeatherResult` to list of :py:class:`Temperature`,
        awaits calculating average temperature and comprehenses it with the list of temperatures,
        on the basis of which was calculated.

        After processing temperatures, writes results to according file.

        :param weather_results: List of sorted :py:class:`WeatherResult` objects, each of which represents
         weather resource (API) name and temperature, which was provided by the resource.
        """

        temperatures: List[Temperature] = [list(weather_result.values())[0] for weather_result in weather_results]
        average_temperature: Temperature = await self.__calculate_average_temperature(temperatures=temperatures)
        full_weather_results: List[AnyStr] = [str(temperature) for temperature in temperatures + [average_temperature]]

        async with aiofiles.open(
            file=self.__config.results_file_path,
            mode=self.__config.results_file_writing_mode
        ) as file:

            await file.write(self.__config.sep.join(full_weather_results) + self.__config.new_line_arg)

    async def __calculate_average_temperature(self, temperatures: List[Temperature]) -> Temperature:
        """
        Calculate the average temperature based on all weather results from different weather resources.

        :param temperatures: List of :py:class:`Temperature` objects.
        :return: :py:class:`Temperature`
        """

        temperature_sum: float = self.__config.default_average_temperature_value
        results_counter: int = self.__config.default_counter_value
        default_temperature: Temperature = Temperature(self.__config.default_temperature_value)
        for temperature in temperatures:
            if temperature != default_temperature:
                temperature_sum += temperature
                results_counter += self.__config.increment_value

        if results_counter == self.__config.default_counter_value:
            return Temperature(self.__config.default_average_temperature_value)

        average_temperature: float = temperature_sum / results_counter
        rounded_average_temperature: float = round(average_temperature, ndigits=self.__config.temperature_decimal_places)
        return Temperature(rounded_average_temperature)
