from .mock_data import MockData
from .test_yaml_configs import test_yaml_config
from src import Config, YamlHandler


test_config: Config = Config(
    customized_settings=YamlHandler(yaml_config=test_yaml_config).get_customized_settings(),
    weather_resources=YamlHandler(yaml_config=test_yaml_config).get_weather_resources()
)
