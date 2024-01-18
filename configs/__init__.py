from config import Config, WeatherResource
from yaml_handler import YamlHandler


config = Config(
    customized_settings_data=YamlHandler.read_customized_settings_yaml()
)

