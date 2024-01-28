from typing import Union, NewType, Dict

Temperature = NewType('Temperature', Union[int, float, None])
WeatherResult = NewType('WeatherResult', Dict[str, Temperature])
