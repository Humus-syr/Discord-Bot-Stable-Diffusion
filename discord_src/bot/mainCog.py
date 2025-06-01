from discord.ext import commands

class MainCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context = True)
    @commands.has_role("Mod")
    async def acommand(self, ctx, argument):
       await self.bot.say("Stuff")        

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

def setup(bot):
    bot.add_cog(MainCog(bot))