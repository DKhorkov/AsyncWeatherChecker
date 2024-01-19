from typing import Literal, AnyStr
from pydantic import BaseModel
from collections import namedtuple
from pathlib import Path


class YamlConfig(BaseModel):
    customized_settings_yaml_path: Path = Path('configs/yaml_configs/customized_settings.yaml')
    weather_resources_yaml_path: Path = Path('configs/yaml_configs/weather_resources.yaml')
    weather_resources_key: AnyStr = 'weather_resources'
    yaml_file_mode: Literal['r'] = 'r'


CustomizedSettings: namedtuple = namedtuple(
    'CustomizedSettings',
    [
        'times_to_check',
        'check_interval_in_seconds'
    ]
)

WeatherResource: namedtuple = namedtuple(
    'WeatherResource',
    [
        'name',
        'url',
        'params',
        'headers',
        'weather_attrs'
    ]
)
