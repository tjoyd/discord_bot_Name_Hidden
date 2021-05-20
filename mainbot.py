import discord
from discord.ext import commands
from discord.ext import tasks
import time
import os
import pymongo
from pymongo import MongoClient
import urllib.parse
import random
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import asyncio
import asyncpg
import aiohttp
from discord import File as dFile
from asyncio import sleep as asyncsleep
import datetime

try:
    mango_url = "mongodb+srv://" + os.environ['user'] + ":" + urllib.parse.quote_plus(os.environ['password']) + os.environ['cluster']
    cluster = MongoClient(mango_url)
    db = cluster[os.environ['database']]
    collection = db[os.environ['collec']]
    banlist = db['Bans']
    levelxp = db['levelxp']
    print('Data Loaded')
except Exception as e:
    print(e)
    print("Data can't be Loaded")
    

           
        
    
intents = discord.Intents.default()
intents.members = True
print('Intent Value:',intents.value)


async def create_db(guild):
    
    myquery = { "gid": guild.id}
    if (collection.count_documents(myquery) != 0):
        return
    welcome = '{mention}, welcome to our {server}. You are {number} member. Please enjoy your stay.'
    post = {"gid": guild.id, "prefix": '+',  "shoobPing": False, "shoobLogs": None, "shoobTimer": False, "shoobPT1": None, "shoobPT2": None, "shoobPT3": None,  "shoobPT4": None, "shoobPT5": None, "shoobPT6": None, "mutedChannels": None, "mutedRoles": None, "achannel": '',"mchannel": '',"bchannel": '', "rT": '', "rT1": '', "rT2": '', "rT3": '', "rT4": '', "rT5": '', "rT6": '', "cT": '', "cT1": '', "cT2": '', "cT3": '', "cT4": '', "cT5": '', "cT6": '', "ti": '', "ti1": '', "ti2": '', "ti3": '', "ti4": '', "ti5": '', "ti6": '', "achannel": '', "mchannel": '', "bchannel": '' , "welcomeMessage": welcome, "welcomeChannel": None, "welcomeRole": None, "gafk": False}                                                     
    collection.insert_one(post)
    print('Guild data of {}-{} is added.'.format(guild.name,guild.id))
    
async def banUser(user,reason):
    print('here')
    post = {"uid": user.id, "name": user.name, "reason": reason}
    banlist.insert_one(post)
    print('{}[{}] is banned for {}'.format(user.name,user.id,reason))
    
    
async def get_prefix(client, message):
    myquery = { "gid": message.guild.id}

    if (collection.count_documents(myquery) == 0):
        await create_db(message.guild)
        prefix = '+'
    else:
        query = {"gid": message.guild.id}
        user = collection.find(query)
        for result in user:
            prefix = result["prefix"]
    return prefix

async def check_ban(userid):
    myquery = { "uid": userid}

    if (banlist.count_documents(myquery) == 0):
        return False
    else:
        return True

client = commands.Bot(command_prefix=get_prefix,case_insensitive=True,intents = intents)
client.remove_command('help')



removeRole = None

async def perm_admin(ctx):
    value = ctx.author.guild_permissions.administrator
    if not value:
        await ctx.send("{}, you don't have permission.".format(ctx.author.mention))
        return False
    return True


    
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))



@client.event
async def on_guild_join(guild):
    await create_db(guild)
    try:
        main = client.get_guild(769269340779839488)
        #print(main)
        channel = main.get_channel(769740636584148992)
        await channel.send('Joined Guild: {}'.format(guild.name))
    except Exception as e:
        print(e)
    print('Joined guild {}-{} is added.'.format(guild.name,guild.id))
    
   

@client.event
async def on_guild_remove(guild):
    try:
        main = client.get_guild(769269340779839488)
        #print(main)
        channel = main.get_channel(769740636584148992)
        await channel.send('Left Guild: {} ;-;'.format(guild.name))
    except Exception as e:
        print(e)
    print('Left guild {}-{} is added.'.format(guild.name,guild.id))



@client.event
async def on_member_join(member):
    print(member)
    if member.bot == True:
        return
    print('nani')
    await update_user(member.guild,member)
    print('Here')
    if member.bot == True:
        return
    
    
    
    query = { "gid": member.guild.id}
    guilds = collection.find(query)
    for result in guilds:
        if result['welcomeRole'] != None:
            role = member.guild.get_role(int(result['welcomeRole']))
            try:
                await member.add_roles(role)
                print('autorole {} added for {}'.format(role,member))
            except Exception as e:
                print('Mission permission on autorole ',e)
                
        if result['welcomeChannel'] == None:
            print('No welcome')
            return
        cid = result['welcomeChannel']
        print('Here2')
        var = False
        text = ''
        string = ''
        for i in result['welcomeMessage']:
            if i == '{':
                var = True
                continue
            elif i == '}':
                string = string.lower()
                
                if string == 'user':
                    text += str(member)
                elif string == 'name':
                    text += str(member.name)
                elif string == 'mention':
                    text += str(member.mention)
                elif string == 'server':
                    text += str(member.guild.name)
                elif string == 'number':
                    num = member.guild.member_count
                    text += str(num)
                    if num == 11:
                        text += 'th'
                    elif num == 12:
                        text += 'th'
                    elif num == 13:
                        text += 'th'
                    else:                       
                        num = num % 10
                        if num == 1:
                            text += 'st'
                        elif num == 2:
                            text += 'nd'
                        elif num == 3:
                            text += 'rd'
                        else:
                            text += 'th'
                print(string)
                string = ''
                var = False
                continue
            if var == True:
                string += i
            else:
                text += i
        print('here 3')
    channel = member.guild.get_channel(cid)
    await channel.send(text)
    print('final')
    
            
@client.command()
async def welcome(ctx):
    if True:
        return
    member = ctx.author
    if member.bot == True:
        return
    
    #await update_user(member.guild,member)
    
    query = { "gid": ctx.guild.id}
    guilds = collection.find(query)
    for result in guilds:
        if result['welcomeMessage'] == None:
            print('No welcome')
            return
        var = False
        text = ''
        string = ''
        for i in result['welcomeMessage']:
            if i == '{':
                var = True
                continue
            elif i == '}':
                string = string.lower()
                
                if string == 'user':
                    text += str(member)
                elif string == 'name':
                    text += str(member.name)
                elif string == 'mention':
                    text += str(member.mention)
                elif string == 'server':
                    text += str(member.guild.name)
                elif string == 'number':
                    num = member.guild.member_count
                    text += str(num)
                    if num == 11:
                        text += 'th'
                    elif num == 12:
                        text += 'th'
                    elif num == 13:
                        text += 'th'
                    else:                       
                        num = num % 10
                        if num == 1:
                            text += 'st'
                        elif num == 2:
                            text += 'nd'
                        elif num == 3:
                            text += 'rd'
                        else:
                            text += 'th'
                print(string)
                string = ''
                var = False
                continue
            if var == True:
                string += i
            else:
                text += i
    await ctx.send(text)


@client.event
async def on_message(message):
    if message.author == client.user:
        return
        
    #print(message.content)
    
    guild = message.guild
    if guild == None:
        print('{}: {}'.format(message.author,message.content))
        return
    
    myquery = { "gid": message.guild.id}
    if (collection.count_documents(myquery) == 0):
        await create_db(message.guild)
        
        
    
    await client.process_commands(message)



    
@client.command(aliases=['p'])
async def ping(ctx):
    if await check_ban(ctx.author.id):
        print('By ban user')
        return
    
    print('-Ping is called,{} in {} by {}'.format(round(client.latency*1000),ctx.guild.name,ctx.author.name))
    await ctx.send('pong! {}ms'.format(round(client.latency*1000)))

@client.command()
async def smug(ctx):
    if True:
        return
    if await check_ban(ctx.author.id):
        print('By ban user')
        return
    
    print('-Smug is called in {}-{} by {}'.format(ctx.guild.name,ctx.guild.id,ctx.author.name))
    data = ['https://tenor.com/UVTP.gif','https://tenor.com/view/satania-anime-smile-evil-smile-gif-10120660','https://tenor.com/view/smirk-anime-anime-smug-anime-smirk-smug-gif-18707538']
    
    await ctx.send("{} smugs > \n{}".format(ctx.author.name,random.choice(data)))

@client.command()
async def f(ctx, * args):
    if await check_ban(ctx.author.id):
        print('By ban user')
        return
    
    print('-F is called in {}-{} by {}'.format(ctx.guild.name,ctx.guild.id,ctx.author.name))
    if len(args) == 0:
        text = str(ctx.author.name)+' paid their respects.'
    else:
        text = str(ctx.author.name)+' paid their respects for '+' '.join(args)
    embed = discord.Embed(
        colour = discord.Colour.magenta(),
        description = text
    )

    

    await ctx.send(embed = embed)
    
   


@client.command()
async def greet(ctx, user:discord.User=None):
    if await check_ban(ctx.author.id):
        print('By ban user')
        return
    
    print('-Greet is called in {}-{}: {}: {}: {}'.format(ctx.guild.name,ctx.guild.id,ctx.channel,ctx.author.name,user))
    if user == None:
        await ctx.send("Hello I'm Kaori, Elaina's little sister.\nNice to meet you all.")
    else:
        await ctx.send("{}, hello I'm Kaori, Elaina's little sister. Nice to meet you.".format(user.name))

        
  
@greet.error
async def greet_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send('Either mention a user or their id')
    else:
        print(error,type(error))
    
    
    
@client.command(aliases=['s'])
async def say(ctx, *args):
    if True:
        return
    if await check_ban(ctx.author.id):
        print('By ban user')
        return
    
    print('-Say is called in {}-{}: {}: {}: {}'.format(ctx.guild.name,ctx.guild.id,ctx.channel,ctx.author.name,''.join(args)))
    try:
        if len(args) == 0:
            return
    except Exception as e:
        print(e)
        
    for arg in args:
        if '<@' in arg:
            await ctx.send('Hello!')
            return
    await ctx.send('{}'.format(' '.join(args)))

@client.command()
async def sayd(ctx, *args):
    if True:
        return
    if await check_ban(ctx.author.id):
        print('By ban user')
        return
    
    print('-Sayd is called in {}-{}: {}: {}: {}'.format(ctx.guild.name,ctx.guild.id,ctx.channel,ctx.author.name,''.join(args)))
    
    try:
        if len(args) == 0:
            return
    except Exception as e:
        print(e)
        
    try:
        await ctx.message.delete(delay=None)
    except Exception as e:
        print(e)
    for arg in args:
        if '<@' in arg:
            await ctx.send('Hello!')
            return
    
    await ctx.send('{}'.format(' '.join(args)))

@client.command(aliases=['ss'])
async def setshoob(ctx,arg1:discord.Role=None,arg2=None):
    if await check_ban(ctx.author.id):
        print('By ban user')
        return
    
    if ctx.author.bot == True:
        return
    
    guild = ctx.guild
    if guild == None:
        return
    
    print('-Set Shoob is called in {}-{}: {}: {}:'.format(ctx.guild.name,ctx.guild.id,ctx.channel,ctx.author.name))
    
    if not await perm_admin(ctx):
        return

    role = arg1
    
    query = {"gid": ctx.guild.id}
    guilds = collection.find(query)
    for result in guilds:
        shoobPing = result["shoobPing"]
 
    if arg1 == None:
        text = 'This is not the correct format.\nFormat: `setshoob <role> <tier_number>`'
        await ctx.send(text)
        return
    elif arg2 == None:
        try:
            dis = int(arg1)
            if dis == 0:
                if shoobPing:
                    text = 'Shoob Ping is disabled'
                else:
                    text = 'Shoob Ping is already disabled'
                await ctx.send(text)
                collection.update_one({"gid":ctx.guild.id}, {"$set":{"shoobPing": False, "shoobPT1": None, "shoobPT2": None, "shoobPT3": None,  "shoobPT4": None, "shoobPT5": None, "shoobPT6": None,}})
                print('Shoob ping is disabled in {}-{}.'.format(ctx.guild.name,ctx.guild.id))
                return
        except Exception as e:
            print(e)
            print('Error during disabling Shoob Ping in {}'.format(ctx.guild.name))
        text = 'This is not the correct format.\nFormat: `setshoob <role> <tier_number>'
        await ctx.send(text)
        return
    try:
        tier = int(arg2)
        if tier < 1 or tier > 6:
            print('Not in range 0>tier>7 in {}'.format(ctx.guild.name))
            await ctx.send('Not a valid number for tier, [ 0>tier>7 ].')
            return
    except Exception as e:
        print(e,type(e))
        await ctx.send('Not a valid number for tier')
        return
    key = 'shoobPT'+str(tier)
    collection.update_one({"gid":ctx.guild.id}, {"$set":{"shoobPing": True, key : role.id}})
    print('SS of Guild {}-{} is updated. {}-{}-{}'.format(ctx.guild.name,ctx.guild.id, True, role.id, tier))
    
    text = "{} role is set as Shoob ping for tier {} ".format(role.mention,tier)
    embed = discord.Embed(
        colour = discord.Colour.magenta(),
        description = text
    )
    await ctx.send(embed = embed)

@client.command(aliases=['csp'])
async def checkping(ctx):
    if await check_ban(ctx.author.id):
        print('By ban user')
        return
    
    if ctx.author.bot == True:
        return
    
    guild = ctx.guild
    if guild == None:
        return

    query = {"gid": ctx.guild.id}
    guilds = collection.find(query)
    for result in guilds:
        shoobPing = result["shoobPing"]
        text = 'Shoob Pings in '+ctx.guild.name+'\n\n'
        if shoobPing:
            if result["shoobPT1"] !=None:
                rid = int(result["shoobPT1"])
                role = ctx.guild.get_role(rid)
                #print('here',role,rid)
                if role != None:
                    text += str(role.mention)+ ' is set for Tier 1\n'
            else:
                print('here',result["shoobPT1"])
            if result["shoobPT2"] !=None:
                rid = int(result["shoobPT2"])
                role = ctx.guild.get_role(rid)
                if role != None:
                    text += str(role.mention)+ ' is set for Tier 2\n'

            if result["shoobPT3"] !=None:
                rid = int(result["shoobPT3"])
                role = ctx.guild.get_role(rid)
                if role != None:
                    text += str(role.mention)+ ' is set for Tier 3\n'

            if result["shoobPT4"] !=None:
                rid = int(result["shoobPT4"])
                role = ctx.guild.get_role(rid)
                if role != None:
                    text += str(role.mention)+ ' is set for Tier 4\n'
            if result["shoobPT5"] !=None:
                rid = int(result["shoobPT5"])
                role = ctx.guild.get_role(rid)
                if role != None:
                    text += str(role.mention)+ ' is set for Tier 5\n'

            if result["shoobPT6"] !=None:
                rid = int(result["shoobPT6"])
                role = ctx.guild.get_role(rid)
                if role != None:
                    text += str(role.mention)+ ' is set for Tier 6\n'
            embed = discord.Embed(
                colour = discord.Colour.magenta(),
                description = text
            )
            await ctx.send(embed = embed)
        else:
            print('No ping')

@setshoob.error
async def setshoob_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send('This is not the correct format.\nFormat: `setshoob <role> <tier_number>`')
    else:
        print(error,type(error))

        
@client.command(aliases=['cp'])
async def changeprefix(ctx,prefix):
    if await check_ban(ctx.author.id):
        print('By ban user')
        return
    
    print('Change Prefix called in {} by {}'.format(ctx.guild.name,ctx.author.name))

    if ctx.author.bot == True:
        return
    
    await ctx.send('This feature is currently disabled. Contact Support.')
    guild = ctx.guild
    if guild == None:
        return
    
    if not await perm_admin(ctx):
        return
    
    collection.update_one({"gid":ctx.guild.id}, {"$set":{"prefix": prefix}})
    await ctx.send('New server prefix is {}'.format(prefix))

    
@client.command(aliases=['st'])
async def shoobtimer(ctx):
    if await check_ban(ctx.author.id):
        print('By ban user')
        return
    if ctx.author.bot == True:
        return   
    guild = ctx.guild
    if guild == None:
        return
    
    print('Shoob Timer called in {} by {}'.format(ctx.guild.name,ctx.author.name))
    if not await perm_admin(ctx):
        return
    
    query = {"gid": ctx.guild.id}
    guilds = collection.find(query)
    for result in guilds:
        shoobTimer = result["shoobTimer"]
        if shoobTimer:
            shoobTimer = False
            collection.update_one({"gid":ctx.guild.id}, {"$set":{"shoobTimer": shoobTimer}})
            await ctx.send('Shoob Timer in this server is deactivated')
        else:
            shoobTimer = True
            collection.update_one({"gid":ctx.guild.id}, {"$set":{"shoobTimer": shoobTimer}})
            await ctx.send('Shoob Timer in this server is activated')
        print('Shoob Timer in {} is changed to {}'.format(ctx.guild,shoobTimer))
  


@client.command(aliases=['sl'])
async def shooblogs(ctx,channel:discord.TextChannel=None):
    if await check_ban(ctx.author.id):
        print('By ban user')
        return
    if ctx.author.bot == True:
        return   
    guild = ctx.guild
    if guild == None:
        return
    
    print('Shoob Logs called in {} by {}'.format(ctx.guild.name,ctx.author.name))
    if not await perm_admin(ctx):
        return
    
    if channel == None:
        collection.update_one({"gid":ctx.guild.id}, {"$set":{"shoobLogs": ctx.channel.id}})
        await ctx.send('This channel is set for Shoob Logs')
    else:
        collection.update_one({"gid":ctx.guild.id}, {"$set":{"shoobLogs": channel.id}})
        await ctx.send('{} is set for Shoob Logs'.format(channel))
    
@shooblogs.error
async def shooblogs_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send('This is not the correct format.\nFormat: `shooblogs <channel>`')
    else:
        print(error,type(error))           
    


    
   
@client.listen('on_message')
async def afk_check(message):
    if await check_ban(message.author.id):
        return
    if message.author.bot == True:
        return
    guild = message.guild
    if guild == None:
        return
    gid = message.guild.id
    query = {"gid": gid}
    guilds = collection.find(query)
    for result in guilds:
        if result['gafk'] == True:
            #print('Here')
            mention = message.mentions
            if mention == None:
                return
            #print(mention)
            query = {"gid": message.guild.id}
            users = levelxp.find(query)
            for user in users:
                if user['afk'] == True:
                    if user['uid'] == message.author.id:
                            #print('afk user back')
                            await message.channel.send('{} welcome back, I set your afk to false'.format(message.author.name))
                            levelxp.update_one({"gid":gid, "uid":user['uid']}, {"$set":{"afk": False, "reason": ''}})
                            return
                mem = message.guild.get_member(user['uid'])
                if mem in mention:
                    #print('lol')
                    if user['afk'] == True:
                        await message.channel.send('{}, {} is afk.\nReason: {}.'.format(message.author.mention, mem.name, user['reason']))
                        #print('user afk')
                        
                    
                    
    
   
@client.command()
async def afk(ctx,*reasons):
    if await check_ban(ctx.author.id):
        print('By ban user')
        return
    if ctx.author.bot == True:
        return   
    guild = ctx.guild
    if guild == None:
        return
    try:
        reason = reasons[0]
        reason = ''
        for i in reasons:
            reason +=i
            reason += ' '
    except Exception as e:
        reason = None
    query = {"gid": ctx.guild.id}
    guilds = collection.find(query)
    for result in guilds:
        if result['gafk'] == True:
            gid = ctx.guild.id
            uid = ctx.author.id
            if reason == None:
                await ctx.send(" command is `afk <reason>`. You must mention a reason")
                return
            await ctx.send("{}, your afk is set for {}".format(ctx.author.mention,reason)) 
            await asyncsleep(2)
            levelxp.update_one({"gid":gid, "uid":uid}, {"$set":{"afk": True, "reason": reason}})
            
        else:
            await ctx.send('Afk is off for this server, ask an admin to use `gafk` to turn on Server Afk')
            
    
    


@client.command()
async def support(ctx):
    if await check_ban(ctx.author.id):
        print('By ban user')
        return
    if ctx.author.bot == True:
        return   
    guild = ctx.guild
    if guild == None:
        return
    await ctx.send('Join our support server at: https://discord.gg/vq32pgv')

    
    
    
@client.command()
async def setWelcome(ctx,*args):
    if await check_ban(ctx.author.id):
        print('By ban user')
        return
    if ctx.author.bot == True:
        return   
    guild = ctx.guild
    if guild == None:
        return
    
    print('Set welcome called in {} by {}'.format(ctx.guild.name,ctx.author.name))
    if not await perm_admin(ctx):
        return
    try:
        arg1 = args[0]
    except Exception as e:
        text = "Usage of `setwelcome`:\n\n`setwelcome channel <channel>` to set welcoming channel.\n`setwelcome message <message>` to set welcome message.\n Message variables are {user}, {name}, {mention}, {server}, {number}.\n Example: `+setwelcome message {mention}, welcome to our {server}. You are the {number} member of our server. Please read #rules.`"
        text += "\n`setwelcome disable` to disable welcome messages."
        await ctx.send(text)
        return
    
    arg2 = ''
    for i in range(1,len(args)):
        arg2 += str(args[i])+' '
        
    print(arg1,arg2)
    
    if arg1.lower() == 'channel':
        arg2 = arg2.strip()
        cid = int(arg2[2:len(arg2)-1])
        channel = ctx.guild.get_channel(cid)
        if channel == None:
            await ctx.send('send valid channel')
            return
        await channel.send('Welcome messages will be sent here')
        collection.update_one({"gid":ctx.guild.id}, {"$set":{"welcomeChannel": cid}})
        
    elif arg1.lower() == 'message':
        var = False
        text = ''
        string = ''
        for i in arg2:
            if i == '{':
                var = True
                continue
            elif i == '}':
                string = string.lower()
                
                if string == 'user':
                    text += '{'+string+'}'
                elif string == 'name':
                    text += '{'+string+'}'
                elif string == 'mention':
                    text += '{'+string+'}'
                elif string == 'server':
                    text += '{'+string+'}'
                elif string == 'number':
                    text += '{'+string+'}'
                else:
                    value = '{'+string+'} is not a valid variable.'
                    await ctx.send(value)
                    return
                string = ''
                var = False
                continue
            if var == True:
                string += i
            else:
                text += i
        collection.update_one({"gid":ctx.guild.id}, {"$set":{"welcomeMessage": text}})
        await ctx.send('welcome message updated')
        
    elif arg1.lower() == 'disable':
        text = '{mention}, welcome to our {server}. You are {number} member. Please enjoy your stay.'
        collection.update_one({"gid":ctx.guild.id}, {"$set":{"welcomeChannel": None, "welcomeMessage": text}})
        await ctx.send('welcome messages are disabled.')
        
    elif arg1.lower() == 'preview':
        member = ctx.author
        if member.bot == True:
            return

        #await update_user(member.guild,member)

        query = { "gid": ctx.guild.id}
        guilds = collection.find(query)
        for result in guilds:
            if result['welcomeMessage'] == None:
                print('No welcome')
                return
            var = False
            text = ''
            string = ''
            for i in result['welcomeMessage']:
                if i == '{':
                    var = True
                    continue
                elif i == '}':
                    string = string.lower()

                    if string == 'user':
                        text += str(member)
                    elif string == 'name':
                        text += str(member.name)
                    elif string == 'mention':
                        text += str(member.mention)
                    elif string == 'server':
                        text += str(member.guild.name)
                    elif string == 'number':
                        num = member.guild.member_count
                        text += str(num)
                        num = num % 10
                        if num == 1:
                            text += 'st'
                        elif num == 2:
                            text += 'nd'
                        elif num == 3:
                            text += 'rd'
                        else:
                            text += 'th'
                    print(string)
                    string = ''
                    var = False
                    continue
                if var == True:
                    string += i
                else:
                    text += i
        await ctx.send(text)
        
        
        
    
@client.command()
async def setStats(ctx):
    if await check_ban(ctx.author.id):
        print('By ban user')
        return
    if ctx.author.bot == True:
        return   
    guild = ctx.guild
    if guild == None:
        return
    
    print('Setup for Server Stats called in {} by {}'.format(ctx.guild.name,ctx.author.name))
    if not await perm_admin(ctx):
        return
    m = await ctx.send('Please react with 👍 for confirmation')
    await m.add_reaction('👍')
    
    def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) == '👍'

    try:
        reaction, user = await client.wait_for('reaction_add', timeout=20.0, check=check)
    except asyncio.TimeoutError:
        await ctx.send('Time Out.')
        return
    
        
    acount = 0
    bcount = 0
    mcount = 0
    for member in guild.members:
        if member.bot == True:
            bcount += 1
        else:
            mcount += 1
        acount += 1
    overwritee = discord.PermissionOverwrite()
    overwrite = discord.PermissionOverwrite()
    
    category = await ctx.guild.create_category('📊 Server Stats 📊',position=0)
    
    overwritee.connect = False
    overwritee.manage_channels = False
    overwritee.send_messages = False
    overwrite.manage_channels = True
    overwrite.connect = True
    overwrite.send_messages = True

    await category.set_permissions(guild.default_role, overwrite=overwritee)
    await category.set_permissions(client.user, overwrite=overwrite)
    
    
    name = 'All Members: '+str(acount)
    channel = await guild.create_voice_channel(name, category=category)
    await channel.set_permissions(guild.default_role, overwrite=overwritee)
    await channel.set_permissions(client.user, overwrite=overwrite)
    cid1 = channel.id
    
    name = 'Members: '+str(mcount)
    channel = await guild.create_voice_channel(name, category=category)
    await channel.set_permissions(guild.default_role, overwrite=overwritee)
    await channel.set_permissions(client.user, overwrite=overwrite)
    cid2 = channel.id
    
    name = 'Bots: '+str(bcount)
    channel = await guild.create_voice_channel(name, category=category)
    await channel.set_permissions(guild.default_role, overwrite=overwritee)
    await channel.set_permissions(client.user, overwrite=overwrite)
    cid3 = channel.id
    
    collection.update_one({"gid":ctx.guild.id}, {"$set":{"achannel": cid1, "mchannel": cid2, "bchannel": cid3}})
    
    await ctx.send('Server stats has been created.')
    print('Channels created')
    
    
    
    
@tasks.loop(seconds=60.0)
async def update_stats():
    query = {}
    guilds = collection.find(query)
    for result in guilds:
        gid = result['gid']
        cid1 = result['achannel']
        cid2 = result['mchannel']
        cid3 = result['bchannel']
        
        try:
            guild = client.get_guild(gid)
        except:
            print('Guild not found')
            return
        if guild == None:
            print('Guild not found')
            return
        acount = 0
        bcount = 0
        mcount = 0
        for member in guild.members:
            if member.bot == True:
                bcount += 1
            else:
                mcount += 1
            acount += 1
        
        if len(str(cid1)) > 2:
            try:
                achannel = guild.get_channel(cid1)
                name = 'All Members: '+str(acount)
                await achannel.edit(name=name)
            except Exception as e:
                pass
                #print('{}, All channel not found in {}'.format(e,guild.name))
        if len(str(cid2)) > 2:
            try:
                mchannel = guild.get_channel(cid2)
                name = 'Members: '+str(mcount)
                await mchannel.edit(name=name)
            except Exception as e:
                pass
                #print('{}, Member channel not found in {}'.format(e,guild.name))
        
        if len(str(cid3)) > 2:
            try:
                bchannel = guild.get_channel(cid3)  
                name = 'Bots: '+str(bcount)
                await bchannel.edit(name=name)
            except Exception as e:
                pass
                #print('{}, Bot channel not found in {}'.format(e,guild.name))

        
        
        #print('Member stats updated for {}'.format(guild.name))
            
update_stats.start()    



@client.command()
async def autorole(ctx,role:discord.Role=None):
    if await check_ban(ctx.author.id):
        print('By ban user')
        return
    if ctx.author.bot == True:
        return   
    guild = ctx.guild
    if guild == None:
        return
    
    print('Setup for Server Stats called in {} by {}'.format(ctx.guild.name,ctx.author.name))
    if not await perm_admin(ctx):
        return
    
    if role == None:
        collection.update_one({"gid":ctx.guild.id}, {"$set":{"welcomeRole": None}})
        await ctx.send('Autorole is disabled.'.format(role))
        return
    
    collection.update_one({"gid":ctx.guild.id}, {"$set":{"welcomeRole": role.id}})
    await ctx.send('{} is set for autorole'.format(role))
        
    
    
    
 
@autorole.error
async def autorole_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send('please set a valid role')
    else:
        print(error,type(error))
    
  

@client.command()
async def gafk(ctx):
    if await check_ban(ctx.author.id):
        print('By ban user')
        return
    if ctx.author.bot == True:
        return   
    guild = ctx.guild
    if guild == None:
        return
    
    print('Setup for Server Stats called in {} by {}'.format(ctx.guild.name,ctx.author.name))
    if not await perm_admin(ctx):
        return
    
    query = {"gid": ctx.guild.id}
    guilds = collection.find(query)
    for result in guilds:
        gafk = result['gafk']
        if gafk == True:
            collection.update_one({"gid":ctx.guild.id}, {"$set":{"gafk": False}})
            await ctx.send('Server afk is deactivated')
        else:
            collection.update_one({"gid":ctx.guild.id}, {"$set":{"gafk": True}})
            await ctx.send('Server afk is activated')
    

@client.command(aliases=['h'])
async def help(ctx):
    if await check_ban(ctx.author.id):
        print('By ban user')
        return

    if ctx.author.bot == True:
        return
    
    guild = ctx.guild
    if guild == None:
        return

    
    query = {"gid": ctx.guild.id}
    guilds = collection.find(query)
    for result in guilds:
        prefix = result["prefix"]

        
    embed = discord.Embed(
        colour = discord.Colour.magenta()
    )

    embed.set_author(name="Kaori Help")
    
    text = str(prefix)+'ping'
    embed.add_field(name=text, value = 'Returns Pong!', inline = False)
    
    text = str(prefix)+'changeprefix <prefix>'
    embed.add_field(name=text, value = 'Changes the server prefix', inline = False)

    text = str(prefix)+'say <message>'
    embed.add_field(name=text, value = 'Will reply with same <message>', inline = False)

    text = str(prefix)+'setshoob <@role> <tier_number>'
    embed.add_field(name=text, value = 'Will ping <@role> for <tier_number> or high tier spawn of Shoob bot.', inline = False)


    await ctx.send(embed = embed)

    
    
@client.command()
async def banBot(ctx,*args):
    if ctx.author.id != 329230819975495681:
        return
    if len(args) == 0:
        await ctx.send("Need user id")
    elif len(args) == 1:
        try:
            uid = int(args[0])
            reason = None
        except:
            await ctx.send('User id is needed')
            return
    elif len(args) == 2:
        try:
            uid = int(args[0])
        except:
            await ctx.send('User id is needed')
            return
        reason = args[1]
    
    myquery = { "uid": uid}

    if (banlist.count_documents(myquery) == 0):
        user = await client.fetch_user(uid)
        print('Ban request send')
        await banUser(user,reason)
        await ctx.send('{} is banned permanently.'.format(user.name)) 
    else:
        await ctx.send('User already banned') 


@client.command()
async def invite(ctx,*args):
    if await check_ban(ctx.author.id):
        print('By ban user')
        return

    if ctx.author.bot == True:
        return
    
    arg = 'Invite '+str(client.user.name)+' to your sevrer: [Invite Link](https://discord.com/api/oauth2/authorize?client_id=761702456169594880&permissions=269995088&scope=bot)'
    embed = discord.Embed(
        colour = discord.Colour.magenta(),
        description = arg
    )
    await ctx.send(embed = embed)

    
    
    
@client.command()
async def embed(ctx, *args):
    if ctx.author.id != 329230819975495681:
        return
    arg = ''
    for i in args:
        arg +=i
    arg += '\n'
    arg += '[Anime Soul](https://animesoul.com/)'
    embed = discord.Embed(
        colour = discord.Colour.magenta(),
        description = arg
    )

    embed.set_author(name="Kaori Embeds")
    await ctx.send(embed = embed)
    
    
@client.command()
async def updatedb(ctx):
    if ctx.author.id != 329230819975495681:
        return
    
    if False:
        query = {}
        users = levelxp.find(query)
        for result in users:
            gid = result['gid']
            uid = result['uid']
            try:
                c = result['psCards']
            except Exception as e:
                levelxp.update_one({"gid":gid, "uid":uid}, {"$set":{"psCards":0, "afk": False, "reason": ''}})
                print('{} updated'.format(uid))
        await ctx.send('Reason added.')
    
    if True:
        query = {}
        guilds = collection.find(query)   
        for result in guilds:
            gid = result['gid']
            
            #text = '{mention}, welcome to our {server}. You are {number} member. Please enjoy your stay.'
            collection.update_one({"gid":gid}, {"$set":{"rT": '', "cT": '', "ti": '' }})
        print('Recent db added')
        await ctx.send('Recent db added')
        
        
@client.listen('on_message')
async def shoobPing(message):
    if await check_ban(message.author.id):
        return

    guild = message.guild
    if guild == None:
        return

    
    #Read Anime Soul Embed Tier

        
    if message.author.id == 673362753489993749:
        query = {"gid": message.guild.id}
        guilds = collection.find(query)
        for result in guilds:
            shoobPing = result["shoobPing"]
            
        if shoobPing:
            embeds = message.embeds # return list of embeds
            
            try:
                data = embeds[0].to_dict()
                try:
                    title = data['title']
                    txt = title.split()
                    for i in txt:
                        #print(i)
                        if i == "claims":
                            print("Recent check")
                            return
                        elif i == "Click":
                            print("Vote check")
                            return
                        elif i == "Guides":
                            print("Recent check")
                            return
                        elif i == "Top":
                            print("Recommendation check")
                            return
                    tier = title[len(title)-1]
                    print('Spawn in {}-{} : {} : {}'.format(message.guild,message.guild.id,message.channel,tier))
                    text = 'shoobPT'+str(tier)
                    query = {"gid": message.guild.id}
                    guilds = collection.find(query)
                    for result in guilds:
                        rid = result[text]
                        if rid == None:
                            print('Shoob Ping not set for Tier: '+tier)
                            return
                        else:
                            rid = int(rid)
                    
                    role = message.guild.get_role(rid)
                    if role != None:
                        await message.channel.send('{}, Shoob has spawned {}'.format(role.mention,title))
                    else:
                        print('Shoob Ping not set for Tier: {}')
                except Exception as e:
                    print(e)
                    #print('Not a spawn card')
            except:
                pass
                #print('No embeds')
        else:
            print('Shoob ping is disabled in {}'.format(message.guild.name))


#Shoob Logs:
guildData = dict()
@client.listen('on_message')
async def shoobLog(message):
    if await check_ban(message.author.id):
        return

    guild = message.guild
    if guild == None:
        return

    
    #Read Anime Soul Embed Tier
        
    if message.author.id == 673362753489993749:
        global guildData
        jurl = message.jump_url
        query = {"gid": message.guild.id}
        guilds = collection.find(query)
        for result in guilds:
            shoobLogs = result["shoobLogs"]
            if True:
                if shoobLogs != None:
                    channel = message.guild.get_channel(int(shoobLogs))
                embeds = message.embeds
                try:
                    data = embeds[0].to_dict()
                    #print(data)
                    try:
                        #detects if card spawned of not
                        #print('check1')
                        title = data['title']
                        tit = title.split()
                        for i in tit:
                            #print(i)
                            if i == "claims":
                                print("Recent check")
                                return
                            elif i == "Click":
                                print("Vote check")
                                return
                            elif i == "Guides":
                                print("Recent check")
                                return
                            elif i == "Top":
                                print("Recommendation check")
                                return
                        try:
                            color = data['colour']
                        except:
                            color = data['color']
                        #print(color)
                        #print('---'+title)
                        #print('check2')
                        tier = tit[len(tit)-1]
                        gids = str(message.guild.id)+'S'
                        guildData[gids] = False
                        gidClaim = str(message.guild.id)+'Claim'
                        guildData[gidClaim] = 'None'
                        gidt = str(message.guild.id)+'T'
                        guildData[gidt] = tier
                        gidv = str(message.guild.id)+'V'
                        guildData[gidv] = None
                        #print(guildData[gidv])
                        #print(guildData)
                        if shoobLogs != None:
                            #print('check 3')
                            text = title+' is spawned.'
                            embed = discord.Embed(
                                colour =color,
                                description = text,
                                timestamp = datetime.datetime.now()
                            )
                            name = message.guild.name
                            embed.set_footer(text=name)

                            m = await channel.send(embed = embed)
                            gid = str(message.guild.id)
                            guildData[gid] = m
                            #print(guildData[gid])
                            
                            #print(guildData[gid])
                            gidc = gid+'C'
                            guildData[gidc] = color
                            
                            #print(guildData[gid])
                            #print(m.id)
                            await asyncsleep(25)
                            #print(guildData[gid])
                            #print('check4')
                            if guildData[gids] == False:
                                string = title+' is despawned'
                                embed = discord.Embed(
                                    colour = color,
                                    description = string,
                                    timestamp = datetime.datetime.now()
                                )
                                name = message.guild.name
                                embed.set_footer(text=name)
                                await m.edit(embed = embed)
                        else:
                            #print('waiting')
                            await asyncsleep(25)
                        s = 'rT'+str(tier)
                        rt = result[s]         #spawn card string
                        c = 'cT'+str(tier)
                        ct = result[c]         #claim card string
                        ti = 'ti'+str(tier)
                        rt = rt.split(',')
                        ct = ct.split(',')
                        ret = ''
                        cet = ''
                        tl = ''
                        recent = result['rT']
                        claim = result['cT']
                        recent = recent.split(',')
                        claim = claim.split(',')
                        
                        nrecent = ''
                        nclaim = ''
                        for i in range(0,len(tit)-2):
                            tl += str(tit[i])
                        #print(rt,ct)
                        if len(rt) >= 5:
                            #print('Here 1')
                            for i in range(0,4):
                                ret += rt[i]+','
                                cet += ct[i]+','
                                try:
                                    nrecent += recent[i]+','
                                    nclaim += claim[i]+','
                                except:
                                    print('No data')
                                
                        else:
                            #print('Here 2')
                            for i in range(0,len(rt)):
                                ret += rt[i]+','
                                cet += ct[i]+','
                                try:
                                    nrecent += recent[i]+','
                                    nclaim += claim[i]+','
                                except:
                                    print('No data 2')
                        #print(rt,ret,ct,cet)
                        #print('Lmao')
                        #print(guildData[gidv])
                        tl2 = tl
                        if guildData[gidv] != None:
                            tl += ' V'+str(guildData[gidv])
                            tl2 = tl2+' V'+str(guildData[gidv])
                        if guildData[gidClaim] == 'None':
                            ret = tl +','+ ret
                            nrecent = '**Tier: '+str(tier)+'** • '+tl +','+nrecent
                        else:
                            ret = '['+tl+']('+str(jurl)+'),'+ ret
                            nrecent = '**Tier: '+str(tier)+'** • ['+tl2+']('+str(jurl)+'),'+ nrecent
                        cet = guildData[gidClaim] + ','+cet
                        nclaim = guildData[gidClaim] + ','+nclaim
                        #print(rt,ret,ct,cet)
                        cti = datetime.datetime.now() 
                       
                        collection.update_one({"gid":message.guild.id}, {"$set":{s: ret, c: cet, ti: cti, 'rT': nrecent, 'cT': nclaim, 'ti': cti}})
                        print('Tier {} card added to recent of {}'.format(tier,message.guild))
                    except Exception as e2:
                        try:
                            description = data['description']
                            text = description.split()
                            string = ''
                            for i in range(1,len(text)):
                                string += text[i]
                                string += ' '
                            #print(string)
                            #print(text[1])
                            uid = int(text[1][2:(len(text[1])-1)])
                            user = message.guild.get_member(uid)
                            gidClaim = str(message.guild.id)+'Claim'
                            guildData[gidClaim] = str(user.mention)
                            gidt = str(message.guild.id)+'T'
                            query = {"gid": message.guild.id, "uid": uid}
                            if (levelxp.count_documents(query) != 0):
                                userxp = levelxp.find(query)
                                for result in userxp:
                                    s = 'sT'+str(guildData[gidt])
                                    count = result[s] + 1
                                    tCards = result['tCards'] + 1
                                    sCards = result['sCards'] + 1
                                levelxp.update_one({"gid":message.guild.id, "uid": uid}, {"$set":{s: count, "tCards": tCards, "sCards": sCards}})
                                print("{} claimed a Tier: {} card of total {}".format(user,guildData[gidt],count))
                            
                            #print(uid)
                            #print('check 5')
                            gid = str(message.guild.id)
                            #print(guildData)
                            
                            gids = gid+'S'
                            guildData[gids] = True
                            gidc = gid+'C'
                            gidv = str(message.guild.id)+'V'
                            vdata = description.split('`')
                            #print(description,vdata)
                            guildData[gidv] = vdata[3]
                            #print(guildData[gidv])
                            if shoobLogs != None:
                                m = guildData[gid]
                                embed = discord.Embed(
                                    colour = guildData[gidc],
                                    description = string,
                                    timestamp = datetime.datetime.now()
                                )
                                name = message.guild.name
                                embed.set_footer(text=name)
                                await m.edit(embed = embed)
                        except Exception as e:
                            print('3 Shoob Log: ',e)
                        print('2 Shoob Log: ',e2)
                except Exception as e:
                    print('1 Shoob Log: ',e)

                    
#Shoob Timer

@client.listen('on_message')
async def shoobTimer(message):
    if await check_ban(message.author.id):
        return

    guild = message.guild
    if guild == None:
        return

    
    #Read Anime Soul Embed Tier
        
    if message.author.id == 673362753489993749:
        global guildData
        query = {"gid": message.guild.id}
        guilds = collection.find(query)
        for result in guilds:
            shoobTimer = result["shoobTimer"]
            if shoobTimer == True:
                #print('Timer Log')
                
                embeds = message.embeds
                try:
                    data = embeds[0].to_dict()
                    #print(data)
                    #print('First Try')
                    try:
                        title = data['title']
                        tit = title.split()
                        for i in tit:
                            #print(i)
                            if i == "claims":
                                print("Recent check")
                                return
                            elif i == "Click":
                                print("Vote check")
                                return
                            elif i == "Guides":
                                print("Recent check")
                                return
                            elif i == "Top":
                                print("Recommendation check")
                                return
                            
                        try:
                            color = data['colour']
                        except:
                            color = data['color']
                        
                        #print('---'+title)
                        text = title+' is spawned. Remaining time: '
                        txt = text + '18s'
                        #print('I have the data')
                        embed = discord.Embed(
                            colour =color,
                            description = txt
                        )
                        m = await message.channel.send(embed = embed)
                        x = 18
                        for i in range(1,18):
                            await asyncsleep(1)
                            x -= 1
                            txt = text+str(x)+'s'
                            embed = discord.Embed(
                                colour =color,
                                description = txt
                            )
                            await m.edit(embed = embed)
                        await m.delete()
                    except Exception as e:
                        print('2 Shoob Timer: ',e)
                except Exception as e:
                    print('1 Shoob Timer: ',e)
            else:
                print('No timer in {}'.format(message.guild))



@client.command()
async def stats(ctx,user:discord.User=None):
    if await check_ban(ctx.author.id):
        print('By ban user')
        return
    
    if user is None:
        query = {"gid": ctx.guild.id, "uid": ctx.author.id}
        userxp = levelxp.find(query)
        text = ''
        for result in userxp:
            text += 'Total Claims: '+str(result['tCards'])+'\n'
            text += 'Season Claims: '+str(result['sCards'])+'\n'
            text += 'Last Season Claims: '+str(result['psCards'])+'\n\n'
            text += '<:Tier1:769600651092426792> **Tier 1** : '+ str(result['sT1'])+'\n'
            text += '<:Tier2:769595307549261854> **Tier 2** : '+ str(result['sT2'])+'\n'
            text += '<:Tier3:769595238619676693> **Tier 3** : '+ str(result['sT3'])+'\n'
            text += '<:Tier4:769592681651109888> **Tier 4** : '+ str(result['sT4'])+'\n'
            text += '<:Tier5:769592855390846986> **Tier 5** : '+ str(result['sT5'])+'\n'
            text += '<:Tier6:769592802124234802> **Tier 6** : '+ str(result['sT6'])+'\n'
        embed = discord.Embed(
            colour = discord.Colour.magenta(),
            description = text
        )
        text = str(ctx.author)+"'s Stats"
        embed.set_author(name=text)
        await ctx.send(embed=embed)

    else:
        query = {"gid": ctx.guild.id, "uid": user.id}
        userxp = levelxp.find(query)
        text = ''
        for result in userxp:
            text += 'Total Claims: '+str(result['tCards'])+'\n'
            text += 'Season Claims: '+str(result['sCards'])+'\n\n'
            text += '<:Tier1:769600651092426792> **Tier 1** : '+ str(result['sT1'])+'\n'
            text += '<:Tier2:769595307549261854> **Tier 2** : '+ str(result['sT2'])+'\n'
            text += '<:Tier3:769595238619676693> **Tier 3** : '+ str(result['sT3'])+'\n'
            text += '<:Tier4:769592681651109888> **Tier 4** : '+ str(result['sT4'])+'\n'
            text += '<:Tier5:769592855390846986> **Tier 5** : '+ str(result['sT5'])+'\n'
            text += '<:Tier6:769592802124234802> **Tier 6** : '+ str(result['sT6'])+'\n'
        embed = discord.Embed(
            colour = discord.Colour.magenta(),
            description = text
        )
        text = str(user)+"'s Stats"
        embed.set_author(name=text)
        await ctx.send(embed=embed)


        
@client.command(aliases=['lb','leaderboards'],case_insensitive=True)
async def leaderboard(ctx):
    query = {"gid": ctx.guild.id}
    userxp = levelxp.find(query)
    userxp = sorted(userxp, key = lambda i: i['sCards'],reverse=True)
    text = ''
    i = 1
    for result in userxp:
        if int(result['sCards']) == 0:
            break
        user = ctx.guild.get_member(int(result['uid']))
        text += str(i)+'. '+str(user.name)+' | Cards: '+str(result['sCards'])+'\n'
        i += 1
        if i == 20:
            break

    embed = discord.Embed(
        colour = discord.Colour.magenta(),
        description = text
    )
    text = str(ctx.guild)+"'s Leaderboard"
    embed.set_author(name=text)
    await ctx.send(embed=embed)
    
    
    
    
@client.command(aliases=['r'],case_insensitive=True)
async def recent(ctx,arg=None):
    query = {"gid": ctx.guild.id}
    guilds = collection.find(query)
    if arg != None:
        arg = arg.lower()
    for result in guilds:
        if arg == 't1':
            ct = result['cT1']
            rt = result['rT1']
            ti = result['ti1']
            color = discord.Color.from_rgb(204,204,204)
        elif arg == 't2':
            ct = result['cT2']
            rt = result['rT2']
            ti = result['ti2']
            color = discord.Color.from_rgb(122,225,141)
        elif arg == 't3':
            ct = result['cT3']
            rt = result['rT3']
            ti = result['ti3']
            color = discord.Color.from_rgb(88,160,227)
        elif arg == 't4':
            ct = result['cT4']
            rt = result['rT4']
            ti = result['ti4']
            color = discord.Color.from_rgb(173,88,227)
        elif arg == 't5':
            ct = result['cT5']
            rt = result['rT5']
            ti = result['ti5']
            color = discord.Color.from_rgb(248,241,5)
        elif arg == 't6':
            ct = result['cT6']
            rt = result['rT6']
            ti = result['ti6']
            color = discord.Color.from_rgb(234,34,34)
        else:
            ct = result['cT']
            rt = result['rT']
            ti = result['ti']
            color = discord.Colour.magenta()
        ct = ct.split(',')
        rt = rt.split(',')
        if arg == None:
            title = 'Recent spawns in '+str(ctx.guild.name)
        else:
            title = 'Recent Tier: '+arg[1]+' cards'
        text = ' '
        for i in rt:
            text += i+'\n'
        text2 = ' '
        for i in ct:
            text2 += i+'\n'
        embed = discord.Embed(
            colour = color,
        )
        embed.set_author(name=title)
        cti = datetime.datetime.now() 
        try:
            x = cti - ti
            if ((x.seconds//60)//60) == 0 and (x.days == 0):
                if (x.seconds//60) == 0:
                    n = str(x.seconds)+' seconds'
                elif (x.seconds//60) <= 5:
                    n = str((x.seconds//60)%60)+' minutes and ' + str(x.seconds%60)+' seconds'
                else:
                    n = str((x.seconds//60)%60)+' minutes'
            
            elif x.days == 0:
                n = str(x.seconds//3600)+' hours and '+ str((x.seconds//60)%60)+' minutes'
            else:
                if x.days == 1:
                    n = str(x.days)+' day and '+str(x.seconds//3600)+' hours'
                else:
                    n = str(x.days)+' days and '+str(x.seconds//3600)+' hours'
            ti = 'Last Spawn '+n+' ago'
        except Exception as e:
            print(e)
        #print(ct,text,len(ct))
        if len(text) > 2:
            embed.add_field(name='Cards', value = text, inline = False)
            embed.add_field(name='Claimed By', value = text2, inline = False)
            embed.set_footer(text=ti, icon_url=discord.Embed.Empty)
        await ctx.send(embed=embed)
    
    
    
# LEVELING SYSTEM:

@client.listen('on_message')
async def levelingXp(message):
    if await check_ban(message.author.id):
        return

    if message.author.bot == True:
        return
    
    guild = message.guild
    if guild == None:
        return

    query = {"gid": message.guild.id}
    guilds = collection.find(query)
    for result in guilds:
        mutedChList = result["mutedChannels"]
    if mutedChList != None:
        chList = mutedChList.split(' ')
        for channel in chList:
            if message.channel.id == int(channel):
                #print('{}-{} in {} is muted.'.format(message.channel,message.channel.id,message.guild))
                return


        
    #print('Messgae from {}-{} in Guild: {}-{}. From Channel: {}'.format(message.author.name,message.author,message.guild.name,message.guild.id,message.channel))
    await update_user(message.guild,message.author)
    query = {"gid": message.guild.id, "uid": message.author.id}
    userxp = levelxp.find(query)
    for result in userxp:
        mcount = result['mcount']
    if mcount != None:
        if mcount < 2:
            mcount += 1
            #print('mcount: {}'.format(mcount),end=' ')
            await add_experience(message.guild,message.author)
            levelxp.update_one({"gid": message.guild.id, "uid": message.author.id}, {"$set":{"mcount": mcount}})
        else:
            pass
            #print('{}-{} max message reached.'.format(message.author.name,message.guild.name))
    else:
        print("Error mcount: {}".format(mcount))

        



@tasks.loop(seconds=60.0)
async def message_reset():
    query = {}
    #count = 0
    userxp = levelxp.find(query)
    for result in userxp:
        gid = result['gid']
        uid = result['uid']
        mcount = result['mcount']
        if mcount != 0:
            levelxp.update_one({"gid": gid, "uid": uid}, {"$set":{"mcount": 0}})
        #count += 1
    #print('mcount reset of total: {} users.'.format(count))
message_reset.start()

        
@client.command(aliases=['dl'],case_insensitive=True)
async def disableLeveling(ctx,channel:discord.TextChannel=None):
    if await check_ban(ctx.author.id):
        print('By ban user')
        return    

    if not await perm_admin(ctx):
        return

    if channel is None:
        channel = ctx.channel
        
    query = {"gid": ctx.guild.id}
    guilds = collection.find(query)
    for result in guilds:
        mutedChList = result["mutedChannels"]
    if mutedChList is None:
        mutedChList = str(channel.id)
    else:
        chList = mutedChList.split()
        for cid in chList:
            if int(cid) == channel.id:
                await ctx.send('Xp is already disabled here')
                return
        mutedChList = mutedChList + ' ' + str(channel.id)
    
    collection.update_one({"gid":ctx.guild.id}, {"$set":{"mutedChannels": mutedChList}})
    await ctx.send('Xp is disabled in {}'.format(channel))      
        



@client.command(case_insensitive=True)
async def rank(ctx,user:discord.User=None):
    if await check_ban(ctx.author.id):
        print('By ban user')
        return
    
    if user is None:
        query = {"gid": ctx.guild.id, "uid": ctx.author.id}
        userxp = levelxp.find(query)
        if userxp is None:
            await ctx.send("You are not ranked yet.")
            return
        else:
            for result in userxp:
                level,rxp,xp = await rLevel(result['experience'])
                #print(level,rxp)

                query = {"gid": ctx.guild.id}
                userxp2 = levelxp.find(query)
                userxp3 = sorted(userxp2, key = lambda i: i['experience'],reverse=True)
                rank = 0
                for i in range(len(userxp3)):
                    if userxp3[i]['uid'] == ctx.author.id:
                        rank = i + 1
                        break
                    
                async with aiohttp.ClientSession() as session:
                    async with session.get(f'{ctx.author.avatar_url}?size=128') as resp:
                        profile_bytes = await resp.read()
                #profile_bytes = ctx.author
                        
                profile_bytes = Image.open(BytesIO(profile_bytes))
                        
                font = ImageFont.truetype('/app/arial.ttf', 24)
                medium_font = ImageFont.truetype('/app/arial.ttf', 18)
                small_font = ImageFont.truetype('/app/arial.ttf', 14)
                
                im = Image.new('RGBA', (400, 138), (44, 44, 44, 255))

                im_draw = ImageDraw.Draw(im)
                im_draw.text((154, 5), ctx.author.name, font=font, fill=(255, 255, 255, 255))

                level_text = 'Level '+str(level)
                im_draw.text((154, 37), level_text, font=medium_font, fill=(255, 255, 255, 255))
                
                rank_text = 'Rank '+str(rank)
                im_draw.text((254, 37), rank_text, font=medium_font, fill=(255, 255, 255, 255))

                xp_text = f'{rxp}/{xp}'
                im_draw.text((164, 67), xp_text, font=small_font, fill=(255, 255, 255, 255))

                im_draw.rectangle((164, 95, 374, 125), fill=(64, 64, 64, 255))
                im_draw.rectangle((164, 95, 164+(int(rxp/xp*100))*2, 125), fill=(221, 221, 221, 255))

                im_draw.rectangle((1, 1, 136, 136), fill=(255, 255, 255, 255))
                im.paste(profile_bytes, (5, 5))

                buffer = BytesIO()
                im.save(buffer, 'png')
                buffer.seek(0)
                
                await ctx.send(file=dFile(fp=buffer, filename='rank_card.png'))
                #await ctx.send("Your Xp is {}.".format(result["experience"]))
            return
    else:
        query = {"gid": ctx.guild.id, "uid": user.id}
        userxp = levelxp.find(query)
        if userxp is None:
            await ctx.send("{} is not ranked yet.".format(user.name))
            return
        else:
            
            for result in userxp:
                level,rxp,xp = await rLevel(result['experience'])
                #print(level,rxp)

                query = {"gid": ctx.guild.id}
                userxp2 = levelxp.find(query)
                userxp3 = sorted(userxp2, key = lambda i: i['experience'],reverse=True)
                rank = 0
                for i in range(len(userxp3)):
                    if userxp3[i]['uid'] == user.id:
                        rank = i + 1
                        break
                    
                async with aiohttp.ClientSession() as session:
                    async with session.get(f'{user.avatar_url}?size=128') as resp:
                        profile_bytes = await resp.read()
                #profile_bytes = ctx.author
                        
                profile_bytes = Image.open(BytesIO(profile_bytes))
                        
                font = ImageFont.truetype('/app/arial.ttf', 24)
                medium_font = ImageFont.truetype('/app/arial.ttf', 18)
                small_font = ImageFont.truetype('/app/arial.ttf', 14)
                
                im = Image.new('RGBA', (400, 138), (44, 44, 44, 255))

                im_draw = ImageDraw.Draw(im)
                im_draw.text((154, 5), user.name, font=font, fill=(255, 255, 255, 255))

                level_text = 'Level '+str(level)
                im_draw.text((154, 37), level_text, font=medium_font, fill=(255, 255, 255, 255))
                
                rank_text = 'Rank '+str(rank)
                im_draw.text((254, 37), rank_text, font=medium_font, fill=(255, 255, 255, 255))

                xp_text = f'{rxp}/{xp}'
                im_draw.text((164, 67), xp_text, font=small_font, fill=(255, 255, 255, 255))

                im_draw.rectangle((164, 95, 374, 125), fill=(64, 64, 64, 255))
                im_draw.rectangle((164, 95, 164+(int(rxp/xp*100))*2, 125), fill=(221, 221, 221, 255))

                im_draw.rectangle((1, 1, 136, 136), fill=(255, 255, 255, 255))
                im.paste(profile_bytes, (5, 5))

                buffer = BytesIO()
                im.save(buffer, 'png')
                buffer.seek(0)
                
                await ctx.send(file=dFile(fp=buffer, filename='rank_card.png'))
                #await ctx.send("Your Xp is {}.".format(result["experience"]))
            return


@client.command(case_insensitive=True)
async def levels(ctx):
    query = {"gid": ctx.guild.id}
    userxp = levelxp.find(query)
    userxp = sorted(userxp, key = lambda i: i['experience'],reverse=True)
    text = ''
    i = 1
    for result in userxp:
        level,rxp,xp = await rLevel(result['experience'])
        user = ctx.guild.get_member(int(result['uid']))
        if user == None:
            user = await client.fetch_user(int(result['uid']))            
        text += str(i)+'. '+str(user.name)+' | Level: '+str(level)+' | Xp: '+str(result['experience'])+'\n'
        i += 1
        if i == 20:
            break

    embed = discord.Embed(
        colour = discord.Colour.magenta(),
        description = text
    )
    text = str(ctx.guild)+"'s Levels"
    embed.set_author(name=text)
    await ctx.send(embed=embed)
    

               
async def rLevel(uxp):
    base = 200
    r = 100
    total = base
    i = 0
    rxp = 0
    while True:
        xp = base + r + i*100
        if uxp < total:
            rxp = uxp - (total - base)
            break
        base = xp
        total += xp
        i += 1
    #print(uxp, xp, total)
    return [i+1,rxp,xp]

async def update_user(guild,user):

    myquery = { "gid": guild.id, "uid": user.id}
    if (levelxp.count_documents(myquery) == 0):
        post = {"gid": guild.id, "uid": user.id,  "message_count": 0, "experience": 0, "mcount": 0, "tCards": 0, "sCards": 0, "sT1": 0, "sT2": 0, "sT3": 0, "sT4": 0, "sT5": 0, "sT6": 0,"psCards": 0, "afk": False, "reason": ''}
        levelxp.insert_one(post)
        print('User: {}-{} of Guild: {}-{} is added'.format(user.name,user.id,guild.name,guild.id))



async def add_experience(guild,user):

    query = {"gid": guild.id, "uid": user.id}
    userxp = levelxp.find(query)
    for result in userxp:
        result["experience"] += 10
        result["message_count"] += 1
        levelxp.update_one({"gid":guild.id, "uid": user.id}, {"$set":{"experience": result["experience"], "message_count": result["message_count"]}})
        #print('User: {}-{} of Guild: {}-{} gained experience'.format(user.name,user.id,guild.name,guild.id))

       
    
client.run(os.environ['token'])
