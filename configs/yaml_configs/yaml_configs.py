from typing import Literal
from pydantic import BaseModel
from collections import namedtuple
from pathlib import Path


class YamlConfig(BaseModel):
    customized_settings_yaml_name: Path = Path('customized_settings.yaml')
    yaml_file_mode: Literal['r'] = 'r'


CustomizedSettingsData: namedtuple = namedtuple(
    'CustomizedSettingsData',
    [
        'city',
        'times_to_check',
        'check_interval_in_seconds'
    ]
)
