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

# For Debugging. Enable these features only for this guild
MY_GUILD = discord.Object(id=167319816649179149)

# extending from Bot. Since it inherits Client, so this has more features.
class Client(commands.Bot):
    """This is the bot class that contains all the featureset and responses to user queries"""

    async def setup_hook(self):
        print('Calling setup_hook(self):')

    def set_init_params(self, config: AppConfig):
        """Initialize the client with the config parameters."""
        self.config = config
        print(f'Config: {self.config}')

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

        # chat_gpt_key()  # using it like this for now. Will use compose later.

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

        if message.content.lower() == 'hey stubby! show image':
            await message.channel.send(file = discord.File('./data/stable-diffusion-images-generation.png'))

        # Keep track and disable the message for 10 mins.
        # lang = detect(message.content)
        # if lang == 'de':
        #     await message.channel.send('Sorry the german translator is not active yet.')

        # Need to call this for discord to work properly
        await self.process_commands(message)

    async def on_error(event, *args, **kwargs):
        print(f'error: {event}')
        with open('err.log', 'a') as f:
            if event == 'on_message':
                f.write(f'Unhandled message: {args[0]}\n')
            else:
                raise

# intents = discord.Intents.default()
# intents.message_content = True

# # switch between these 2 as activity for gags.
# watching = discord.Activity(name='you intently', type = discord.ActivityType.watching)
# playing = discord.Game(name='with life')
# client = Client(intents = intents, command_prefix = '!', activity = watching)  # or activity = playing

# bot = commands.Bot(command_prefix='!', intents = intents)

# tree = app_commands.CommandTree(client)
# @client.tree.command(name="test", description="Test to see if slash commands are working")
# async def test(interaction):
#     await interaction.response.send_message("Test")

@commands.hybrid_command(name='catcall')
async def tease(ctx):
    response = "Yo cutie. Waccha up to?"
    await ctx.send(response)

def get_model_type(msg: str) -> str:
    """Extracts the model type from the message."""
    # TODO: Do this in a more robust way.
    if msg.lower().startswith('chat'):
        return 'chat'
    elif msg.lower().startswith('image'):
        return 'image'
    else:
        return 'unknown'

@commands.hybrid_command(name='stubby')
async def stubby_command(ctx, *, arg: str = ""):
    """Stubby command to respond with a message."""
    command_type = get_model_type(arg)

    json_payload = {
        'command': command_type,
        'message': arg
    }

    response = ""
    if command_type != 'chat' and command_type != 'image':
        response = "What can I do for you? I can chat or generate images."
        await ctx.send(response)
        return

    # make an http post call on localhost to get the response based on the command type
    async with aiohttp.ClientSession() as session:
        host = 'localhost'
        port = 8000
        endpoint = 'command'
        if command_type == 'chat':
            host = ctx.bot.config.model_server.chat_server
            port = ctx.bot.config.model_server.chat_port
            endpoint = ctx.bot.config.model_server.chat_uri
        elif command_type == 'image':
            host = ctx.bot.config.model_server.stable_diffusion_server
            port = ctx.bot.config.model_server.stable_diffusion_port
            endpoint = ctx.bot.config.model_server.stable_diffusion_uri

        url = f'http://{host}:{port}/{endpoint}'

        # Should I even handle log injection here? Maybe let's make it a TODO for now.
        logger.info(f'Stubby called url: {url}, json_payload: {json_payload}')

        async with session.post(url, json=json_payload) as response:
            if response.status == 200:
                data = await response.json()
                response = data.get('response', 'No response from server.')
            else:
                response = f'AI servier responded with error:'
                logger.error(f'Error response from server: {response.status}')

    # Send the response back to the discord channel
    await ctx.send(response)


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
    random_status = random.choice([watching, playing])
    client = Client(intents = intents, command_prefix = '!', activity = random_status)  # or activity = playing
    client.set_init_params(config)
    client.add_command(tease)
    client.add_command(stubby_command)

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