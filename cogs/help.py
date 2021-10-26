import discord
from discord.ext import commands
from datetime import datetime

description = (
    'Use **``sf!help [command]``** to get further info about a command!'
    '\nThumbnail not made by me, credits [here](https://www.pixilart.com/art/mario-block-gif-08908fe58fdb62f '
    '"Takes you to the original post! Go like their post!")')
thumbnail = "https://media.discordapp.net/attachments/756177435032158294/796719056588636210/oie_7133620UaExY78e.gif?width=670&height=670"


class Help(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.group(name="help", invoke_without_command=True)
    async def help(self, ctx):
        counter = 1
        embed = discord.Embed(
            title="StormFall Command List",
            description=
            'Use **``sf!help [command]``** to get further info about a command!\nThumbnail not made by me, credits [here](https://www.pixilart.com/art/mario-block-gif-08908fe58fdb62f "Takes you to the original post! Go like their post!")',
            color=discord.Color.dark_gold())
        embed.set_thumbnail(url=f"{thumbnail}")
        embed.add_field(
            name="**🛠️   Utilities**",
            value=
            f'[``sf!help utilities``](https://hypixel.net/threads/3340014/ "Run the command for further details and the list of utility commands!")',
            inline=True)
        embed.add_field(
            name="**⛈️ Guild-Only**",
            value=
            f'[``sf!help guild``](https://hypixel.net/threads/3340014/ "Run the command for further details and the list of utility commands!")'
        )
        embed.add_field(
            name="ℹ️ Infos",
            value=
            f'[``sf!help info``](https://hypixel.net/threads/3340014/ "Run the command for further details and the list of utility commands!")'
        )
        embed.set_footer(icon_url=ctx.guild.me.avatar_url,
                         text=f"{ctx.guild.me} | Made by Manqekyo#2652")
        embed.timestamp = datetime.utcnow()
        send = await ctx.channel.send(embed=embed)

        # use log
        url = send.jump_url
        logchannel = ctx.guild.get_channel(787986229122564126)
        log = discord.Embed(title="Help Log:",
                            description=f"[Jump to Message]({url})",
                            color=discord.Color.dark_gold())
        log.set_footer(icon_url=ctx.author.avatar_url,
                       text=f'Command ran by {ctx.author.name}')
        log.timestamp = datetime.utcnow()
        await logchannel.send(embed=log)

    @help.command(name="utilities")
    async def utilities(self, ctx):
        embed = discord.Embed(title="StormFall Utilities Commands",
                              description=f'{description}',
                              color=discord.Color.dark_gold())
        embed.set_thumbnail(url=f"{thumbnail}")
        embed.add_field(name="**💡 sf!suggestion**",
                        value=f'Suggest something!')
        send = await ctx.send(embed=embed)

        # use log
        url = send.jump_url
        logchannel = ctx.guild.get_channel(787986229122564126)
        log = discord.Embed(title="Utilities Help Log",
                            description=f"[Jump to Message]({url})",
                            color=discord.Color.dark_gold())
        log.set_footer(icon_url=ctx.author.avatar_url,
                       text=f'Command ran by {ctx.author.name}')
        log.timestamp = datetime.utcnow()
        await logchannel.send(embed=log)

    @help.command(name="guild")
    async def guild(self, ctx):
        emoji = '<:gexp:808761784118149200>'
        embed = discord.Embed(title="StormFall Guild Commands",
                              description=f'{description}',
                              color=discord.Color.dark_gold())
        embed.set_thumbnail(url=f"{thumbnail}")
        embed.add_field(name=f"**{emoji} sf!inactive**",
                        value='Send an inactive notice to the Staff Team')
        send = await ctx.send(embed=embed)

        # use log
        url = send.jump_url
        logchannel = ctx.guild.get_channel(787986229122564126)
        log = discord.Embed(title="Guild Help Log",
                            description=f"[Jump to Message]({url})",
                            color=discord.Color.dark_gold())
        log.set_footer(icon_url=ctx.author.avatar_url,
                       text=f'Command ran by {ctx.author.name}')
        log.timestamp = datetime.utcnow()
        await logchannel.send(embed=log)

    @help.command()
    async def info(self, ctx):
        rain = '🌧️'  # kuha ng rain emoji
        helpemoji = '📖'
        embed = discord.Embed(title=f'Stormfall Information-based Commands',
                              description=f'{description}',
                              color=discord.Color.dark_gold())
        embed.set_thumbnail(url=f'{thumbnail}')
        embed.add_field(
            name=f'**{rain} sf!rain**',
            value=f'Prints information about how to attain the Rain rank!')
        embed.add_field(name=f'**{helpemoji} sf!help**',
                        value=f'Prints the help message!')
        send = await ctx.send(embed=embed)

        # use log
        url = send.jump_url
        logchannel = ctx.guild.get_channel(787986229122564126)
        log = discord.Embed(title="Info Help Log",
                            description=f"[Jump to Message]({url})",
                              color=discord.Color.dark_gold())
        log.set_footer(icon_url=ctx.author.avatar_url,
                       text=f'Command ran by {ctx.author.name}')
        log.timestamp = datetime.utcnow()
        await logchannel.send(embed=log)


def setup(client):
    client.add_cog(Help(client))
