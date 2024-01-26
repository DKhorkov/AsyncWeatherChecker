from pathlib import Path

from src import YamlConfig

__config_dir: Path = Path(__file__).parent
__customized_settings_yaml_path: Path = __config_dir / Path('customized_settings.yaml')
__weather_resources_yaml_path: Path = __config_dir / Path('weather_resources.yaml')
test_yaml_config: YamlConfig = YamlConfig(
    customized_settings_yaml_path=__customized_settings_yaml_path,
    weather_resources_yaml_path=__weather_resources_yaml_path
)

