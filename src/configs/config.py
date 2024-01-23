from typing import List, Literal, AnyStr, LiteralString
from pydantic import BaseModel
from pathlib import Path

from .yaml_configs import CustomizedSettings, WeatherResource


class Config(BaseModel):
    customized_settings: CustomizedSettings
    weather_resources: List[WeatherResource]
    iteration_start_point: int = 0
    sep: AnyStr = ','
    results_file_path: Path = Path('./weather_results.csv')
    results_file_mode: Literal['a', 'w+', 'a+'] = 'a+'
    default_temperature: float = 0.0
    base_headers: List[AnyStr] = ['Average']
    new_line_arg: str = '\n'
    increment_value: int = 1
    default_counter_value: int = 0

