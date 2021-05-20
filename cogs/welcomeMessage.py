import discord
from discord.ext import commands
import platform
import urllib.parse
import os
import asyncio
import traceback
from utils.db import collection, levelxp, levelroleDb
import aiohttp
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageOps
from discord import File as dFile
import numpy as np





class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")



    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.bot == True:
            return
        #print('nani')
#        await update_user(member.guild,member)
        
        
        
        query = { "gid": member.guild.id}
        guilds = collection.find(query)
        for result in guilds:
            if result['welcomeRole'] != None:
                role = member.guild.get_role(int(result['welcomeRole']))
                try:
                    await member.add_roles(role)
                    print('autorole {} added for {}'.format(role,member))
                except Exception as e:
                    print('Missing permission on autorole at',str(member.guild),e)
            else:
                print("Welcome Role isn't activted in {}".format(member.guild))
                    
            if result['welcomeChannel'] == None:
                print('No welcome in {}'.format(member.guild))
                return
            cid = result['welcomeChannel']
            imageUrl = result['welcomeImg']
            #print('Here2')
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
                    #print(string)
                    string = ''
                    var = False
                    continue
                if var == True:
                    string += i
                else:
                    text += i
            #print('here 3')
        channel = member.guild.get_channel(cid)
        if imageUrl != None:
            try:
                buffer = await self.welcomeimage(member,imageUrl)
                await channel.send(text,file=dFile(fp=buffer, filename='welcome.png'))
            except:
                await channel.send(text)
        else:
            await channel.send(text)
        print('Welcome message sent for {} in {}.'.format(member,member.guild))





    @commands.group()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 3, commands.BucketType.guild)
    async def welcome(self, ctx):
        if ctx.author.bot == True:
            return

        
        if ctx.invoked_subcommand is None:
            text = 'Setup Welcome message for the Server. Sends a welcome message and image when a new member joins the server.'
            text += '\nUsage: `'+str(ctx.prefix)+'welcome channel <channel>` to set where welcome messages will be sent'
            text += '\n\n`'+str(ctx.prefix)+'welcome message <message>` to customize the welcome message. Message variables are {user}, {name}, {mention}, {server}, {number}.'
            text += '\nExample: `'+str(ctx.prefix)+'welcome message {mention}, welcome to our {server}. You are the {number} member of our server.`'
            text += '\n\n`'+str(ctx.prefix)+'welcome image <image-link>` to set up the welcome image. Preffered Size is 1000x400.'
            text += '\n\n`'+str(ctx.prefix)+'welcome preview` to see a preview of welcome message.'
            text += '\n\n`'+str(ctx.prefix)+'welcome disable` to disable welcome messages.'
            embed = discord.Embed(
                    colour = discord.Colour.blue(),
                    description = text
                )
            await ctx.send(embed=embed)
#            await ctx.send("This is the first command layer")


    @welcome.group()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 4, commands.BucketType.guild)
    async def message(self, ctx, *, message=None):
        if ctx.author.bot == True:
            return
        #print(f'Welcome Message: {message}')
        if message != None:
            message = str(message)
            var = False
            text = ''
            string = ''
            for i in message:
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
            await ctx.send('welcome message is updated. Use `welcome preview` to see the preview.')
        else:
            text = '{mention}, welcome to our server **{server}**. You are {number} member of our server. Please enjoy your stay.'
            collection.update_one({"gid":ctx.guild.id}, {"$set":{"welcomeMessage": text}})
            await ctx.send('welcome message is set to default. Use `welcome preview` to see the preview.')
            



    @welcome.group()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 4, commands.BucketType.guild)
    async def channel(self, ctx,channel:discord.TextChannel=None):
        if ctx.author.bot == True:
            return
        if channel == None:
            await ctx.send('Send a channel.')
            return
        try:
            await channel.send('Welcome messages will be sent here.')
            collection.update_one({"gid":ctx.guild.id}, {"$set":{"welcomeChannel": channel.id}})
        except:
            await ctx.send("I don't have permission to send messages in that channel")

    @channel.error
    async def channel_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send('Please mention a valid channel.')
        else:
            print(error,type(error))




    @welcome.group()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 4, commands.BucketType.guild)
    async def disable(self, ctx):
        if ctx.author.bot == True:
            return
        text = '{mention}, welcome to our server **{server}**. You are {number} member of our server. Please enjoy your stay.'
        collection.update_one({"gid":ctx.guild.id}, {"$set":{"welcomeChannel": None, "welcomeMessage": text, "welcomeImg": None}})
        await ctx.send('welcome messages are disabled.')

    @welcome.group()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 4, commands.BucketType.guild)
    async def image(self, ctx, *, url=None):
        if ctx.author.bot == True:
            return
        if url == None:
            collection.update_one({"gid":ctx.guild.id}, {"$set":{"welcomeImg": None}})
            await ctx.send('Welcome Image is disabled.\nNote: Preffered image size is 1000x400.')
            return
        collection.update_one({"gid":ctx.guild.id}, {"$set":{"welcomeImg": url}})
        buffer = await self.welcomeimage(ctx.author,url)
        await ctx.send('Welcome Image is set.\nType `welcome image` to disable it.\nNote: Preffered image size is 1000x400.',file=dFile(fp=buffer, filename='welcome.png'))
        


    @welcome.group()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 4, commands.BucketType.guild)
    async def preview(self, ctx):
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
            imageUrl = result['welcomeImg']
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
                    #print(string)
                    string = ''
                    var = False
                    continue
                if var == True:
                    string += i
                else:
                    text += i
        
        if imageUrl != None:
            buffer = await self.welcomeimage(ctx.author,imageUrl)
            await ctx.send(text,file=dFile(fp=buffer, filename='welcome.png'))
        else:
            await ctx.send(text)





    ##Welcome Autorole
    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 4, commands.BucketType.guild)
    async def autorole(self,ctx,role:discord.Role=None):
        if ctx.author.bot == True:
            return   
        if role == None:
            collection.update_one({"gid":ctx.guild.id}, {"$set":{"welcomeRole": None}})
            await ctx.send('Autorole is disabled.'.format(role))
            return
        
        collection.update_one({"gid":ctx.guild.id}, {"$set":{"welcomeRole": role.id}})
        await ctx.send('{} is set for autorole'.format(role))

    @autorole.error
    async def autorole_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send('please set a valid role')
        else:
            print(error,type(error))

    
    async def welcomeimage(self, member,url):
        async with aiohttp.ClientSession() as session:
            async with session.get(f'{member.avatar_url}') as resp:
                profile_bytes = await resp.read()

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                background = await resp.read()

        big_size = (200, 200)
        background_size = (1000,400)
        
        profile_bytes = Image.open(BytesIO(profile_bytes)).convert("RGB")
        background = Image.open(BytesIO(background)).convert("RGB")
        
        background.thumbnail(background_size)
        profile_bytes.thumbnail(big_size)
        
        White = Image.new("RGBA", (210,210), "white")
        mask = Image.new("L", profile_bytes.size, 0)
        mask2 = Image.new("L", White.size, 0)
        
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + big_size, fill=255)
        profile_bytes = ImageOps.fit(profile_bytes, mask.size, centering=(0.5, 0.5))
        profile_bytes.putalpha(mask)


        draw = ImageDraw.Draw(mask2)
        draw.ellipse((0, 0) + White.size, fill=255)
        White = ImageOps.fit(White, mask2.size, centering=(0.5, 0.5))
        White.putalpha(mask2)
        
        
        width, height = background.size
        big_size = (int((width - 200)/2),int((height - 300)/2))
        big_size2 = (int((width - 210)/2),int((height - 310)/2))
        welcomeH = int((height + 100)/2)
        
        
        background.paste(White, big_size2, mask2)
        background.paste(profile_bytes, big_size, mask)
        bfont = ImageFont.truetype('ARIBLK.TTF', 58)
        font = ImageFont.truetype('ARIBLK.TTF', 38)

        im_draw = ImageDraw.Draw(background)
        text = 'WELCOME'
        w, H = draw.textsize(text,font = bfont)
        
        im_draw.text(((width-w)/2,welcomeH), text, font=bfont, fill=(255, 255, 255, 255))

        text = str(member.name)
        w, h = draw.textsize(text,font = font)
        im_draw.text(((width-w)/2,welcomeH+h+10), text, font=font, fill=(255, 255, 255, 255))

        buffer = BytesIO()
        background.save(buffer, 'png')
        buffer.seek(0)

        return buffer


    @commands.command()
    @commands.is_owner()
    async def welcometest(self, ctx):
        buffer = await self.welcomeimage(ctx.author,'https://cdn.discordapp.com/attachments/773735384970428439/774143894635806741/welcomeImage.png')
        await ctx.send(file=dFile(fp=buffer, filename='welcome.png'))
    












def setup(client):
    client.add_cog(Welcome(client))
