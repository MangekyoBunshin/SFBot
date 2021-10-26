import sys
import requests
from mojang import MojangAPI
from discord.ext import commands
from datetime import datetime
from datetime import timedelta
import sqlite3

async def player_is_in_guild(guild: dict, uuid: str) -> bool:
    for member in guild["guild"]["members"]:
        if member["uuid"] == uuid:
            return True
    return False
class StaffInactive(commands.Cog):

    def __init__(self, client):
        self.client = client
        
    @commands.command()
    @commands.has_role('♔ | Staff')
    async def staffinactive(self, ctx, user, day, discord):
        # check if date is valid
        msg = await ctx.send('Processing... (1/5)')
        try:
            night = datetime.strptime(day, "%Y-%m-%d").date()
            # check for the date if its in the past or 1year in the future or same day
            time_now = datetime.now()
            time_365 = time_now + timedelta(days = 365)
            time_1 = time_now - timedelta(days = 1)
            # so that the format of 'night' and 'timebefore' is same
            timenow = time_now.strftime("%Y-%m-%d")
            timebefore = time_1.strftime("%Y-%m-%d")
            timein365d = time_365.strftime("%Y-%m-%d")
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
    # check IGN is correct

        await msg.edit(content = f'Checking if the account exists... (2/5)')
        uuid = MojangAPI.get_uuid(user)
        username = MojangAPI.get_username(uuid)

        if not uuid:
            await msg.edit(content = f'You either sent the wrong username or made a typo because that username does not exist!')
        else:

    # check if in StormFall or no

            await msg.edit(content=f'Checking if the account is in the guild... (3/5)')
            guild = requests.get('https://api.hypixel.net/guild?key=eba433ff-c57e-48ce-ade9-242242be49f9&name=stormfall').json()
            if await player_is_in_guild(guild, uuid) is False:
               await msg.edit(content = f'{user} is not in StormFall!')
            else:
                await msg.edit(content = f'Checking if you already have a notice... (4/5)')

                ## store data

                inac = sqlite3.connect('inactives.db')
                cursor = inac.cursor()
                query = """INSERT INTO inactive(discord, ign, startdate, enddate) VALUES (?, ?, ?, ?)"""
                data = (discord, username, timenow, night)
                try:
                    cursor.execute(query, data)
                    inac.commit()
                    await msg.edit(content = f'Storing the data... (5/5)')
                except sqlite3.Error as er:
                    await msg.edit(content = f'{ctx.author.mention}, you already have an inactivity notice!')
                    sys.exit()
                inac.close()

                # msg that will get sent to #inactive channel

                startdate = time_now.strftime("%B %d, %Y")
                enddate = night.strftime("%B %d, %Y")
                await msg.edit(content = f'{user} Inactivity Notice **from {startdate} until {enddate}** has been recorded!')

    
    @commands.command(pass_context = True)
    async def getstaffinactives(self, ctx):
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
                send += (f'`sf!staffinactive {row[1]} {row[2]} {row[0]}`\n')
            await msg.edit(content = send)
        inac.close()
        cursor.close()

    @staffinactive.error
    async def staffinactive_handler(self, ctx, error):
        if isinstance(error, commands.UserInputError):
            await ctx.send(f"Wrong format! Format:\nsf!staffinactive [IGN] [Date] [Discord ID]")

def setup(client):
    client.add_cog(StaffInactive(client)) 