from pydantic import BaseModel


class MockDataConfig(BaseModel):
    # Params below should be equal to provided in "tests/configs/yaml_configs/customized_setting.yaml" file:
    times_to_check_weather: int = 10
    check_weather_interval_in_seconds: int = 10


mock_data_config: MockDataConfig = MockDataConfig()
