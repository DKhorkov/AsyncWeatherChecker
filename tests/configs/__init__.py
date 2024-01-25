from .mock_data import MockData
from .yaml_configs import yaml_config
from src import Config, YamlHandler


config = Config(
    customized_settings=YamlHandler(yaml_config=yaml_config).get_customized_settings(),
    weather_resources=YamlHandler(yaml_config=yaml_config).get_weather_resources()
)
