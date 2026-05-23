import os
import yaml
from pathlib import Path
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

CONFIG_PATH = Path(__file__).parent / "config.yaml"

class ConfigModel(BaseModel):
    nse_indexes: dict[str, str] = {}
    mcx_assets: dict[str, str] = {}
    watchlists: dict[str, list[str]] = {}

def load_yaml_config() -> ConfigModel:
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH, "r") as f:
            data = yaml.safe_load(f) or {}
            return ConfigModel(**data)
    return ConfigModel()

_config_data = load_yaml_config()

class Settings(BaseSettings):
    mcp_port: int = 8816
    mcp_host: str = "0.0.0.0"

    # From YAML
    nse_indexes: dict[str, str] = _config_data.nse_indexes
    mcx_assets: dict[str, str] = _config_data.mcx_assets
    watchlists: dict[str, list[str]] = _config_data.watchlists

    model_config = SettingsConfigDict(env_prefix="")

settings = Settings()
