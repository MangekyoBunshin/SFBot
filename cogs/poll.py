import discord
import asyncio
import sys
import random
import os
import time
from discord import Embed
from discord import Colour
from discord.ext import commands
from discord.ext import tasks
from datetime import datetime



class Poll(commands.Cog):

    def __init__(self, client):
        self.client = client
    # Poll
    poll_counter = 1
    @commands.command(name="poll")
    @commands.has_permissions(administrator=True)
    async def poll(self, ctx, *, sug):
        # other stuff
        channel = client.get_channel(891406132785074196) # Polls channel ID
        global poll_counter
        poll_counter = poll_counter + 1
        emoji = client.get_emoji(766566417632985090) # Downvote emoji ID
        emoji2 = client.get_emoji(766573475657678848) # Upvote emoji ID
        role = ctx.guild.get_role(817587002667958283) # Polls role ID

        # below is the poll message

        poll = await channel.send(f'**Poll #{poll_counter}:**\n{role.mention}\n\n{sug}\n')
        await poll.add_reaction(emoji2)
        await poll.add_reaction(emoji)

def setup(client):
    client.add_cog(Poll(client))