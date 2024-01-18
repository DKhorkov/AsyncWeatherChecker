from typing import List, Literal
from pydantic import BaseModel
from collections import namedtuple
from pathlib import Path

from yaml_configs import CustomizedSettingsData


WeatherResource: namedtuple = namedtuple(
    'WeatherResource',
    [
        'name',
        'url',
        'params',
        'weather_attr'
    ]
)


class Config(BaseModel):
    customized_settings_data: CustomizedSettingsData
    weather_resources: List[WeatherResource]
    iteration_start_point: int = 0
    sep: str = ','
    results_filename: Path = Path('./weather_results.csv')
    results_file_mode: Literal['a', 'w+'] = 'a'

