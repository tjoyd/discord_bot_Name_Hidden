import discord
from discord.ext import commands
import platform
import urllib.parse
import datetime
import traceback
import asyncio
from asyncio import sleep as asyncsleep
from utils.db import collection, levelxp
import json

import aiohttp
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from discord import File as dFile


shoobId = 673362753489993749

class Shoob(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.shoob = dict()
        self.guildData = dict()
        self.carduser = dict()

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")


    @commands.Cog.listener('on_message')
    async def shoob_Ping(self, message):
        if message.author.id != shoobId:
            return
        embeds = message.embeds
        try:
            data = embeds[0].to_dict()
            title = data['title']
        except:
            return

        query = {"gid": message.guild.id}
        guilds = collection.find(query)
        for result in guilds:
            self.shoob[message.guild.id] = result
            shoobPing = result["shoobPing"]

            if shoobPing:
                embeds = message.embeds
                try:
                    data = embeds[0].to_dict()
                    title = data['title']
                except:
                    return
                txt = title.split()
                for i in txt:
                    if i == "claim" or i == "claims":
                        #print("Recent check")
                        return
                    elif i == "Click":
                        #print("Vote check")
                        return
                    elif i == "Guides":
                        #print("Recent check")
                        return
                    elif i == "Top":
                        #print("Recommendation check")
                        return
                    elif i == "voted":
                        #print("Vote check")
                        return
                    elif i == "Vote":
                        #print("Vote check")
                        return
                    elif i == "gift":
                        #print("Vote check")
                        return
                
                tier = title[len(title)-1]
                if int(tier) == 1:
                    return
                text = 'shoobPT'+str(tier)
                query = {"gid": message.guild.id}
                guilds = collection.find(query)
                for result in guilds:
                    rid = result[text]
                    if rid == None:
                        #print('Shoob Ping not set for Tier: {}'.format(tier))
                        return
                    else:
                        rid = int(rid)
                    
                role = message.guild.get_role(rid)
                if role != None:
                    await message.channel.send('{}, Shoob has spawned {}'.format(role.mention,title))
                else:
                    pass
                    #print('Shoob Ping for Tier: {} is deleted'.format(tier))


    @commands.Cog.listener('on_message')
    async def shoobLog(self,message):
    #Read Anime Soul Embed Tier
        if message.author.id == shoobId:
            embeds = message.embeds
            try:
                data = embeds[0].to_dict()
            except:
                return
            #print(self.guildData)
            jurl = message.jump_url
            result = self.shoob[message.guild.id]
            shoobLogs = result["shoobLogs"]
            if True:
                if shoobLogs != None:
                    channel = message.guild.get_channel(int(shoobLogs))

                #print(data)
                try:
                    #detects if card spawned of not
                    #print('check1')
                    #print(data)
                    title = data['title']
                    tit = title.split()
                    for i in tit:
                        #print(i)
                        if i == "claim" or i == "claims":
                            #print("Recent check")
                            return
                        elif i == "Click":
                            #print("Vote check")
                            return
                        elif i == "Guides":
                            #print("Recent check")
                            return
                        elif i == "Top":
                            #print("Recommendation check")
                            return
                        elif i == "Vote":
                            #print("Vote check")
                            return
                        elif i == "voted":
                            #print("Vote check")
                            return
                        elif i == "gift":
                            #print("Vote check")
                            return
                    try:
                        color = data['colour']
                    except:
                        color = data['color']

                    #print('---'+title)
                    #print('check2')
                    gid = message.guild.id
                    tier = tit[len(tit)-1]
                    self.guildData[gid] = dict()

                    gid = message.guild.id

                    self.guildData[gid]['spawn'] = 0  #if 0 card spwned, 1 claimed, -1 despawned
                    self.guildData[gid]['claim'] = 'No one' #Claimed by 
                    self.guildData[gid]['tier'] = tier
                    self.guildData[gid]['version'] = None #Card version if claimed
                    #print(self.guildData)
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
                        count = 0
                        try:
                            await asyncsleep(1)
                            m = await channel.send(embed = embed)
                            self.guildData[gid]['message'] = m

                            self.guildData[gid]['color'] = color
                            
                            while self.guildData[gid]['spawn'] == 0:
                                if count > 18:
                                    break
                                count += 1
                                await asyncsleep(1)

                            #print('check4')
                            if self.guildData[gid]['spawn'] == 0:
                                string = title+' is despawned'
                                embed = discord.Embed(
                                    colour = color,
                                    description = string,
                                    timestamp = datetime.datetime.now()
                                )
                                name = message.guild.name
                                embed.set_footer(text=name)
                                await m.edit(embed = embed)
                        except:
                            if count == 0:
                                while self.guildData[gid]['spawn'] == 0:
                                    if count > 18:
                                        break
                                    count += 1
                                    await asyncsleep(1)
                    else:
                        count = 0
                        while self.guildData[gid]['spawn'] == 0:
                            if count > 18:
                                break
                            count += 1
                            await asyncsleep(1)
                    try:
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
                            tl += ' '
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
                        tl2 = tl
                        if self.guildData[gid]['version'] != None:
                            tl += ' V'+str(self.guildData[gid]['version'])
                            tl2 = tl2+' V'+str(self.guildData[gid]['version'])
                        if self.guildData[gid]['claim'] == 'No one':
                            ret = tl +','+ ret
                            nrecent = '**Tier: '+str(tier)+'** • '+tl +','+nrecent
                            stdes = result['stdes'] + 1
                            stclaim = result['stclaim']
                        else:
                            ret = '['+tl+']('+str(jurl)+'),'+ ret
                            nrecent = '**Tier: '+str(tier)+'** • ['+tl2+']('+str(jurl)+'),'+ nrecent
                            stdes = result['stdes']
                            stclaim = result['stclaim'] + 1
                            
                        cet = self.guildData[gid]['claim'] + ','+cet
                        nclaim = self.guildData[gid]['claim'] + ','+nclaim
                        #print(rt,ret,ct,cet)
                        cti = datetime.datetime.now()
                                  

                        collection.update_one({"gid":message.guild.id}, {"$set":{s: ret, c: cet, ti: cti, 'rT': nrecent, 'cT': nclaim, 'ti': cti, 'stdes': stdes, 'stclaim':stclaim}})
                        print('Tier {} card added to recent of {}'.format(tier,message.guild))
                    except Exception as e:
                        print(e)
                        print('Recent addition error at guild {}-{}'.format(message.guild,message.guild.id))
                                  



                except Exception as e2:
                    try:
                        description = data['description']
                    except:
                        return
                    #print(self.guildData)
                    gid = message.guild.id
                    #print(message,message.guild,message.guild.id)
                    text = description.split()
                    string = ''
                    for i in range(1,len(text)):
                        string += text[i]
                        string += ' '
                    #print(string)
                    #print(text[1])
                    uid = int(text[1][2:(len(text[1])-1)])
                    #print(text[1], uid)
                    user = None
                    #print(user)
                    self.guildData[gid]['claim'] = str(text[1])
                    await self.update_user(message.guild,uid)
                    query = {"gid": message.guild.id, "uid": uid}
                    if (levelxp.count_documents(query) != 0):
                        userxp = levelxp.find(query)
                        for result in userxp:
                            s = 'sT'+str(self.guildData[gid]['tier'])
                            count = result[s] + 1
                            tCards = result['tCards'] + 1
                            sCards = result['sCards'] + 1
                        levelxp.update_one({"gid":message.guild.id, "uid": uid}, {"$set":{s: count, "tCards": tCards, "sCards": sCards}})
                        print("{} claimed a Tier: {} card of total {}".format(uid,self.guildData[gid]['tier'],count))

                    #print(uid)
                    #print('check 5')

                    #print(self.guildData)

                    self.guildData[gid]['spawn'] = 1

                    vdata = description.split('`')
                    #print(description,vdata)
                    self.guildData[gid]['version'] = vdata[3]
                    #print(self.guildData[gid]['version'])
                    try:
                        if shoobLogs != None:
                            m = self.guildData[gid]['message']
                            embed = discord.Embed(
                                colour = self.guildData[gid]['color'],
                                description = string,
                                timestamp = datetime.datetime.now()
                            )
                            name = message.guild.name
                            embed.set_footer(text=name)
                            await m.edit(embed = embed)
                    except:
                        pass




    @commands.Cog.listener('on_message')
    async def shoobTimer(self,message):
        if len(message.guild.members) < 11:
            return
        #Read Anime Soul Embed Tier        
        if message.author.id == shoobId:
            embeds = message.embeds
            try:
                data = embeds[0].to_dict()
            except:
                return
            #guildData = self.guildData
            result = self.shoob[message.guild.id]
            shoobTimer = result["shoobTimer"]
            if shoobTimer == True:
                #print('Timer Log')



                #print(data)
                #print('First Try')
                try:
                    title = data['title']
                except:
                    return

                tit = title.split()
                for i in tit:
                    #print(i)
                    if i == "claim" or i == "claims":
                        #print("Recent check")
                        return
                    elif i == "Click":
                        #print("Vote check")
                        return
                    elif i == "Guides":
                        #print("Recent check")
                        return
                    elif i == "Top":
                        #print("Recommendation check")
                        return
                    elif i == "voted":
                        #print("Vote check")
                        return
                    elif i == "Vote":
                        #print("Vote check")
                        return
                    elif i == "gift":
                        #print("Vote check")
                        return


                color = discord.Colour.from_rgb(0, 255, 0)

                #print('---'+title)
                text = "🟢 | **Time remaining till despawn:** "
                txt = text + '14s'
                #print('I have the data')
                embed = discord.Embed(
                    colour =color,
                    description = txt
                )
                try:
                    m = await message.channel.send(embed = embed)
                except:
                    #No permission to send message/embed
                    return
                await asyncsleep(1)
                txt = text + '13s'
                embed = discord.Embed(
                    colour =color,
                    description = txt
                )
                await m.edit(embed = embed)
                x = 13
                gid = message.guild.id
                for i in range(1,8):
                    await asyncsleep(1)
                    if self.guildData[gid]['spawn'] == 1:
                        txt = '<a:Tick:819037821762273301> | **This card is claimed.**'
                        color = discord.Colour.from_rgb(88,160,227)
                        embed = discord.Embed(
                            colour =color,
                            description = txt
                        )
                        await m.edit(embed = embed)
                        await asyncsleep(4)
                        break
                    else:
                        if x == 1:
                            x = 0
                            color = discord.Colour.from_rgb(255, 0, 0)
                            text = "🔴 | **Time remaining till despawn:** "
                            txt = text+str(x)+'s'
                            embed = discord.Embed(
                                colour =color,
                                description = txt
                            )
                            await m.edit(embed = embed)
                            await asyncsleep(1)
                        else:    
                            await asyncsleep(1)
                            x -= 2
                            if x <= 9 and x > 4:
                                color = discord.Colour.from_rgb(255, 241, 0)
                                text = "🟡 | **Time remaining till despawn:** "
                            elif x <= 4:
                                color = discord.Colour.from_rgb(255, 0, 0)
                                text = "🔴 | **Time remaining till despawn:** "
                            txt = text+str(x)+'s'
                            embed = discord.Embed(
                                colour =color,
                                description = txt
                            )
                            await m.edit(embed = embed)
                await m.delete()


    async def update_user(self,guild,uid):
        myquery = { "gid": guild.id, "uid": uid}
        if (levelxp.count_documents(myquery) == 0):
            post = {"gid": guild.id, "uid": uid,  "message_count": 0, "experience": 0, "mcount": 0, "tCards": 0, "sCards": 0, "sT1": 0, "sT2": 0, "sT3": 0, "sT4": 0, "sT5": 0, "sT6": 0,"psCards": 0, "afk": False, "reason": ''}
            levelxp.insert_one(post)
            print('User: {} of Guild: {}-{} is added'.format(uid,guild.name,guild.id))

                

    @commands.command(aliases=['ss'])
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 3, commands.BucketType.guild)
    async def setshoob(self,ctx,tier:int=None,role:discord.Role=None):
        if ctx.author.bot == True:
            return
        if tier == None:
            collection.update_one({"gid":ctx.guild.id}, {"$set":{"shoobPing": False, "shoobPT1": None, "shoobPT2": None, "shoobPT3": None,  "shoobPT4": None, "shoobPT5": None, "shoobPT6": None,}})
            await ctx.send('Shoob Ping is disabled for all tiers. To enable shoob ping use `setshoob <tier-number> <role>`\nUse: `{}help setshoob` for more info.'.format(ctx.prefix))
            return
        elif tier < 1 or tier > 6:
            await ctx.send('Not a valid tier')
            return
        
        if role == None:
            key = 'shoobPT'+str(tier)
            collection.update_one({"gid":ctx.guild.id}, {"$set":{key: None}})
            await ctx.send('Shoob ping for Tier {} is disabled. To enable shoob ping use `setshoob <tier-number> <role>`\nUse: `{}help setshoob` for more info.'.format(tier,ctx.prefix))
            return

        key = 'shoobPT'+str(tier)
        collection.update_one({"gid":ctx.guild.id}, {"$set":{"shoobPing": True, key : role.id}})

        text = "{} role is set as Shoob ping for tier {} ".format(role.mention,tier)
        embed = discord.Embed(
            colour = discord.Colour.magenta(),
            description = text
        )
        await ctx.send(embed = embed)

    @setshoob.error
    async def setshoob_error(self,ctx, error):
        if isinstance(error, commands.BadArgument):
            text = '\nUsage: `'+str(ctx.prefix)+'setshoob <tier-number> <role>`'
            text += '\nUsage: `'+str(ctx.prefix)+'setshoob` to disable shoob pings for all tiers.'
            text += '\nUsage: `'+str(ctx.prefix)+'setshoob <tier-number>` to disable shoob pings for a specific tier.'
            text += '\nExample: `'+str(ctx.prefix)+'setshoob 5 @<Tier 5-Role>`'
            embed = discord.Embed(
                    colour = discord.Colour.blue(),
                    description = text
                )
            await ctx.send(embed=embed)
        else:
            print(error,type(error))


    @commands.command(aliases=['st'])
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 4, commands.BucketType.guild)
    async def shoobtimer(self, ctx):
        if ctx.author.bot == True:
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
            #print('Shoob Timer in {} is changed to {}'.format(ctx.guild,shoobTimer))


    @commands.command(aliases=['sl'])
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 4, commands.BucketType.guild)
    async def shooblogs(self,ctx,channel:discord.TextChannel=None):
        if ctx.author.bot == True:
            return   
        if channel == None:
            collection.update_one({"gid":ctx.guild.id}, {"$set":{"shoobLogs": None}})
            await ctx.send('Shoob Logs has been disabled')
        else:
            collection.update_one({"gid":ctx.guild.id}, {"$set":{"shoobLogs": channel.id}})
            await ctx.send('{} is set for Shoob Logs'.format(channel))
        
    @shooblogs.error
    async def shooblogs_error(self,ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send('This is not the correct format.\nFormat: `shooblogs <channel>`')
        else:
            print(error,type(error))



    @commands.command(aliases=['csp'])
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def checkping(self,ctx):
        if ctx.author.bot == True:
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
                    pass
                    #print('here',result["shoobPT1"])
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
                text = 'No ping role is set for Shoob.'
                embed = discord.Embed(
                    colour = discord.Colour.magenta(),
                    description = text
                )
                await ctx.send(embed = embed)






    ##UTILITY COMMANDS
    @commands.command(aliases=['r'])
    @commands.guild_only()
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def recent(self,ctx,arg=None):
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
                embed.add_field(name='Cards', value = text, inline = True)
                embed.add_field(name='Claimed By', value = text2, inline = True)
                embed.set_footer(text=ti, icon_url=discord.Embed.Empty)
            else:
                embed = discord.Embed(
                    colour = color,
                    description = 'No recent cards'
                )
                embed.set_author(name=title)
                
            await ctx.send(embed=embed)



    @commands.command(aliases=['lb','slb'])
    @commands.guild_only()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def season(self,ctx):
        query = {"gid": ctx.guild.id}
        userxp = levelxp.find(query)
        userxp = sorted(userxp, key = lambda i: i['sCards'],reverse=True)
        text = '```'
        i = 1
        arank = 0
        for result in userxp:
            if int(result['sCards']) == 0:
                break
            if int(result['uid']) == ctx.author.id:
                arank = i
            user = ctx.guild.get_member(int(result['uid']))
            if user == None:
                user = await self.bot.fetch_user(int(result['uid']))
            extra = ''
            if len(str(user.name))<20:
                for k in range(20-len(str(user.name))):
                    extra += ' '
            text += ''+str(i)+'. '+str(user.name)+str(extra)+' Cards: '+str(result['sCards'])+'\n'
            i += 1
            if i == 21:
                break
            
        text += '```'
        embed = discord.Embed(
            colour = discord.Colour.magenta(),
            description = text,
            timestamp = datetime.datetime.now()
        )
        text = str(ctx.guild)+"'s Season Leaderboard"
        embed.set_author(name=text)
        if arank == 0:
            footer = str(ctx.author.name)+' is not ranked yet.'
        else:
            footer = str(ctx.author.name)+"'s rank is #"+str(arank)
        embed.set_footer(text=footer)
        await ctx.send(embed=embed)



    @commands.command(aliases=['olb'])
    @commands.guild_only()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def leaderboard(self,ctx):
        query = {"gid": ctx.guild.id}
        userxp = levelxp.find(query)
        userxp = sorted(userxp, key = lambda i: i['tCards'],reverse=True)
        text = '```'
        i = 1
        arank = 0
        for result in userxp:
            if int(result['tCards']) == 0:
                break
            if int(result['uid']) == ctx.author.id:
                arank = i
            user = ctx.guild.get_member(int(result['uid']))
            if user == None:
                user = await self.bot.fetch_user(int(result['uid']))
            extra = ''
            if len(str(user.name))<20:
                for k in range(20-len(str(user.name))):
                    extra += ' '
            text += ''+str(i)+'. '+str(user.name)+str(extra)+' Cards: '+str(result['tCards'])+'\n'
            i += 1
            if i == 21:
                break
        text += '```'
        embed = discord.Embed(
            colour = discord.Colour.magenta(),
            description = text,
            timestamp = datetime.datetime.now()
        )
        text = str(ctx.guild)+"'s Overall Leaderboard"
        embed.set_author(name=text)
        if arank == 0:
            footer = str(ctx.author.name)+' is not ranked yet.'
        else:
            footer = str(ctx.author.name)+"'s rank is #"+str(arank)+"."
        embed.set_footer(text=footer)
        await ctx.send(embed=embed)




    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def stats(self,ctx,user:discord.User=None):
        
        if user is None:
            await self.update_user(ctx.guild,ctx.author.id)
            query = {"gid": ctx.guild.id, "uid": ctx.author.id}
            userxp = levelxp.find(query)
            text = ''
            for result in userxp:
                text += 'Total Claims: '+str(result['tCards'])+'\n'
                text += 'Season Claims: '+str(result['sCards'])+'\n'
                
                text += '<:tier1:825974256046964747> **Tier 1** : '+ str(result['sT1'])+'\n'
                text += '<:tier2:825974256433102848> **Tier 2** : '+ str(result['sT2'])+'\n'
                text += '<:tier3:825974256075800606> **Tier 3** : '+ str(result['sT3'])+'\n'
                text += '<:tier4:825974256042115073> **Tier 4** : '+ str(result['sT4'])+'\n'
                text += '<:tier5:825974255811690568> **Tier 5** : '+ str(result['sT5'])+'\n'
                text += '<:tier6:825974255966748674> **Tier 6** : '+ str(result['sT6'])+'\n'
            embed = discord.Embed(
                colour = discord.Colour.magenta(),
                description = text
            )
            text = str(ctx.author)+"'s Stats"
            embed.set_author(name=text)
            await ctx.send(embed=embed)

        else:
            await self.update_user(ctx.guild,user.id)
            query = {"gid": ctx.guild.id, "uid": user.id}
            userxp = levelxp.find(query)
            text = ''
            for result in userxp:
                text += 'Total Claims: '+str(result['tCards'])+'\n'
                text += 'Season Claims: '+str(result['sCards'])+'\n\n'
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
            text = str(user)+"'s Stats"
            embed.set_author(name=text)
            await ctx.send(embed=embed)

        
    async def cardpage(self,message, result, info_id, pos, mov,ctx):
        if ctx.author in self.carduser:
            if self.carduser[ctx.author] != 1:
                return
        await asyncsleep(1)
        title = 'Search result'
        description = ''
        count = int(pos+mov)*10
        k = 0
        for j in range(len(result)-count):
            i = result[j+count]
            description += "**"+str(j+count+1)+"**. "+str(i['name']) + " - `Tier: "+str(i['tier'])+"`- Info Id: "+str(info_id[j+count])+"\n"
            k += 1
            if k >= 10:
                break
        color = discord.Color.from_rgb(122,225,141)    
        embed = discord.Embed(
            colour = color,
            title = title,
            description = description
        )

        if (pos+mov) != 0:
            if len(result) > count+10:
                embed.set_footer(text="Reply with the number. For next page type `next` or previous page type `prev`.")
            else:
                embed.set_footer(text="Reply with the number. For previous page type `prev`.")
        else:
            if len(result) > count+10:
                embed.set_footer(text="Reply with the number. For next page type `next`.")
            else:
                embed.set_footer(text="Reply with the number.")
        await message.edit(embed=embed)
        prefix = ctx.prefix
        text = str(prefix)+'c '
        text2 = str(prefix)+'card '
        def check(m):
            if m.content.lower().startswith(text) or m.content.lower().startswith(text2):
                return m.channel == ctx.channel and m.author == ctx.author
            for j in range(len(result)-count):
                if m.content == str(count+j+1):
                    return m.content == str(count+j+1) and m.channel == ctx.channel and m.author == ctx.author
            
            if len(result) > count+10:
                if m.content.lower() == 'next':
                    return m.content.lower() == 'next' and m.channel == ctx.channel and m.author == ctx.author
            if (pos+mov) != 0:
                if m.content.lower() == 'prev' or m.content.lower() == 'previous':
                    return m.content.lower() == 'prev' and m.channel == ctx.channel and m.author == ctx.author
        try:
            msg = await self.bot.wait_for('message', timeout=60.0, check=check)
        except asyncio.TimeoutError:
            self.carduser[ctx.author] = 0
            return
        else:
            if msg.content.lower().startswith(text) or msg.content.lower().startswith(text2):
                self.carduser[ctx.author] -= 1
                return
            if msg.content.lower() == 'next':
                await self.cardpage(message, result, info_id, pos+mov, 1,ctx)
                return
            if msg.content.lower() == 'prev':
                await self.cardpage(message, result, info_id, pos+mov, -1,ctx)
                return
            id = int(msg.content)
            id -= 1
        tier = str(result[id]['tier'])
        if tier == '1':
            color = discord.Color.from_rgb(204,204,204)
        elif tier == '2':
            color = discord.Color.from_rgb(122,225,141)
        elif tier == '3':
            color = discord.Color.from_rgb(88,160,227)
        elif tier == '4':
            color = discord.Color.from_rgb(173,88,227)
        elif tier == '5':
            color = discord.Color.from_rgb(248,241,5)
        elif tier == '6':
            color = discord.Color.from_rgb(234,34,34)
        else:
            color = discord.Colour.magenta()
        title = str(result[id]['name']) + " Tier: "+str(result[id]['tier'])
        description = "Info Id: "+str(info_id[id])
        embed = discord.Embed(
            colour = color,
            url = result[id]['link'],
            title = title,
            description = description
        )
        image = result[id]['image']
        if '.png' not in image and '.gif' not in image:
            #print(image)
            await message.delete()
            
            async with aiohttp.ClientSession() as session:
                async with session.get(f'{image}') as resp:
                    profile_bytes = await resp.read()
                    
            profile_bytes = Image.open(BytesIO(profile_bytes))
            mask = Image.new("RGBA", profile_bytes.size, 0)
            mask.paste(profile_bytes, (0, 0))

            buffer = BytesIO()
            mask.save(buffer, 'png')
            buffer.seek(0)

            
            #await ctx.send(file=dFile(fp=buffer, filename='card.png'))
            
            imageFile = discord.File(fp=buffer, filename="image.png")
            embed.set_image(url="attachment://image.png")
            message = await ctx.send(file=imageFile, embed=embed)
            #print('ooooog')
            
        else:
            #print(image)
            #print('Ok ok')
            embed.set_image(url=(image))
            await message.edit(embed=embed)
        def check2(m):
            if m.content.lower() == 'back':
                return m.content.lower() == 'back' and m.channel == ctx.channel and m.author == ctx.author
        try:
            msg = await self.bot.wait_for('message', timeout=60.0, check=check2)
        except asyncio.TimeoutError:
            self.carduser[ctx.author] = 0
            return
        else:
            if msg.content.lower() == 'back':
                await self.cardpage(message, result, info_id, 0, 0,ctx)
                return


    @commands.command(aliases=['c'])
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def card(self,ctx,*,name=None):
        if ctx.author in self.carduser:
            self.carduser[ctx.author] += 1
        else:
            self.carduser[ctx.author] = 1
        if name == None:
            await ctx.send(f"Correct format is `{ctx.prefix}card <card-name>`\nExample: `{ctx.prefix}card naruto`\n`{ctx.prefix}card -t6 naruto`.")
            return
        name = name.lower()
        name = name.strip()
        name = name.split(' ')
        for i in name:
            i = i.strip()
        
        tier = None
        if name[0].startswith('-t'):
            try:
                tier = name[0][2]
            except:
                tier = None
            name.pop(0)
        if tier not in ['1','2','3','4','5','6','s']:
            tier = None
            
        result = list()
        info_id = list()
        eventCard = False
        for i in range(len(name)):
            if name[i] == 'e' or name[i] == 'event':
                eventCard = True
                name.pop(i)
                break
                
        with open('/app/Data/cards.json','r') as f:
            cards = json.load(f)
            
        if eventCard == False:
            for i in cards:
                check = False
                for item in name:
                    if item in cards[i]['name'].lower():
                        check = True
                    else:
                        check = False
                        break

                if check == True:
                    if tier != None:
                        if cards[i]['tier'].lower() == tier:
                            result.append(cards[i])
                            info_id.append(i)
                    else:
                        result.append(cards[i])
                        info_id.append(i)
          
        with open('/app/Data/cards_e.json','r') as f:
            cards_e = json.load(f)
        
        for i in cards_e:
            check = False
            for item in name:
                if item in cards_e[i]['name'].lower():
                    check = True
                else:
                    check = False
                    break
                    
            if check == True:
                if tier != None:
                    if cards_e[i]['tier'].lower() == tier:
                        result.append(cards_e[i])
                        info_id.append(str(len(cards)+int(i)))
                else:
                    result.append(cards_e[i])
                    info_id.append(str(len(cards)+int(i)))
                
        if len(result) == 0:
            await ctx.send(f"Card not found.\nCorrect format is `{ctx.prefix}card <card-name>`\nExample: `{ctx.prefix}card naruto`\n`{ctx.prefix}card -t6 naruto`.")
            return
        else:
            color = discord.Color.from_rgb(122,225,141)
            if len(result) != 1:
                title = 'Search result'
                description = ''
                count = 0
                for i in result:
                    description += "**"+str(count+1)+"**. "+str(i['name']) + " - `Tier: "+str(i['tier'])+"`- Info Id: "+str(info_id[count])+"\n"
                    count += 1
                    if count == 10:
                        break

                embed = discord.Embed(
                    colour = color,
                    title = title,
                    description = description
                )

                #embed.set_author(name=title,url = result['link'])
                if len(result) > 10:
                    embed.set_footer(text="Reply with the number. For next page type `next`.")
                else:
                    embed.set_footer(text="Reply with the number.")
                message = await ctx.send(embed=embed)

                prefix = ctx.prefix
                text = str(prefix)+'c '
                text2 = str(prefix)+'card '
                def check(m):
                    if m.content.lower().startswith(text) or m.content.lower().startswith(text2):
                        return m.channel == ctx.channel and m.author == ctx.author
                    if m.content == '1':
                        return m.content == '1' and m.channel == ctx.channel and m.author == ctx.author
                    elif m.content == '2':
                        return m.content == '2' and m.channel == ctx.channel and m.author == ctx.author
                    elif m.content == '3':
                        return m.content == '3' and m.channel == ctx.channel and m.author == ctx.author
                    elif m.content == '4':
                        return m.content == '4' and m.channel == ctx.channel and m.author == ctx.author
                    elif m.content == '5':
                        return m.content == '5' and m.channel == ctx.channel and m.author == ctx.author
                    elif m.content == '6':
                        return m.content == '6' and m.channel == ctx.channel and m.author == ctx.author
                    elif m.content == '7':
                        return m.content == '7' and m.channel == ctx.channel and m.author == ctx.author
                    elif m.content == '8':
                        return m.content == '8' and m.channel == ctx.channel and m.author == ctx.author
                    elif m.content == '9':
                        return m.content == '9' and m.channel == ctx.channel and m.author == ctx.author
                    elif m.content == '10':
                        return m.content == '10' and m.channel == ctx.channel and m.author == ctx.author
                    elif len(result) > 10:
                        if m.content.lower() == 'next':
                            return m.content.lower() == 'next' and m.channel == ctx.channel and m.author == ctx.author

                try:
                    msg = await self.bot.wait_for('message', timeout=30.0, check=check)
                except asyncio.TimeoutError:
                    self.carduser[ctx.author] = 0
                    return
                else:
                    #print(msg.content)
                    if msg.content.lower().startswith(text) or msg.content.lower().startswith(text2):
                        self.carduser[ctx.author] -= 1
                        return
                    if msg.content.lower() == 'next':
                        await self.cardpage(message, result, info_id, 0, 1,ctx)
                        return
                    id = int(msg.content)
                    id -= 1
            else:
                id = 0
                title = 'Place Holder'
                description = 'None'
                embed = discord.Embed(
                    colour = color,
                    title = title,
                    description = description
                )
                message = await ctx.send(embed=embed)
                
            tier = str(result[id]['tier'])
            if tier == '1':
                color = discord.Color.from_rgb(204,204,204)
            elif tier == '2':
                color = discord.Color.from_rgb(122,225,141)
            elif tier == '3':
                color = discord.Color.from_rgb(88,160,227)
            elif tier == '4':
                color = discord.Color.from_rgb(173,88,227)
            elif tier == '5':
                color = discord.Color.from_rgb(248,241,5)
            elif tier == '6':
                color = discord.Color.from_rgb(234,34,34)
            else:
                color = discord.Colour.magenta()
            title = str(result[id]['name']) + " Tier: "+str(result[id]['tier'])
            description = "Info Id: "+str(info_id[id])
            embed = discord.Embed(
                colour = color,
                url = result[id]['link'],
                title = title,
                description = description
            )
            image = result[id]['image']
            image = result[id]['image']
            if '.png' not in image and '.gif' not in image:
                #print(image)
                await message.delete()
                async with aiohttp.ClientSession() as session:
                    async with session.get(f'{image}') as resp:
                        profile_bytes = await resp.read()
                        
                profile_bytes = Image.open(BytesIO(profile_bytes))
                mask = Image.new("RGBA", profile_bytes.size, 0)
                mask.paste(profile_bytes, (0, 0))

                buffer = BytesIO()
                mask.save(buffer, 'png')
                buffer.seek(0)

                #await ctx.send(file=dFile(fp=buffer, filename='card.png'))
                imageFile = discord.File(fp=buffer, filename="image.png")
                embed.set_image(url="attachment://image.png")
                message = await ctx.send(file=imageFile, embed=embed)
                
            else:
                #print(image)
                #print('Ok ok')
                embed.set_image(url=(image))
                await message.edit(embed=embed)
            def check2(m):
                if m.content.lower() == 'back':
                    return m.content.lower() == 'back' and m.channel == ctx.channel and m.author == ctx.author
            try:
                msg = await self.bot.wait_for('message', timeout=30.0, check=check2)
            except asyncio.TimeoutError:
                self.carduser[ctx.author] = 0
                return
            else:
                if msg.content.lower() == 'back':
                    await self.cardpage(message, result, info_id, 0, 0,ctx)
                    return
                
    @card.error
    async def card_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send('Please enter a valid name.')
        else:
            print(error,type(error))
        
                
                



def setup(client):
    client.add_cog(Shoob(client))
