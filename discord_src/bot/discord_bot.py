import discord
import os
# from discord.ext import commands
from dotenv import load_dotenv
import aiohttp
import random
import openai
import logging

import hydra
from omegaconf import OmegaConf

from discord_src.utils import utils
from discord_src.config.app_config import AppConfig
from discord_src.bot import ai_group

from discord import app_commands
from discord.ext import commands

# Logger
logger = logging.getLogger(__name__)

# TODO: remove this later, we should read this just once in run_bot script and pass it to this function.
# CONFIG_PATH = "./discord_src/utils/config.yml"
# config = utils.load_config(CONFIG_PATH)

# TODO: check this. Env vars not workings
print(f'hydra env va? HYDRA_FULL_ERROR : {os.getenv("HYDRA_FULL_ERROR")}')

# @hydra.main(version_base = '1.3', config_path='../../discord_src/config', config_name="config")
# def do_this(cfg: AppConfig):
#     # print(f'cfg: {cfg}')
#     # return
#     # this line actually runs the checks of pydantic
#     from omegaconf import OmegaConf
#     OmegaConf.to_object(cfg)
#     # log to console and into the `outputs` folder per default
#     print(f"\n{OmegaConf.to_yaml(cfg)}")

#     print(f'habiibi: {cfg.paths.data_path}')

# do_this()

# For Debugging. Enable these features only for this guild
MY_GUILD = discord.Object(id=167319816649179149)

# extending from Bot. Since it inherits Client, so this has more features.
class Client(commands.Bot):
    """This is the bot class that contains all the featureset and responses to user queries"""

    async def setup_hook(self):
        print('Calling setup_hook(self):')

    async def on_ready(self):
        """Initialize some parameters and register slash commands once discord connection is established."""
        await self.tree.sync(guild=MY_GUILD)

        for guild in self.guilds:
            print(f'guild name: {guild}, id: {guild.id}')
            for channel in guild.channels:
                print(f'channel name: {channel}, id: {channel.id}')

        # g_channel = self.get_channel(167319816649179149);
        # await g_channel.send('Hello here!');

        print(f'{self.user} has connected to Discord!')

        # @hydra.main(version_base = '1.3', config_path='../../discord_src/config', config_name="config")
        def chat_gpt_key(cfg: AppConfig):
            # initialize Chat GPT Api if we have the token.
            if cfg.open_ai_fallback:
                openai.api_key = os.getenv('OPENAI_API_KEY')

        chat_gpt_key()  # using it like this for now. Will use compose later.

    async def on_message(self, message):
        """I don't plan to use this often, but this is for adding some secret features."""
        # don't respond to ourselves
        if message.author == self.user:
            return

        print(f'message: {message.content}')

        if message.content == 'ping':
            await message.channel.send('pong')

        if message.content == 'raise exception':
            raise discord.DiscordException

        if message.content == 'show image':
            await message.channel.send(file = discord.File('./data/stable-diffusion-images-generation.png'))

        # Keep track and disable the message for 10 mins.
        # lang = detect(message.content)
        # if lang == 'de':
        #     await message.channel.send('Sorry the german translator is not active yet.')

        # Need to call this for discord to work properly
        await self.process_commands(message)

# intents = discord.Intents.default()
# intents.message_content = True

# # switch between these 2 as activity for gags.
# watching = discord.Activity(name='you intently', type = discord.ActivityType.watching)
# playing = discord.Game(name='with life')
# client = Client(intents = intents, command_prefix = '!', activity = watching)  # or activity = playing

# @client.event
# async def on_error(event, *args, **kwargs):
#     print(f'error: {event}')
#     with open('err.log', 'a') as f:
#         if event == 'on_message':
#             f.write(f'Unhandled message: {args[0]}\n')
#         else:
#             raise

# bot = commands.Bot(command_prefix='!', intents = intents)

# tree = app_commands.CommandTree(client)
# @client.tree.command(name="test", description="Test to see if slash commands are working")
# async def test(interaction):
#     await interaction.response.send_message("Test")


# @client.command(name='catcall')
# async def tease(ctx):
#     response = "Yo cutie. Waccha up to?"
#     await ctx.send(response)

# @client.tree.command(guild=MY_GUILD)
# async def slash(interaction: discord.Interaction, number: int, string: str):
#     await interaction.response.send_message(f'Modify {number=} {string=}', ephemeral=True)

# # Add the slash commands
# client.tree.add_command(ai_group.AIgroup(client, config), guild=MY_GUILD)



def create_discord_client(config: AppConfig) -> discord.Client:
    intents = discord.Intents.default()
    intents.message_content = True

    # switch between these 2 as activity for gags.
    watching = discord.Activity(name='you intently', type = discord.ActivityType.watching)
    playing = discord.Game(name='with life')
    client = Client(intents = intents, command_prefix = '!', activity = watching)  # or activity = playing

    # update_discord_client(client)
    return client


# if __name__ == '__main__':
#     # If we want to run just this file independently
#     load_dotenv()
#     TOKEN = os.getenv('DISCORD_TOKEN')
#     CONFIG_PATH = "utils/config.yml"

#     logging.basicConfig()

#     config = utils.load_config(CONFIG_PATH)

#     client.run(TOKEN)