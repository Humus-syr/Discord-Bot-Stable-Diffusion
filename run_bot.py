# intention is to make this a cli launcher to launch either the app or the server using the same application

import logging
import os
from dotenv import load_dotenv
from threading import Thread

from discord_src.utils import utils
from discord_src.bot import discord_bot#, image_client

import discord_src.config.app_config  # load the config store.

import hydra
from omegaconf import DictConfig, OmegaConf
from discord_src.config.app_config import AppConfig



#### INIT CODE HERE
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
CONFIG_PATH = "./discord_src/config/"

# Logger
logging.basicConfig(level=logging.INFO,
					filename = "./logs/py_log.log",
					filemode = "w",
					format = "%(asctime)s %(levelname)s %(message)s")

logger = logging.getLogger(__name__)

logger.info('Initing config')

####INIT ENDS

# os.environ["CUDasdfasf"] = "1"

@hydra.main(version_base = None, config_path=CONFIG_PATH, config_name="config")
def main(cfg: DictConfig) -> None:
	validated_config = AppConfig(**OmegaConf.to_container(cfg, resolve=True))
	logger.setLevel(validated_config.LOG_LEVEL)
	# config_obj = OmegaConf.to_object(config)
	logger.info('Launching bot')

	discord_client = discord_bot.create_discord_client(validated_config)
	discord_client.run(TOKEN)


if __name__ == "__main__":
	main()