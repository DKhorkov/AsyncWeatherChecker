import os
import sys

from pathlib import Path

"""
Adding src folder path for correct import of src.test_configs via importing AsyncWeatherChecker for testing.

https://stackoverflow.com/questions/1896918/running-unittest-with-typical-test-directory-structure
"""
__PROJECT_PATH: Path = Path(os.getcwd())
__SOURCE_PATH: Path = __PROJECT_PATH.joinpath("src")
sys.path.append(__SOURCE_PATH.__str__())
