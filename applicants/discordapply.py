import discord
from discord.ext import commands
import sqlite3
database = sqlite3.connect('applicants.db')
cursor = database.cursor()
# table
inac_tba = """CREATE TABLE IF NOT EXISTS 
                    applicant(discord BLOB type UNIQUE,
                            ign TEXT type UNIQUE, 
                            discordID BLOB type UNIQUE)"""
cursor.execute("CREATE TABLE IF NOT EXISTS responseID(msgID REAL type UNIQUE)")
cursor.execute(inac_tba)
cursor.close()

format = "sf!accept userID IGN msgID"
deny_format = "sf!deny userID IGN msgID reason"
class discordApply(commands.Cog):

    def __init__(self, client):
        self.client = client
        
    @commands.command()
    async def delresponses(self, ctx):
        # establish connection to check whether or not MEMBER is an applicant
        db = sqlite3.connect('applicants.db')
        cursor = db.cursor()
        delete = cursor.execute("DELETE FROM applicant")
        db.commit()
        await ctx.send("Deleted")

    @commands.command()
    async def accept(self, ctx, user: discord.Member, ign, msgID):
        # change nickname
        change = await user.edit(nick=ign)
        # give member Accepted role
        role = discord.utils.get(ctx.guild.roles, name = "💯 | Accepted")
        add_role = await user.add_roles(role)
        # send Accepted Message
        message = "Hello! You have been accepted in the StormFall Hypixel Guild (https://discord.gg/ZmQeGvG)! Thank you for applying, and whenever you're ready / free to be invited into the guild, ping a Staff Member in #accepted!"
        send = await user.send(message)
        # react with "ACCEPTED" to msg
        msg = await ctx.fetch_message(msgID)
        await msg.add_reaction('🔴')

    @commands.command()
    async def deny(self, ctx, user: discord.Member, ign, msgID, *, reason):
      # send Denied Message
      message = f"Hello! Sorry to say, but your application to the StormFall Hypixel Guild (https://discord.gg/ZmQeGvG) have been denied. \nThank you for applying, but you can still re-apply once you  reach the Guild Requirements [#requirements].\n\nReason: {reason}"
      send = await user.send(message)

      msg = await ctx.fetch_message(msgID)
      await msg.add_reaction('🇩')
      await msg.add_reaction('🇪')
      await msg.add_reaction('🇳')
      await msg.add_reaction('🇾')

    @deny.error
    async def denied_error(self, ctx, error):
        if isinstance(error, commands.NoPrivateMessage):
            await ctx.send("The applicant does not have DMs enabled! Ping him in #accepted instead!")
        if isinstance(error, commands.UserInputError):
            await ctx.send(f"Use the format! `{deny_format}`")

    @accept.error
    async def accepted_error(self, ctx, error):
        if isinstance(error, commands.NoPrivateMessage):
            await ctx.send("The applicant does not have DMs enabled! Ping him in #accepted instead!")
        if isinstance(error, commands.UserInputError):
            await ctx.send(f"Use the format! `{format}`")
def setup(client):
    client.add_cog(discordApply(client)) 