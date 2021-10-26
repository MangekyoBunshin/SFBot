import discord
import math
import asyncio
import sys
import random
import os
import gspread
import sqlite3
import time
from discord import Embed
from discord import Colour
import keep_alive
from discord.ext import commands
from discord.ext import tasks
from datetime import datetime
from mojang import MojangAPI
import requests

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix=['sf!','Sf!','SF!','sF!'], intents=intents, case_insensitive=True)
client.remove_command('help')


token = os.environ.get("DISCORD_BOT_SECRET")

@client.event
async def on_ready():
    print("Bot is online!")
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Version 120391209 at this point"))


#   COG THINGS  #

for filename in os.listdir('./inactive'):
    if filename.endswith('.py'):
        client.load_extension(f'inactive.{filename[:-3]}')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')


for filename in os.listdir('./applicants'):
    if filename.endswith('.py'):
        client.load_extension(f'applicants.{filename[:-3]}')


keys = os.environ['keys']
key = os.environ['api_key']
gc_key = os.environ['gc_key']
counter = 0
@tasks.loop(seconds=60.0)
async def responses():
    # get the spreadsheet
    gc = gspread.service_account(filename="applicants/keys.json")
    sh = gc.open_by_key(os.environ['gc_key'])
    
    # open worksheet
    worksheet = sh.sheet1
    responses = worksheet.get_all_records()

    # check if there's responses or not
    global counter
    counter = counter + 1

    if len(responses) == 0:
        print(f"No responses. ({counter})")
    else:
        # establish database connection
        db = sqlite3.connect('applicants.db')
        cursor = db.cursor()
        # continue
        await asyncio.sleep(1)
        ign = ""
        disc = ""
        timezone = ""
        gamemode = ""
        survey = ""
        timestamp = ""
        gexp = ""

        # embed description
        desc = ""
        for d in responses:
            ign += str(d['IGN'])
            disc += d['Discord']
            timezone += d['Timezone']
            gamemode += d['Gamemode']
            survey += d['Survey']
            timestamp += d['Timestamp']
            gexp += d['WeekGEXP']

        
        # get UUID
        uuid = MojangAPI.get_uuid(ign)
        name = MojangAPI.get_username(uuid)

        # get member
        print(disc)
        user = None
        # run a loop thru every server that the bot is in
        guild = client.get_guild(720219388699213837)
        user = guild.get_member_named(disc)
            # if userID is in the Discord:
        if user:
            try:
                query = """INSERT INTO applicant(discord, ign, discordID) VALUES (?, ?, ?)"""
                id = user.id
                data = (str(user), str(name), int(id))
                cursor.execute(query, data)
                db.commit()
            except sqlite3.IntegrityError:
                print("Already has a response.")
        if user is None:
            user = f"{disc} does not exist / is not in the Discord"
            
        
        # delete the extra characters in GAMEMODE if they chose Skyblock

        if gamemode == "Skyblock (Remember to turn on your Skyblock API! To enable it, go to Skyblock Menu -> Settings -> API access and enable everything!)":
            gamemode = gamemode[:8] + gamemode[132:]
        
        desc += ("───────────────────────────────────────────\n"
                f"**IGN** - `{ign}`\n"
                f"**Discord** - `{user}`\n"
                f"**Main Gamemode(s)** - `{gamemode}`\n"
                f"**Timezone** - `{timezone}`\n"
                f"**Where did they hear about the guild** - `{survey}`\n")
        

        if user == f"{disc} does not exist / is not in the Discord":
            desc += (
                f"**Discord ID** - User does not exist / not in the discord\n───────────────────────────────────────────\n\n"
                f"**R  E  Q  U  I  R  E  M  E  N  T  S**:\n\n"
            )
        else:
            desc += (
            f"**Discord ID** - {user.id}\n───────────────────────────────────────────\n\n"
            f"**R  E  Q  U  I  R  E  M  E  N  T  S**:\n\n")

        # get their stats
        api = requests.get(f'https://api.hypixel.net/player?key={key}&uuid={uuid}').json()
        # emojis
        no = client.get_emoji(720239556007428226)
        yes = client.get_emoji(720239621166071849)
        
        desc += f"\n**     N E T W O R K  E X P**\n\n"
        try:
            network_exp = api["player"]["networkExp"]
            sqrt = math.sqrt(2 * network_exp + 30625)
            calc = int((sqrt / 50) - 2.5)
            network_req = 40
            if calc >= network_req: # he meets the BW Stars requirement
                desc += f"{yes} LVL {calc} ``[LVL {network_req} req]``\n"
            else:
                desc += f"{no} LVL {calc} ``[LVL {network_req} req]``\n"
        except KeyError:
            desc += f"{no} Network Level did not get fetched.\n"
        except TypeError:
            desc += f"{no} Network Level did not get fetched.\n"
        # insert Discord ID, Discord #
        desc += f"\n**     B E D W A R S**\n\n"
        # BWS Stars
        try:
            bw_xp = api["player"]["achievements"]["bedwars_level"]
            bw_star_req = 50
            if bw_xp >= bw_star_req: # he meets the BW Stars requirement
                desc += f"{yes}  {bw_xp} Stars ``[{bw_star_req} star req]``\n"
            else:
                desc += f"{no}  {bw_xp} Stars ``[{bw_star_req} star req]``\n"
        except KeyError:
            desc += f"{no} Bedwars stats did not get fetched.\n"
        except TypeError:
            desc += f"{no} Network Level did not get fetched.\n"
        # BWS Final Kills
        try:
            bw_fk = api["player"]["stats"]["Bedwars"]["final_kills_bedwars"]
            bw_fk_req = 200
            if bw_fk >= bw_fk_req:
                desc += f"{yes}  {bw_fk} Final Kills ``[{bw_fk_req} Final Kills req]``\n"
            else:
                desc += f"{no}  {bw_fk} Final Kills ``[{bw_fk_req} Final Kills req]``\n"
        except:    
            desc += f"{no} Bedwars stats did not get fetched.\n"
        # bedwars wins
        try:
            bw_win = api["player"]["stats"]["Bedwars"]["wins_bedwars"]
            bw_win_req = 90
            if bw_win >= bw_win_req:
                desc += f"{yes}  {bw_win} Wins ``[{bw_win_req} Wins req]``\n"
            else:
                desc += f"{no}  {bw_win} Wins ``[{bw_win_req} Wins req]``\n"
        except:
            desc += f"{no} Bedwars stats did not get fetched.\n"
        
        desc += f"\n**     S K Y W A R S**\n\n"

        # skywars stars
        try:
            sw_xp = api["player"]["achievements"]["skywars_you_re_a_star"]
            sw_xp_req = 6
            if sw_xp >= sw_xp_req:
                desc += f"{yes}  {sw_xp} Stars ``[{sw_xp_req} star req]``\n"
            else:
                desc += f"{no}  {sw_xp} Stars ``[{sw_xp_req} star req]``\n"
        except KeyError:
            desc += f"{no} Skywars stats did not get fetched.\n"

        # skywars kills
        try:
            sw_kill = api["player"]["stats"]["SkyWars"]["kills"]
            sw_kill_req = 600
            if sw_kill >= sw_kill_req:
                desc += f"{yes}  {sw_kill} Kills ``[{sw_kill_req} kills req]``\n"
            else:
                desc += f"{no}  {sw_kill} Kills ``[{sw_kill_req} kills req]``\n"
        except KeyError:
            desc += f"{no} Skywars stats did not get fetched.\n"
        
        desc += f"\n**     D U E L S**\n\n"

        # duel wins
        try:
            wins = api["player"]["stats"]["Duels"]["wins"]
            wins_req = 250
            if wins >= wins_req:
                desc += f"{yes}  {wins} Wins ``[{wins_req} wins req]``\n"
            else:
                desc += f"{no}  {wins} Wins ``[{wins_req} wins req]``\n"
        except KeyError:
            desc += f"{no} Duels stats did not get fetched.\n"

        desc += ("\n\n**For Skyblock Stats, use Maro bot**\n")
        # embed builder
        embed = Embed(title=f"{ign}'s Application",
                    url = f'https://crafatar.com/renders/body/{uuid}',
                    description=desc,
                    colour=discord.Colour.dark_gold())

        embed.set_thumbnail(url=f'https://crafatar.com/renders/body/{uuid}')
        embed.timestamp = datetime.utcnow()
        channel = client.get_channel(765529942468722708)
        send_message = await channel.send(embed=embed)
        msgID = send_message.id
        delete = worksheet.delete_rows(2)
        if user == f"{disc} does not exist / is not in the Discord":
          sends = await channel.send(
            f"Accept -> **`sf!accept [Discord_ID] {ign} {msgID}`**\n"
            f"Deny -> **`sf!deny [Discord_ID] {ign} {msgID} [Reason]`**"
          )
        else:
          sends = await channel.send(
            f"Accept -> **`sf!accept {user.id} {ign} {msgID}`**\n"
            f"Deny -> **`sf!deny {user.id} {ign} {msgID} [Reason]`**"
          )
        # close database
        cursor.close()
        db.close()


@tasks.loop(hours=12.0)
async def timer():
  try:
    # access inactive.db
    connection = sqlite3.connect('inactives.db')
    cursor = connection.cursor()
    # kunin lahat nung inactives
    inactives = cursor.execute("""SELECT * from inactive""").fetchall()
    print("TOTAL INACTIVES COUNT: ", len(inactives))
    # run a loop
    for row in inactives:
      values = (f" | DISCORD: {row[0]}\n"
                f" | IGN: {row[1]}\n"
                f" | Start Date: {row[2]}\n"
                f" | End Date: {row[3]}\n"
                f" | Reason: {row[4]}\n"
                f" | End Date Timestamp: {row[5]}"
                )
      print(values)
      # timestamp now
      now = datetime.now().timestamp()
      strp = datetime.strptime(row[3], "%Y-%m-%d")
      timestamp = datetime.timestamp(strp)
      # compare timestamp now vs timestamp of inactive end date

      if now >= timestamp: # kailangan na iremove ung inactive
        ign = row[1]
        delete = cursor.execute("""DELETE from inactive WHERE ign=?""", (ign,))
        connection.commit()
        print(" | Inactive Deleted |\n")
      elif now <= timestamp: # hindi pa kailangan iremove ung inactive
        print(" | N O T  Y E T |\n")
        continue
  except sqlite3.Error as error:
    print("Failed to delete record from a sqlite table", error) 
    
@client.command()
async def start(ctx):
    responses_loop.start()
    await ctx.send("Started")

# Ping
@client.command()
async def ping(ctx):
     await ctx.send(f'Pong! In {round(client.latency * 1000)}ms')



# Downvote or Upvote

@client.command(name="upvote")
async def getmsg(ctx, msgID: int):
    msg = await ctx.fetch_message(msgID)
    emoji = discord.utils.get(msg.guild.emojis, name='upvote')
    await msg.add_reaction(emoji)
    await ctx.message.add_reaction('👌')
    # use log

    logchannel = ctx.guild.get_channel(787986229122564126)
    log = discord.Embed(title="Help Log:", description=f"", color=discord.Color.dark_gold())
    log.set_footer(icon_url=ctx.author.avatar_url, text=f'Command ran by {ctx.author.name}')
    log.timestamp = datetime.utcnow()
    await logchannel.send(embed=log)


@client.command(name="downvote")
async def getmsg(ctx, msgID: int):
    msg = await ctx.fetch_message(int(msgID))
    emoji = discord.utils.get(msg.guild.emojis, name='downvote')
    await msg.add_reaction(emoji)
    await ctx.message.add_reaction('👌')
    # use log

    logchannel = ctx.guild.get_channel(787986229122564126)
    log = discord.Embed(title="Downvote Log:", description=f"", color=discord.Color.dark_gold())
    log.set_footer(icon_url=ctx.author.avatar_url, text=f'Command ran by {ctx.author.name}')
    log.timestamp = datetime.utcnow()
    await logchannel.send(embed=log)


# Downvote and Upvote reactions
@client.command(name="react")
async def react(ctx, msgID: int):
    msg = await ctx.fetch_message(int(msgID))
    emoji = client.get_emoji(766566417632985090) # Downvote emoji ID
    emoji2 = client.get_emoji(766573475657678848) # Upvote emoji ID
    await msg.add_reaction(emoji2)
    await msg.add_reaction(emoji)
    await ctx.message.delete()
    # use log

    logchannel = ctx.guild.get_channel(787986229122564126)
    log = discord.Embed(title="React Log:", description=f"", color=discord.Color.dark_gold())
    log.set_footer(icon_url=ctx.author.avatar_url, text=f'Command ran by {ctx.author.name}')
    log.timestamp = datetime.utcnow()
    await logchannel.send(embed=log)



# ERROR HANDLERS #

@client.event
async def on_command_error(ctx, error):

    if isinstance(error, commands.CommandNotFound):
        await ctx.send("You've either made a typo, or the command doesn't exist!", delete_after=5)
        msg = ctx.message
        await msg.delete()

    elif isinstance(error, commands.NoPrivateMessage):
        await ctx.send("You cannot use this command in Private Messages!", delete_after=5)
        msg = ctx.message
        await msg.delete()
    
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send('Dont use sf!lol, you dont have permissions lol')

if __name__ == "__main__":
    responses.start()
    timer.start()
    print("GUILD APPLICATIONS TIMER STARTED\n"
    "INACTIVE TIMER STARTED")

keep_alive.keep_alive()
client.run(token)
