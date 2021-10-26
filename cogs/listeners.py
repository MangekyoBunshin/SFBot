import discord
import sys
from discord.ext import commands

class Listeners(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if 'discord.gg' == message.content:
          await message.channel.send(f'{message.author.mention}, you are not allowed to advertise in the StormFall discord!')
          await message.delete()
          


def setup(client):
    client.add_cog(Listeners(client))