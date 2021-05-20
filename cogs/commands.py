import discord
from discord.ext import commands
import platform
import datetime
import traceback
import asyncio
from utils.db import collection, levelxp, levelroleDb, giveawayDB,globalDB



class Commands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def botstats(self, ctx):
        if ctx.author.bot == True:
            return
        """
        A usefull command that displays bot statistics.
        """
        pythonVersion = platform.python_version()
        dpyVersion = discord.__version__
        serverCount = len(self.bot.guilds)
        

        embed = discord.Embed(title=f'{self.bot.user.name} Stats', description='\uFEFF', colour=ctx.author.colour, timestamp=ctx.message.created_at)

        embed.add_field(name='Bot Version:', value=self.bot.version)
        embed.add_field(name='Python Version:', value=pythonVersion)
        embed.add_field(name='Discord.Py Version', value=dpyVersion)
        embed.add_field(name='Total Guilds:', value=serverCount)
        
        embed.add_field(name='Bot Developers:', value="<@329230819975495681>")

        embed.set_footer(text=f"{self.bot.user.name}")
        embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)

        await ctx.send(embed=embed)

    
    @commands.command(aliases=['p'])
    @commands.guild_only()
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def ping(self,ctx):
        if ctx.author.bot == True:
            return
        if ctx.guild != None:
            print('-Ping is called,{} in {} by {}'.format(round(self.bot.latency*1000),ctx.guild.name,ctx.author.name))
        else:
            print('-Ping is called,{} in DM by {}'.format(round(self.bot.latency*1000),ctx.author.name))
        await ctx.send('pong! {}ms'.format(round(self.bot.latency*1000)))



    @commands.command()
    @commands.guild_only()
    @commands.is_owner()
    async def echo(self, ctx, *, message=None):
        if ctx.author.bot == True:
            return
        """
        A simple command that repeats the users input back to them.
        """
        message = message or "Please provide the message to be repeated."
#        await ctx.message.delete()
        await ctx.send(message)

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def prefix(self, ctx, *, pre='+'):
        if ctx.author.bot == True:
            return
        """
        Set a custom prefix for a guild
        """
        collection.update_one({"gid":ctx.guild.id}, {"$set":{"prefix": pre}})
        await ctx.send('Server prefix is set to `{}`. Use `{}prefix <new_prefix>` to change prefix.'.format(pre,pre))


    @commands.command()
    @commands.is_owner()
    async def currenttime(self, ctx):
        now = datetime.datetime.now(datetime.timezone.utc)
        x = datetime.datetime(2020, 5, 17, 4)
        now = str(now)+' '+str(x)
        await ctx.send(str(now))


    
    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def f(self,ctx, * args):
        if ctx.author.bot == True:
            return
        if len(args) == 0:
            text = str(ctx.author.name)+' paid their respects.'
        else:
            text = str(ctx.author.name)+' paid their respects for '+' '.join(args)
        embed = discord.Embed(
            colour = discord.Colour.magenta(),
            description = text
        )
        await ctx.send(embed = embed)


    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def intro(self,ctx, user:discord.Member=None):
        if ctx.author.bot == True:
            return
        if user == None:
            await ctx.send("Hello I'm Kaori, <@822255174608224256>'s little sister.\nNice to meet you all.")
        else:
            await ctx.send("{}, hello I'm Kaori, <@822255174608224256>'s little sister. Nice to meet you.".format(user.name))

    @intro.error
    async def greet_error(ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send('Either mention a user or their id')
        else:
            print(error,type(error))

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def support(self,ctx):
        if ctx.author.bot == True:
            return   
        await ctx.send('Join our support server at: https://discord.gg/vq32pgv')


    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def invite(self,ctx):
        if ctx.author.bot == True:
            return
        
        #arg = 'Invite '+str(self.bot.user.name)+' to your server: [Invite Link](https://discord.com/api/oauth2/authorize?client_id=761702456169594880&permissions=269995088&scope=bot)'
        arg = "Invites are permanently closed for Kaori.\nThere are better bots(eg. Nene, Sirona) you can add them. Thank you."
        embed = discord.Embed(
            colour = discord.Colour.magenta(),
            description = arg
        )
        await ctx.send(embed = embed)
        
    @commands.command()
    @commands.guild_only()
    @commands.is_owner()
    async def guildremove(self, ctx,gid):
        if ctx.author.bot == True:
            return
        guild = self.bot.get_guild(int(gid))
        text = 'Left Guild '+str(guild)+'-'+str(guild.id)+' owner '+str(guild.owner)+str(guild.owner.id)
        await ctx.send(text)
        await guild.leave()
        
    @commands.command()
    @commands.guild_only()
    @commands.is_owner()
    async def allguildinfon(self, ctx):
        guilds = self.bot.guilds
        for guild in guilds:
            print(f'{guild} - {guild.id} - {guild.member_count} - {guild.owner} - {guild.owner.id}')
    
    @commands.command(aliases=['av'])
    @commands.guild_only()
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def avatar(self,ctx,*,text=None):
        if text == None:
            user = ctx.author
        else:
            found = False
            if '@!' in text:
                text = text[3:-1]
            elif '@' in text:
                text = text[2:-1]
                
            try:
                id = int(text)
                user = ctx.guild.get_member(id)
                found = True
            except:
                text = text.lower()
                for member in list(ctx.guild.members):
                    #print(member)
                    if  member.nick == None:
                        continue
                    if text in member.nick.lower():
                        found = True
                        user = member
                        break
                if found != True:
                    for member in list(ctx.guild.members):
                        if text in member.name.lower():
                            found = True
                            user = member
                            break
                if found != True:
                    m = await ctx.send('User not found')
                    await m.delete(delay=4)
                    return
        pfp = user.avatar_url
        color = user.colour
        embed=discord.Embed(title=user.display_name,descriptioin = pfp,color=color)
        embed.set_image(url=(pfp))
        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.is_owner()
    @commands.cooldown(1, 10, commands.BucketType.guild)
    async def embed(self, ctx, *, message='Test argument'):
        embed = discord.Embed(
            colour = discord.Colour.magenta(),
            description = message
        )
        author = ctx.author.name
        embed.set_author(name=author)
        await ctx.send(embed = embed)

    @commands.command()
    @commands.guild_only()
    @commands.is_owner()
    @commands.cooldown(1, 10, commands.BucketType.guild)
    async def emessage(self, ctx, mid, *, text='Test argument'):
        if ctx.author.bot == True:
            return
        try:
            message = await ctx.channel.fetch_message(int(mid))
        except:
            await ctx.send('Message not found.')
            return
        if message == None:
            await ctx.send('Message not found.')
            return
        elif message.author != self.bot.user:
            m = await ctx.send("Catn't edit the message.")
            await m.delete(delay = 2)
            return
        embeds = message.embeds
        print(embeds)
        try:
            data = embeds[0].to_dict()
        except:
            m = await ctx.send("Only Embed editing is allowed")
            await m.delete(delay = 2)
            return
        print(data)
        try:
            title = data['title']
        except:
            title = "Kaori Embed"
        print(title)
        embed = discord.Embed(
            colour = discord.Colour.from_rgb(0, 255, 0),
            description = text,
            title = title
        )
        await message.edit(embed = embed)

    @commands.command()
    @commands.guild_only()
    @commands.is_owner()
    @commands.cooldown(1, 10, commands.BucketType.guild)
    async def etitle(self, ctx, mid, *, text='Test argument'):
        if ctx.author.bot == True:
            return
        try:
            message = await ctx.channel.fetch_message(int(mid))
        except:
            await ctx.send('Message not found.')
            return
        if message == None:
            await ctx.send('Message not found.')
            return
        elif message.author != self.bot.user:
            m = await ctx.send("Catn't edit the message.")
            await m.delete(delay = 2)
            return
        embeds = message.embeds
        
        try:
            data = embeds[0].to_dict()
        except:
            m = await ctx.send("Only Embed editing is allowed")
            await m.delete(delay = 2)
            return
        
        try:
            description = data['description']
        except:
            description = "Placeholder"

        embed = discord.Embed(
            colour = discord.Colour.from_rgb(0, 255, 0),
            description = description,
            title = text
        )
        await message.edit(embed = embed)

    @commands.command()
    @commands.guild_only()
    @commands.is_owner()
    @commands.cooldown(1, 10, commands.BucketType.guild)
    async def edelete(self, ctx, mid):
        if ctx.author.bot == True:
            return
        try:
            message = await ctx.channel.fetch_message(int(mid))
        except:
            #await ctx.send('Message not found.')
            return
        if message == None:
            #await ctx.send('Message not found.')
            return
        elif message.author != self.bot.user:
            m = await ctx.send("Catn't delete that message.")
            await m.delete(delay = 2)
            return
        await message.delete()
    
    @commands.command()
    @commands.is_owner()
    async def printcmd(self, ctx):
        for item in self.bot.counts:
            print(self.bot.counts[item])
        await ctx.send('printed')
    
    
    @commands.command()
    @commands.guild_only()
    @commands.is_owner()
    @commands.cooldown(1, 10, commands.BucketType.guild)
    async def addtrusted(self, ctx, id):
        try:
            id = int(id)
        except:
            return
        
       
    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 10, commands.BucketType.guild)
    async def avc(self, ctx, id=None):
        if ctx.author.id in [822255174608224256,703294524897886299,730510693425741835,329230819975495681]:
            pass
        else:
            return

        
        if id == None:
            user = ctx.author
        else:
            user = await self.bot.fetch_user(int(id))
        pfp = user.avatar_url
        color = user.colour
        embed=discord.Embed(title=user.display_name,descriptioin = pfp,color=color)
        embed.set_image(url=(pfp))
        await ctx.send(embed=embed)
        
        
    @commands.command()
    @commands.guild_only()
    @commands.is_owner()
    @commands.cooldown(1, 10, commands.BucketType.guild)
    async def getc(self, ctx, gid):
        guild = self.bot.get_guild(int(gid))
        text = ''
        count = 0
        for channel in guild.channels:
            text += str(channel.name)+' : '+str(channel.id)
            count += 1
            if count >= 10:
                await ctx.send(text)
                count = 0
                text = ''
        await ctx.send(text)
        
        
        

    @commands.command()
    @commands.is_owner()
    async def updatedbconfirm(self, ctx):
        await ctx.send('Lets go...')
        if True:
            query = {}
            guilds = collection.find(query)   
            for result in guilds:
                gid = result['gid']
                try:
                    collection.update_one({"gid":gid}, {"$set":{'stclaim': 0, 'stdes':0}})
                except:
                    #text = '{mention}, welcome to our {server}. You are {number} member. Please enjoy your stay.'
                    #collection.update_one({"gid":gid}, {"$set":{'stclaim': 0, 'stdes':0}})
                    print('error in claim')
            await ctx.send('claims added')
        if True:
            query = {}
            users = levelxp.find(query)
            for result in users:
                gid = result['gid']
                uid = result['uid']
                pCards = result['sCards']
                #text = '{mention}, welcome to our {server}. You are {number} member. Please enjoy your stay.'
                levelxp.update_one({"gid":gid,"uid":uid}, {"$set":{'sCards': 0,'pCards':pCards}})
            await ctx.send('Season Reset.')



def setup(client):
    client.add_cog(Commands(client))
