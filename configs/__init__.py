from .config import Config
from .yaml_configs import WeatherResource, CustomizedSettings
from .yaml_handler import YamlHandler


config = Config(
    customized_settings=YamlHandler.read_customized_settings_yaml(),
    weather_resources=YamlHandler.read_weather_resources_yaml()
)

