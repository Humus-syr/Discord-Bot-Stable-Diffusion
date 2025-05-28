import dataclasses
from typing import Optional

# Pydantic has more validation features, plus it gives us static and runtime type safety.
from pydantic import Field
from pydantic.dataclasses import dataclass

from omegaconf import MISSING

import hydra  # other option was to use the bison package
from hydra.core.config_store import ConfigStore

@dataclass
class ModelServerParams:
  # sd_server: str = MISSING
  # sd_port: int = MISSING
  # sd_uri: str = MISSING

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


cs = ConfigStore.instance()
cs.store(name = 'app_config', node = AppConfig)
# cs.store(name="config2", node=MySQLConfig(host="test.db", port=3307))


# Testing code here
# @hydra.main(version_base = None, config_path='.', config_name="config")
# def do_this(cfg: AppConfig):
#     # print(f'cfg: {cfg}')
#     # return
#     # this line actually runs the checks of pydantic
#     from omegaconf import OmegaConf
#     OmegaConf.to_object(cfg)
#     # log to console and into the `outputs` folder per default
#     print(f"\n{OmegaConf.to_yaml(cfg)}")

#     print(f'habiibi: {cfg.paths.data_path}')

# if __name__ == '__main__':
#   print(f'hi. erer')
#   do_this()