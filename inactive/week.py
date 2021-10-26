import discord
import asyncio
import sys
import json
import random
import os
import keep_alive
import requests
from discord.ext.commands import cooldown, BucketType
from mojang import MojangAPI
from discord.ext import commands
from datetime import datetime
from datetime import date
from datetime import timedelta
import time
import sqlite3
from threading import Thread
from natsort import natsorted

class Week(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command() 
    async def week(self, ctx):
        msg = await ctx.reply("Gathering information")
        guild = requests.get('https://api.hypixel.net/guild?key=eba433ff-c57e-48ce-ade9-242242be49f9&name=stormfall').json()
        desc = []
        # get inactive.db connection
        db = sqlite3.connect('inactives.db')
        c = db.cursor()
        # get the ppl who has under 5k GEXP
        for member in guild["guild"]["members"]:
            all_gexp = sum(member["expHistory"].values())
            uuid = member["uuid"]
            username = MojangAPI.get_username(uuid)
            if sum(member["expHistory"].values()) < 5000:
                print("7")
                c.execute("SELECT ign FROM inactive WHERE ign = ?", (username,))
                print("8")
                # merong inactive
                if c.fetchone():
                    print(f'{username} - Has Inactive Notice')
                    continue
                else: # walang inactive
                    now = datetime.now()
                    ts = datetime.timestamp(now)
                    date_7_days_ago = now - timedelta(days=7) 
                    ts_7d_ago = datetime.timestamp(date_7_days_ago) 
                    seconds = int(round(ts_7d_ago * 1000)) 
                    join = member["joined"] # timestamp from when the member joined
                    # calculate whether the member joined recently (within 7 days of current date)
                    if join > seconds: # they joined within 7 days
                        continue
                    elif join < seconds:
                        print(f'{username} - No Inactive Notice')
                        append = f'{all_gexp}={username}'
                        desc.append(append)
        sort = natsorted(desc)
        count = len(desc)
        new_desc = []
        for i in range(1,count):
            a = sort[-i]
            aa = f"{a}"
            indexx = aa.index('=')
            append = f"{aa[1 + indexx:]} - {aa[:indexx]}"
            new_desc.append(append)

        final_desc = ""
        for i, num in enumerate(new_desc, start=1):
          final_desc += f"[#{i}] {num}\n"
        
        desc = f"```css\n{final_desc}```"
        embed = discord.Embed(
          title = f'StormFall Members with < 5000 GEXP in a Week',
          description = f'{desc}',
          url = f'https://hypixel.net/threads/⚡-stormfall-⚡-storm-level-43-gold-tag-level-3-discord.3340014/post-32276018',
          color = discord.Color.gold())
        
        await msg.edit(embed=embed)
        db.close()
        c.close()

def setup(client):
    client.add_cog(Week(client)) 