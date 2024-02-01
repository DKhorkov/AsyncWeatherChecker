from pydantic import BaseModel
from typing import List, AnyStr
from pathlib import Path

from src import Config, YamlHandler
from .test_yaml_configs import test_yaml_config


test_config: Config = Config(
    customized_settings=YamlHandler(yaml_config=test_yaml_config).get_customized_settings(),
    weather_resources=YamlHandler(yaml_config=test_yaml_config).get_weather_resources(),
    results_file_path=Path('./test_weather_results.csv')
)


class MockDataConfig(BaseModel):
    # Params below should be equal to provided in
    # "tests/test_configs/test_yaml_configs/customized_setting.yaml" file:
    times_to_check_weather: int = 2
    check_weather_interval_in_seconds: int = 5

    # Params below should NOT be equal to provided in
    # "tests/test_configs/test_yaml_configs/customized_setting.yaml" file:
    broken_times_to_check_weather: int = 10
    broken_check_weather_interval_in_seconds: int = 10

    temperature_values: List[float] = [-5.214, 3.9432, 1.0, -2.43]
    temperature_from_response: float = 15.00

    # Equal to average number from temperature_values, rounded to decimal places,
    # equal to test_config.temperature_decimal_places:
    average_temperature_value: float = -0.68

    # Should be sorted and length equal to length of @temperature_values:
    weather_resources_names: List[AnyStr] = [
        'AppForWeather',
        'OpenMeteo',
        'SomeAPI',
        'YandexWeather',
    ]


mock_data_config: MockDataConfig = MockDataConfig()

