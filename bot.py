import discord
from discord.ext import commands
from discord.ext import tasks
import logging
import platform
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import pymongo
from pymongo import MongoClient
import urllib.parse
import os
from pathlib import Path
from utils.db import collection, levelxp, levelroleDb, giveawayDB

cwd = Path(__file__).parents[0]
cwd = str(cwd)



owner_id = 822255174608224256
version = '0.0.1'
TOKEN = os.environ['token']



intents = discord.Intents.default()
intents.members = True





##logger = logging.getLogger('discord')
##logger.setLevel(logging.DEBUG)
##handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
##handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
##logger.addHandler(handler)





## SOME INITIALIZATIONS

async def get_prefix(client, message):
    if message.guild == None:
        return '+'
    myquery = { "gid": message.guild.id}

    if (collection.count_documents(myquery) == 0):
        await create_gdb(message.guild)
        prefix = '+'
    else:
        query = {"gid": message.guild.id}
        user = collection.find(query)
        for result in user:
            prefix = result["prefix"]
    p = prefix
    if not prefix.islower():
        p = prefix.lower()
    elif not prefix.isupper():
        p = prefix.upper()

    
    if p != prefix:
        return [p,prefix]
    return prefix


async def create_gdb(guild):
    
    myquery = { "gid": guild.id}
    if (collection.count_documents(myquery) != 0):
        return
    welcome = '{mention}, welcome to our server **{server}**. You are {number} member of our server. Please enjoy your stay.'
    post = {"gid": guild.id, "prefix": '+',  "shoobPing": False, "shoobLogs": None, "shoobTimer": False, "shoobPT1": None, "shoobPT2": None, "shoobPT3": None,  "shoobPT4": None, "shoobPT5": None, "shoobPT6": None, "mutedChannels": None, "mutedRoles": None, "achannel": '',"mchannel": '',"bchannel": '', "rT": '', "rT1": '', "rT2": '', "rT3": '', "rT4": '', "rT5": '', "rT6": '', "cT": '', "cT1": '', "cT2": '', "cT3": '', "cT4": '', "cT5": '', "cT6": '', "ti": '', "ti1": '', "ti2": '', "ti3": '', "ti4": '', "ti5": '', "ti6": '', "achannel": '', "mchannel": '', "bchannel": '' , "welcomeMessage": welcome, "welcomeChannel": None, "welcomeRole": None, "gafk": False,"welcomeImg":None}                                                     
    collection.insert_one(post)
    print('Guild data of {}-{} is added.'.format(guild.name,guild.id))


    
## DECLEAR CLIENT
client = commands.Bot(command_prefix=get_prefix, owner_id= owner_id,case_insensitive=True,intents = intents)
client.version = version
client.config_token = TOKEN
client.remove_command('help')
client.counts = dict()

## CONNECTION RELATED
@client.event
async def on_connect():
    print('Bot connected')

@client.event
async def on_disconnect():
    print('Bot disconnected')

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))



## GUILD JOIN AND LEAVE

    
@client.event
async def on_guild_join(guild):
    await create_gdb(guild)
    try:
        main = client.get_guild(769269340779839488)
        channel = main.get_channel(769740636584148992)
        await channel.send('Joined Guild: {} - {} members'.format(guild.name,guild.member_count))
    except Exception as e:
        print(e)
    print('Joined guild {}-{} is added.'.format(guild.name,guild.id))

@client.event
async def on_guild_remove(guild):
    try:
        main = client.get_guild(769269340779839488)
        channel = main.get_channel(769740636584148992)
        await channel.send('Left Guild: {} - {} members ;-;'.format(guild.name,guild.member_count))
    except Exception as e:
        print(e)
    print('Left guild {}-{} is added.'.format(guild.name,guild.id))

    

##ON MESSAGE - JUST FOR CHECK
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.author.bot == True:
        return

    bot_mention = '<@'+str(client.user.id)+'>'
    bot_mention2 = '<@!'+str(client.user.id)+'>'


    if bot_mention == message.content or bot_mention2 == message.content:
        #print('mentioned')
        prefix = '+'
        query = {"gid": message.guild.id}
        user = collection.find(query)
        for result in user:
            prefix = result["prefix"]
        await message.channel.send('Prefix of this server is: `{}` .'.format(prefix))
        #print('sent prefix')

    await client.process_commands(message)






if __name__ == '__main__':
    # When running this file, if it is the 'main' file
    # I.E its not being imported from another python file run this
    for file in os.listdir(cwd+"/cogs"):
        if file.endswith(".py") and not file.startswith("_"):
            client.load_extension(f"cogs.{file[:-3]}")
    client.run(client.config_token)
