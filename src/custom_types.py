from typing import Union, NewType, Dict

Temperature = NewType('Temperature', Union[int, float])
WeatherResult = NewType('WeatherResult', Dict[str, Temperature])
