from .config import Config
from .yaml_configs import WeatherResource, CustomizedSettings, YamlConfig, yaml_config
from .yaml_handler import YamlHandler


config = Config(
    customized_settings=YamlHandler(yaml_config=yaml_config).read_customized_settings_yaml(),
    weather_resources=YamlHandler(yaml_config=yaml_config).read_weather_resources_yaml()
)

