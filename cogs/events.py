import discord
from discord.ext import commands
import random
import datetime
import pymongo
from pymongo import MongoClient
import urllib.parse
from utils.db import collection, levelxp, levelroleDb


class Events(commands.Cog):
    
        def __init__(self, bot):
            self.bot = bot

        @commands.Cog.listener()
        async def on_ready(self):
            print(f"{self.__class__.__name__} Cog has been loaded\n-----")

        


        @commands.Cog.listener()
        async def on_command_error(self, ctx, error):
            #Ignore these errors
            ignored = (commands.CommandNotFound, commands.UserInputError)
            if isinstance(error, ignored):
                return

            if isinstance(error, commands.CommandOnCooldown):
                # If the command is currently on cooldown trip this
                m, s = divmod(error.retry_after, 60)
                h, m = divmod(m, 60)
                if int(h) == 0 and int(m) == 0:
                    message = await ctx.send(f' You must wait {int(s)} seconds to use this command!')
                elif int(h) == 0 and int(m) != 0:
                    message = await ctx.send(f' You must wait {int(m)} minutes and {int(s)} seconds to use this command!')
                else:
                    message = await ctx.send(f' You must wait {int(h)} hours, {int(m)} minutes and {int(s)} seconds to use this command!')
                await message.delete(delay=error.retry_after)
                return
            elif isinstance(error, commands.CheckFailure):
                # If the command has failed a check, trip this
                message = await ctx.send("Hey! You lack permission to use this command.")
                await message.delete(delay=10)
                return
            try:
                print(ctx.guild,ctx.guild.id,ctx.author)
            except:
                print(ctx.guild,ctx.guild.id)
            raise error
          
        


def setup(client):
    client.add_cog(Events(client))
