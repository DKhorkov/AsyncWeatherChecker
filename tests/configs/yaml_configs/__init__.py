from pathlib import Path

from src import YamlConfig

config_dir: Path = Path(__file__).parent
customized_settings_yaml_path: Path = config_dir / Path('customized_settings.yaml')
weather_resources_yaml_path: Path = config_dir / Path('weather_resources.yaml')
yaml_config = YamlConfig(
    customized_settings_yaml_path=customized_settings_yaml_path,
    weather_resources_yaml_path=weather_resources_yaml_path
)

