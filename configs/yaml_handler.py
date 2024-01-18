import yaml

from yaml_configs import CustomizedSettingsData, yaml_config


class YamlHandler:

    @staticmethod
    def read_customized_settings_yaml() -> CustomizedSettingsData:
        with open(yaml_config.customized_settings_yaml_name, yaml_config.yaml_file_name) as yaml_file:
            raw_customized_settings_data = yaml.safe_load(yaml_file)

        return CustomizedSettingsData(**raw_customized_settings_data)
