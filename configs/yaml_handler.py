import yaml

from typing import List

from .yaml_configs import CustomizedSettings, WeatherResource, yaml_config


class YamlHandler:

    @staticmethod
    def read_customized_settings_yaml() -> CustomizedSettings:
        """
        Reads customized settings from .yaml file with according name and return object with parsed data.

        :return: :py:class:`CustomizedSettings` object.
        """

        with open(yaml_config.customized_settings_yaml_path, yaml_config.yaml_file_mode) as yaml_file:
            yaml_data = yaml.safe_load(yaml_file)

        return CustomizedSettings(**yaml_data)

    @staticmethod
    def read_weather_resources_yaml() -> List[WeatherResource]:
        """
        Reads weather resources from .yaml file with according name and return list of object with parsed data.

        :return: List of :py:class:`WeatherResource` objects.
        """

        with open(yaml_config.weather_resources_yaml_path, yaml_config.yaml_file_mode) as yaml_file:
            yaml_data = yaml.safe_load(yaml_file)

        return [
            WeatherResource(**weather_resource) for weather_resource in yaml_data[yaml_config.weather_resources_key]
        ]
