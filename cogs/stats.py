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

class Stats(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name="stats")
    async def stats(self, ctx, ign):
        print("Test 1 Passed")
        uuid = MojangAPI.get_uuid(ign)
        name = MojangAPI.get_username(uuid)
        if not uuid:
            await ctx.send(f"{ign} does not exist."
                            "Fix your typos, or MojangAPI is down.")
        else:
            print("Test 2 Passed")
            api = requests.get(f'https://api.hypixel.net/player?key=eba433ff-c57e-48ce-ade9-242242be49f9&uuid={uuid}').json()
            desc = ""
            print("Test 3 Passed")
            # emojis
            yes = '✅'
            no = '🚫'
            print("Test 4 Passed")
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
            print("Test 5 Passed")
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
            print("Test 6 Passed")
            try:
                bw_win = api["player"]["stats"]["Bedwars"]["wins_bedwars"]
                bw_win_req = 90
                if bw_win >= bw_win_req:
                    desc += f"{yes}  {bw_win} Wins ``[{bw_win_req} Wins req]``\n"
                else:
                    desc += f"{no}  {bw_win} Wins ``[{bw_win_req} Wins req]``\n"
            except:
                desc += f"{no} Bedwars stats did not get fetched.\n"
            print("Test 7 Passed")
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
            print("Test 8 Passed")
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
            print("Test 9 Passed")
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
            print("Test 10 Passed")
            # embed builder
            embed = discord.Embed(
                title = f"{name}'s Stats",
                description = f"{desc}",
                colour=discord.Colour.dark_gold()
            )
                
            embed.set_thumbnail(url=f'https://crafatar.com/renders/body/{uuid}')
            embed.timestamp = datetime.utcnow()
            print("Test 11 Passed")
            await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Stats(client)) 