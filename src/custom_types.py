from typing import Union, NewType, Dict, AnyStr

Temperature = NewType('Temperature', Union[int, float, None])
WeatherResult = NewType('WeatherResult', Dict[AnyStr, Temperature])
