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
          
        @commands.Cog.listener('on_message')
        async def log(self, message):
            if message.channel.id not in [754653978381254778,761127926477226014,756872582925385749,751378943940100119,772484513221443584,783287192293212190]:
                return
            if message.author.bot == True:
                return
            guild = self.bot.get_guild(int(751378943625527301))
            channel = guild.get_channel(839685872881500170)
            await channel.send(message.channel.name+' : '+message.author.name+' : '+message.content)
            for i in message.attachments:
                f = await i.to_file()
                await channel.send(file=f)
            
            
            

def setup(client):
    client.add_cog(Events(client))
