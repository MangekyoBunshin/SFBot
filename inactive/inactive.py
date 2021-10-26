import discord
import sys
import json
import requests
from discord.ext.commands import cooldown, BucketType
from mojang import MojangAPI
from discord.ext import commands
from datetime import datetime
from datetime import timedelta
import datetime 
import sqlite3

# sqlite3
inac = sqlite3.connect('inactives.db')
cursor = inac.cursor()
# table
inac_tba = """CREATE TABLE IF NOT EXISTS inactive(discord TEXT,ign TEXT type UNIQUE, startdate TEXT, enddate TEXT,reason TEXT, timestamp REAL)"""
cursor.execute(inac_tba)
cursor.close()

# functions

async def player_is_in_guild(guild: dict, uuid: str) -> bool:
    for member in guild["guild"]["members"]:
        if member["uuid"] == uuid:
            return True
    return False

# format
format = '``sf!inactive [IGN] [Ending Date (YYYY-MM-DD)]``'

class Inactive(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_role('☁️ | Cloud')
    @cooldown(1, 5, BucketType.user)
    async def inactive(self, ctx, user, day):
    # check if date is valid
        msg = await ctx.reply('Processing... (1/5)')
        try:
            print("Test 1")
            night = datetime.datetime.strptime(day, "%Y-%m-%d").date()
            print("Test 2")
            # check for the date if its in the past or 1y in the future or same day
            time_now = datetime.datetime.now()
            time_365 = time_now + timedelta(days = 365)
            time_1 = time_now - timedelta(days = 1)
            print("Test 3")
            # so that the format of 'night' and 'timebefore' is sam
            timenow = time_now.strftime("%Y-%m-%d")
            timebefore = time_1.strftime("%Y-%m-%d")
            timein365d = time_365.strftime("%Y-%m-%d")
            print("Test 4")
            # check
            if timein365d < str(night):
                await msg.edit(content = 'You cannot register an inactivity date longer than a year!')
                sys.exit()
            elif timebefore > str(night):
                await msg.edit(content = 'Trying to register an inactivity notice that ends in the past? Get outta here! Run the command again but this time with the correct date.')
                sys.exit()
            elif timenow == str(night):
                await msg.edit(content = 'Trying to register an inactivity notice that ends in the same day? Get outta here! Run the command again but this time with the correct date.')
                sys.exit()
            else:
                pass
        except ValueError:
            await msg.edit(content = f'{ctx.author.mention}, please use the correct format! {format}')
            sys.exit()

    # turn the variable night into timestamp for auto removing when timestamp = timestampnow
        print("bro")
        timestamp = datetime.datetime.strptime(day, "%Y-%m-%d").timestamp()
        print("TIMESTAMP of the end date = ", timestamp)
    # check kung ung sinend na IGN ay tama
        await msg.edit(content = f'Checking if the account exists... (2/5)')
        uuid = MojangAPI.get_uuid(user)
        username = MojangAPI.get_username(uuid)
        if not uuid:
            await msg.edit(content = f'You either sent the wrong username or made a typo because that username does not exist!')
        else:
    # check kung nasa StormFall ba o hindi

            await msg.edit(content=f'Checking if the account is in the guild... (3/5)')
            try:
                geld = requests.get('https://api.hypixel.net/guild?key=eba433ff-c57e-48ce-ade9-242242be49f9&name=stormfall').json()
                if await player_is_in_guild(geld, uuid) is False:
                    await msg.edit(content = f'{user} is not in StormFall!')
                else:
                    await msg.edit(content = f'Checking if you already have a notice... (4/5)')

                    ## store data

                    inac = sqlite3.connect('inactives.db')
                    cursor = inac.cursor()
                    aut = ctx.author.id
                    query = """INSERT INTO inactive(discord, ign, startdate, enddate, timestamp) VALUES (?, ?, ?, ?, ?)"""
                    data = (aut, username, timenow, night, timestamp)
                    try:
                        cursor.execute(query, data)
                        inac.commit()
                        await msg.edit(content = f'Storing the data... (5/5)')
                    except sqlite3.Error as er:
                        await msg.edit(content = f'{ctx.author.mention}, you already have an inactivity notice!')
                    inac.close()

                        # msg na issend dun sa #inactive channel

                    startdate = time_now.strftime("%B %d, %Y")
                    enddate = night.strftime("%B %d, %Y")
                    await msg.edit(content = f'Your Inactivity Notice **from {startdate} until {enddate}** has been recorded!')

                        

            except json.JSONDecodeError:
                await msg.edit(content="Hypixel API is currently down. Please try again later.")
       

    @commands.command(pass_context = True)
    async def getinactives(self, ctx):
        inac = sqlite3.connect('inactives.db')
        cursor = inac.cursor()
        fetch = cursor.execute("""SELECT discord, ign, enddate FROM inactive""").fetchall()
        feech = len(fetch)
        send = ""
        await ctx.send(f'There are a total of {feech} inactives')
        if feech == 0:
            sys.exit()
        elif feech != 0:
            msg = await ctx.send(f'Getting the data...')
            send += f'Format: IGN | End Date | Discord ID |\n'
            for row in fetch:
                send += (f'{row[1]} | {row[2]} | {row[0]} |\n')
        await msg.edit(content = send)
        inac.close()
        cursor.close()

    @commands.command()
    @commands.has_permissions(administrator = True)
    async def deleteinactives(self, ctx):
        # use log

        logchannel = ctx.guild.get_channel(787986229122564126)
        log = discord.Embed(title="Delete Inactive Log", description=f"_ _", color=discord.Color.dark_gold())
        log.set_footer(icon_url=ctx.author.avatar_url, text=f'Command ran by {ctx.author.name}')
        log.timestamp = datetime.datetime.utcnow()
        await logchannel.send(embed=log)

        msg = await ctx.send('Deleting data...')
        inac = sqlite3.connect('inactives.db')
        cursor = inac.cursor()
        query = """DELETE from inactive"""
        cursor.execute(query)
        inac.commit()
        await msg.edit(content = f'Data deleted! Table is now empty.')
        inac.close()
        cursor.close()


    @inactive.error
    async def inactive_handler(self, ctx, error):
        if isinstance(error, commands.UserInputError):
            await ctx.send(f"Wrong format! Use the format: {format}")
        elif isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == "ctx":
                await ctx.send(f"You forgot to give the date and reason!\n"
                               f"Format: {format}", delete_after=5)
                msg = ctx.message
                await msg.delete()
            if error.param.name == "Reason":
                await ctx.send("You forgot to give the reason!", delete_after=5)
                msg = ctx.message
                await msg.delete()
        elif isinstance(error, commands.MissingRole):
            await ctx.send("You're not a part of the guild!")
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f'{ctx.author.mention}, the command is in cooldown! (5s cooldown)')

    @getinactives.error
    async def getinac_handler(self, ctx, error):
        if isinstance(error, commands.MissingRole):
            await ctx.send("This command is only for staff members!")

def setup(client):
    client.add_cog(Inactive(client)) 