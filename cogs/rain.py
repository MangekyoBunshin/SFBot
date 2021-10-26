import discord
from discord.ext import commands

from datetime import datetime
from datetime import date
from datetime import timedelta
# Rain

class Rain(commands.Cog):

    def __init__(self, client):
        self.client = client
        
    @commands.command(name="rain", brief = 'Command to show @Rain requirements!',
                      description = 'Theses are the base requirements to get the Rain rank!\n'
                                    'Be reminded that these are subjected to change, and that meeting these DOES NOT mean you can/will get Rain 100%!')
    async def rain(self, ctx):
        author = ctx.author.mention
        embed = discord.Embed(title="Base Requirements for Rain")
        embed.add_field(name="1. Be active in/with the community",
                        value="Talk with the other guild members and discord members thru the in-game and in the discord server",
                        inline=False)
        embed.add_field(name="2. Participate in the guild events frequently.", value="_ _", inline=False)
        embed.add_field(name="3. Have not broken any major rules in the past month",
                        value="AKA Do not do anything of the following:\n Saying any racial or homophobic slurs, being disrespectful, toxic, and being a massive dickhead, doxxing someone, and sending any 18+ materials such as links, gifs, pictures and videos.",
                        inline=False)
        embed.add_field(name="4. Being known and trusted by the staff.",
                        value="**Additional tips**: \nHaving many suggestion be accepted would help with the promotion!\nGetting tons of GEXP per week will also help you with the promotion!\nAnd obviously, having a nice reputation with the community.",
                        inline=False)
        embed.set_footer(text="More requirements shall be added as time goes on!")
        aaa = await ctx.send(content=f'{author}', embed=embed)

        # use log
        print("Test 1 Passed")
        url = aaa.jump_url
        print("Test 2 Passed")
        logchannel = ctx.guild.get_channel(787986229122564126)
        embed = discord.Embed(title="Rain Log", description=f"[Jump to Message]({url})", color=discord.Color.dark_gold())
        print("Test 3 Passed")
        embed.set_footer(icon_url=ctx.author.avatar_url, text=f'Command ran by {ctx.author.name}')
        print("Test 4 Passed")
        embed.timestamp = datetime.utcnow()
        print("Test 5 Passed")
        await logchannel.send(embed=embed)

        # add reaction to delete message

        await aaa.add_reaction('🗑️')

        def check(reaction, user):
            return user == ctx.message.author and str(
                reaction.emoji) == "🗑️"

        try:
            reaction, user = await client.wait_for("reaction_add", check=check)
            await ctx.message.delete()
            await aaa.delete()
        except:
            sys.exit()

def setup(client):
    client.add_cog(Rain(client)) 