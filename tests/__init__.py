import os
import sys

from pathlib import Path

"""
Adding src folder path for correct import of src.configs via importing AsyncWeatherChecker for testing.

https://stackoverflow.com/questions/1896918/running-unittest-with-typical-test-directory-structure
"""
PROJECT_PATH: Path = Path(os.getcwd())
SOURCE_PATH: Path = PROJECT_PATH.joinpath("src")
sys.path.append(SOURCE_PATH.__str__())
