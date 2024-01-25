import yaml

from typing import List

from .yaml_configs import CustomizedSettings, WeatherResource, YamlConfig


class YamlHandler:
    """
    A class for working with YAML files, reading data from them and writing data to.
    """

    def __init__(self, yaml_config: YamlConfig) -> None:
        self.__yaml_config: YamlConfig = yaml_config

    def get_customized_settings(self) -> CustomizedSettings:
        """
        Reads customized settings from .yaml file with according name and return object with parsed data.

        :return: :py:class:`CustomizedSettings` object.
        """

        with open(self.__yaml_config.customized_settings_yaml_path, self.__yaml_config.yaml_file_mode) as yaml_file:
            yaml_data = yaml.safe_load(yaml_file)

        return CustomizedSettings(**yaml_data)

    def get_weather_resources(self) -> List[WeatherResource]:
        """
        Reads weather resources from .yaml file with according name and return list of object with parsed data.

        :return: List of :py:class:`WeatherResource` objects.
        """

        with open(self.__yaml_config.weather_resources_yaml_path, self.__yaml_config.yaml_file_mode) as yaml_file:
            yaml_data = yaml.safe_load(yaml_file)

        return [
            WeatherResource(**weather_resource) for weather_resource in yaml_data[self.__yaml_config.weather_resources_key]
        ]
