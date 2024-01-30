from typing import List, Literal, AnyStr
from pydantic import BaseModel
from pathlib import Path

from .yaml_configs import CustomizedSettings, WeatherResource


class Config(BaseModel):
    customized_settings: CustomizedSettings
    weather_resources: List[WeatherResource]
    iteration_start_point: int = 0
    sep: AnyStr = ','
    results_file_path: Path = Path('./weather_results.csv')
    results_file_writing_mode: Literal['a', 'w+', 'a+'] = 'a+'
    results_file_reading_mode: Literal['r', 'r+'] = 'r'
    default_temperature_value: None = None
    default_average_temperature_value: float = 0.0
    temperature_decimal_places: int = 2
    base_headers: List[AnyStr] = ['Average']
    new_line_arg: AnyStr = '\n'
    increment_value: int = 1
    default_counter_value: int = 0

