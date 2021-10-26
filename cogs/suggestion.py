import discord
from discord.ext import commands
from datetime import datetime
from discord.ext.commands import cooldown, BucketType

counter = 7
class Suggestion(commands.Cog):

    def __init__(self, client):
        self.client = client

######################################################################
    @commands.command(name="suggestion")
    @cooldown(1, 5, BucketType.user)
    async def suggestion(self, ctx, *, sug):

        # channel to send suggestion at

        channel = ctx.guild.get_channel(755796839277527172)

        # suggestion counter
        global counter
        counter = counter + 1

        # suggestion embed

        sendem = discord.Embed(title=f"**Suggestion #{counter}:**", description=f"``{sug}``",
                               color=discord.Color.gold())
        sendem.set_footer(icon_url=ctx.author.avatar_url, text=f'Suggested by {ctx.author.name}!')
        sendem.timestamp = datetime.utcnow()

        # send msgs

        await channel.send(embed=sendem)
        await ctx.send(f'Okay, cool! Your suggestion has been posted in {channel.mention}!')

        # reaction add
        emoji = discord.utils.get(ctx.guild.emojis, name='downvote')
        emoji2 = discord.utils.get(ctx.guild.emojis, name='upvote')
        await channel.last_message.add_reaction(emoji2)
        await channel.last_message.add_reaction(emoji)

        # use log
        logchannel = ctx.guild.get_channel(757408843260100711)
        log = discord.Embed(title="Suggestion Log:", description=f"**{sug}**", color=discord.Color.dark_gold())
        log.set_footer(icon_url=ctx.author.avatar_url, text=f'Command ran by {ctx.author.name}!')
        await logchannel.send(embed=log)

    @suggestion.error
    async def sugerror(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'{ctx.author.mention}, you forgot to put your suggestion!\n'
                           f'``sf!suggestion <suggestion>``')

        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f'{ctx.author.mention}, the command is in cooldown! (5s cooldown)')

########################################################################################################################





def setup(client):
    client.add_cog(Suggestion(client))