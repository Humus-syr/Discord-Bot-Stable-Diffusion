import dataclasses
from typing import Optional

# Pydantic has more validation features, plus it gives us static and runtime type safety.
from pydantic import Field, field_validator
from pydantic.dataclasses import dataclass

from omegaconf import MISSING, DictConfig, OmegaConf
from typing import Any, Dict, List, Type

import hydra  # other option was to use the bison package
from hydra.core.config_store import ConfigStore

@dataclass
class ModelServerParams:
  stable_diffusion_server: str = MISSING
  stable_diffusion_port: int = MISSING
  stable_diffusion_uri: str = MISSING
  chat_server: str = MISSING
  chat_port: int = MISSING
  chat_uri: str = MISSING

@dataclass
class ProjPaths:
  data_path: str = './data'
  log_path: Optional[str] = Field('./logs', title='The folder where log are stored')

@dataclass
class AppConfig:
  open_ai_fallback: bool = MISSING
  LOG_LEVEL: str = 'INFO'  # can be DEBUG, INFO, WARNING, ERROR, CRITICAL
  model_server: ModelServerParams = dataclasses.field(default_factory = ModelServerParams)  # model params
  paths: ProjPaths = dataclasses.field(default_factory = ProjPaths)

  @field_validator("LOG_LEVEL")
  @classmethod
  def validate_log_level(cls, v: str) -> str:
    log_options = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
    if v not in log_options:
      raise ValueError(f"'LOG_LEVEL' must be from this list: {log_options} but got '{v}'")
    return v

  
  @classmethod
  def from_dict(cls, cfg: Dict[str, Any]):
      return cls(**OmegaConf.to_container(cfg, resolve=True))

# Register the AppConfig with Hydra's ConfigStore
cs = ConfigStore.instance()
cs.store(name = 'app_config', node = AppConfig)

# Testing code here
@hydra.main(version_base = None, config_path='.', config_name="config")
def get_config(cfg: DictConfig):
    # print(f'Loaded config: {OmegaConf.to_yaml(cfg)}')
    # return OmegaConf.to_object(cfg)
    validated_config = AppConfig(**OmegaConf.to_container(cfg, resolve=True))
    # print(type(validated_config))
    # return validated_config

if __name__ == '__main__':
  print(f'hi. erer')
  get_config()
