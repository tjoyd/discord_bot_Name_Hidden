import discord
from discord.ext import tasks, commands
import platform
import datetime
import traceback
import asyncio
from utils.db import collection



class Serverstats(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.update_stats.start()

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

    def cog_unload(self):
        self.update_stats.cancel()


    @tasks.loop(minutes=5.0)
    async def update_stats(self):
        print('Updating Server stats')
        query = {}
        guilds = collection.find(query)
        print(guilds.count())
        for result in guilds:
            #print("Updating....")
            gid = result['gid']
            cid1 = result['achannel']
            cid2 = result['mchannel']
            cid3 = result['bchannel']
            #print("part 0 fine")
            guild = self.bot.get_guild(int(gid))
            if guild == None:
                continue
            #print("part 1 fine")
            if len(str(cid1)) > 2:
                try:
                    achannel = self.bot.get_channel(cid1)
                except Exception as e:
                    #print('{}, All channel not found in {}'.format(e,guild.name))
                    if len(str(cid2)) > 2:
                        try:
                            mchannel = self.bot.get_channel(cid2)
                        except Exception as e:
                            #print('{}, Member channel not found in {}'.format(e,guild.name))
                            if len(str(cid3)) > 2:
                                try:
                                    bchannel = self.bot.get_channel(cid3)  
                                except Exception as e:
                                    print('No stats',e)
                                    return
                            else:
                                return
                    else:
                        if len(str(cid3)) > 2:
                            try:
                                bchannel = self.bot.get_channel(cid3)  
                            except Exception as e:
                                print('No stats',e)
                                return
                        else:
                            return
            else:
                if len(str(cid2)) > 2:
                    try:
                        mchannel = self.bot.get_channel(cid2)
                    except Exception as e:
                        #print('{}, Member channel not found in {}'.format(e,guild.name))
                        if len(str(cid3)) > 2:
                            try:
                                bchannel = self.bot.get_channel(cid3)  
                            except Exception as e:
                                print('No stats',e)
                                return
                        else:
                            return
                else:
                    if len(str(cid3)) > 2:
                        try:
                            bchannel = self.bot.get_channel(cid3)  
                        except Exception as e:
                            print('No stats',e)
                            return
                    else:
                        return
                        
            #print("Here part 2")
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
                    achannel = self.bot.get_channel(cid1)
                    name = 'All Members: '+str(acount)
                    await achannel.edit(name=name)
                except Exception as e:
                    pass
                    #print('{}, All channel not found in {}'.format(e,guild.name))
            if len(str(cid2)) > 2:
                try:
                    mchannel = self.bot.get_channel(cid2)
                    name = 'Members: '+str(mcount)
                    await mchannel.edit(name=name)
                except Exception as e:
                    pass
                    #print('{}, Member channel not found in {}'.format(e,guild.name))
            
            if len(str(cid3)) > 2:
                try:
                    bchannel = self.bot.get_channel(cid3)  
                    name = 'Bots: '+str(bcount)
                    await bchannel.edit(name=name)
                except Exception as e:
                    pass
            #print("Here part 3")
                    #print('{}, Bot channel not found in {}'.format(e,guild.name))
        print('Done updating Server stats')
    @update_stats.before_loop
    async def before_update_stats(self):
        #print('waiting...')
        await self.bot.wait_until_ready()
    
    


    @commands.group()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 4, commands.BucketType.guild)
    async def setStats(self,ctx):
        if ctx.author.bot == True:
            return   
        m = await ctx.send('Please react with 👍 for confirmation')
        await m.add_reaction('👍')
        
        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) == '👍'

        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=20.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send('Time Out.')
            return
        
            
        acount = 0
        bcount = 0
        mcount = 0
        guild = ctx.guild
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
        await category.set_permissions(self.bot.user, overwrite=overwrite)
        
        
        name = 'All Members: '+str(acount)
        channel = await guild.create_voice_channel(name, category=category)
        await channel.set_permissions(guild.default_role, overwrite=overwritee)
        await channel.set_permissions(self.bot.user, overwrite=overwrite)
        cid1 = channel.id
        
        name = 'Members: '+str(mcount)
        channel = await guild.create_voice_channel(name, category=category)
        await channel.set_permissions(guild.default_role, overwrite=overwritee)
        await channel.set_permissions(self.bot.user, overwrite=overwrite)
        cid2 = channel.id
        
        name = 'Bots: '+str(bcount)
        channel = await guild.create_voice_channel(name, category=category)
        await channel.set_permissions(guild.default_role, overwrite=overwritee)
        await channel.set_permissions(self.bot.user, overwrite=overwrite)
        cid3 = channel.id
        
        collection.update_one({"gid":ctx.guild.id}, {"$set":{"achannel": cid1, "mchannel": cid2, "bchannel": cid3}})
        
        await ctx.send('Server stats has been created.\nTo disable just delete the channels.')






















def setup(client):
    client.add_cog(Serverstats(client))
