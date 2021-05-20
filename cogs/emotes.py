import discord
from discord.ext import commands
import platform
##import pymongo
##from pymongo import MongoClient
import urllib.parse
import datetime
import traceback
import asyncio
import giphy_client
from giphy_client.rest import ApiException
from pprint import pprint
import random
#from utils.db import collection, levelxp, levelroleDb, giveawayDB



giphy_token = '3sf9xVkjapLXXN795UQdykDdxMC1gnST'
api_instance = giphy_client.DefaultApi()

class Emotes(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

    def cog_load(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")
        

    async def search_gifs(self,query):
        try:
            response = api_instance.gifs_search_get(giphy_token, 
                query, limit=15, rating='g',lang='en')
            lst = list(response.data)
            gif = random.choices(lst)

            return gif[0].images.downsized_medium.url

        except ApiException as e:
            return "Exception when calling DefaultApi->gifs_search_get: %s\n" % e

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def hug(self, ctx,*, users = None):
        if ctx.author.bot == True:
            return
        if users == ctx.author:
            users = None
        if users == None:
            description = 'I will hug you '+str(ctx.author.mention)            
        else:
            description = str(ctx.author.mention)+' hugs '+str(users)+' how cute '            

        gif = [
            'https://media1.tenor.com/images/1069921ddcf38ff722125c8f65401c28/tenor.gif',
            'https://media1.tenor.com/images/78d3f21a608a4ff0c8a09ec12ffe763d/tenor.gif',
            'https://media1.tenor.com/images/1d94b18b89f600cbb420cce85558b493/tenor.gif',
            'https://media1.tenor.com/images/e9d7da26f8b2adbb8aa99cfd48c58c3e/tenor.gif',
            'https://media1.tenor.com/images/9dddcb8d880010200af468d781b4bbcd/tenor.gif',
            'https://media1.tenor.com/images/6db54c4d6dad5f1f2863d878cfb2d8df/tenor.gif',
            'https://media1.tenor.com/images/969f0f462e4b7350da543f0231ba94cb/tenor.gif',
            'https://media1.tenor.com/images/4e9c3a6736d667bea00300721cff45ec/tenor.gif',
            'https://media1.tenor.com/images/5ccc34d0e6f1dccba5b1c13f8539db77/tenor.gif',
            'https://media1.tenor.com/images/7db5f172665f5a64c1a5ebe0fd4cfec8/tenor.gif',
            'https://media1.tenor.com/images/daffa3b7992a08767168614178cce7d6/tenor.gif',
            'https://media1.tenor.com/images/c7efda563983124a76d319813155bd8e/tenor.gif',
            'https://media1.tenor.com/images/b62f047f8ed11b832cb6c0d8ec30687b/tenor.gif',
            'https://media1.tenor.com/images/552c49f523d61c01da04bb1128b42cbf/tenor.gif',
            'https://media1.tenor.com/images/42922e87b3ec288b11f59ba7f3cc6393/tenor.gif',
            'https://media1.tenor.com/images/c1058ebe89313d50dfc878d38630036b/tenor.gif',
            'https://media1.tenor.com/images/cc805107341e281102a2280f08b582e0/tenor.gif',
            'https://media1.tenor.com/images/074d69c5afcc89f3f879ca473e003af2/tenor.gif',
            'https://media1.tenor.com/images/16f4ef8659534c88264670265e2a1626/tenor.gif',
            'https://media1.tenor.com/images/3ce31b15c2326831a8de9f0b693763ff/tenor.gif',
            'https://media1.tenor.com/images/b4ba20e6cb49d8f8bae81d86e45e4dcc/tenor.gif',
            'https://media1.tenor.com/images/0a7494520e44fd0c9a78c5acb854a269/tenor.gif',
            'https://media1.tenor.com/images/40aed63f5bc795ed7a980d0ad5c387f2/tenor.gif',
            'https://media1.tenor.com/images/240edafecfc89af0fadd02399d730c0e/tenor.gif',
            'https://media1.tenor.com/images/949d3eb3f689fea42258a88fa171d4fc/tenor.gif',
            'https://media1.tenor.com/images/8679b6265fc8d9914ec809b630ccfd16/tenor.gif',
            'https://media1.tenor.com/images/b48748f5786679662511e841ccb3d326/tenor.gif',
            'https://media1.tenor.com/images/e3fea11903891bbb44e1d83040822746/tenor.gif',
            'https://media1.tenor.com/images/d3dca2dec335e5707e668b2f9813fde5/tenor.gif',
            'https://media1.tenor.com/images/900c0ef99c095a6a42eef2cb465a1610/tenor.gif'
        ]
        gif = str(random.choices(gif)[0])
        print(gif)
        embed = discord.Embed(
            description=description,
            colour = discord.Colour.from_rgb(88,160,227)
        )
        embed.set_image(url=(gif))
        await ctx.send(embed=embed)

    @hug.error
    async def hug_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send('Please mention a valid user')
        else:
            print(error,type(error))
            

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def pat(self, ctx, *, users = None):
        if ctx.author.bot == True:
            return
        if users == ctx.author:
            users = None
        if users == None:
            description = 'There there '+str(ctx.author.mention)+', I will pat you.'            
        else:
            description = str(ctx.author.mention)+' pats '+str(users)           


##        gif = await self.search_gifs('anime headpat')
##        while 'animal' in gif:
##            gif = await self.search_gifs('anime headpat')
        gif = [
            'https://media1.tenor.com/images/857aef7553857b812808a355f31bbd1f/tenor.gif',
            'https://media1.tenor.com/images/bfdeb9ec7f89aad86170d06fe4189bec/tenor.gif',
            'https://media1.tenor.com/images/005e8df693c0f59e442b0bf95c22d0f5/tenor.gif',
            'https://media1.tenor.com/images/8b5711095b0ba786c43b617bf9c675dd/tenor.gif',
            'https://media1.tenor.com/images/f5176d4c5cbb776e85af5dcc5eea59be/tenor.gif',
            'https://media1.tenor.com/images/0ac15c04eaf7264dbfac413c6ce11496/tenor.gif',
            'https://media1.tenor.com/images/28f4f29de42f03f66fb17c5621e7bedf/tenor.gif',
            'https://media1.tenor.com/images/f5faaccf8cc78a9c6138b3a8f8d875b6/tenor.gif',
            'https://media1.tenor.com/images/f330c520a8dfa461130a799faca13c7e/tenor.gif',
            'https://media1.tenor.com/images/54722063c802bac30d928db3bf3cc3b4/tenor.gif',
            'https://media1.tenor.com/images/c2232aec426d8b5e85e026cbca410463/tenor.gif',
            'https://media1.tenor.com/images/6bb32b2d8f4a7fa5b4b98ecf43de5917/tenor.gif',
            'https://media1.tenor.com/images/d9b480bcd392d05426ae6150e986bbf0/tenor.gif',
            'https://media1.tenor.com/images/6151c42c94df654b1c7de2fdebaa6bd1/tenor.gif',
            'https://media1.tenor.com/images/634b7ee8ffef2cd9e3c8ecb5be882fc5/tenor.gif',
            'https://media1.tenor.com/images/daa885ec8a9cfa4107eb966df05ba260/tenor.gif',
            'https://media1.tenor.com/images/55df4c5fb33f3cd05b2f1ac417e050d9/tenor.gif',
            'https://media1.tenor.com/images/c0c1c5d15f8ad65a9f0aaf6c91a3811e/tenor.gif',
            'https://media1.tenor.com/images/755b519f860ef65a4b9f889aece000fe/tenor.gif',
            'https://media1.tenor.com/images/13f385a3442ac5b513a0fa8e8d805567/tenor.gif',
            'https://media1.tenor.com/images/116fe7ede5b7976920fac3bf8067d42b/tenor.gif',
            'https://media1.tenor.com/images/da8f0e8dd1a7f7db5298bda9cc648a9a/tenor.gif',
            'https://media1.tenor.com/images/e5fff7bc2fc641f8ed0cba92475ea741/tenor.gif',
            'https://media1.tenor.com/images/55df4c5fb33f3cd05b2f1ac417e050d9/tenor.gif',
            'https://media1.tenor.com/images/116fe7ede5b7976920fac3bf8067d42b/tenor.gif',
            'https://media1.tenor.com/images/6151c42c94df654b1c7de2fdebaa6bd1/tenor.gif',
            'https://media1.tenor.com/images/b11413bc19d5a09c2f32945f962b9021/tenor.gif',
            'https://media1.tenor.com/images/daa885ec8a9cfa4107eb966df05ba260/tenor.gif',
            'https://media1.tenor.com/images/d9b480bcd392d05426ae6150e986bbf0/tenor.gif',
            'https://media1.tenor.com/images/c2232aec426d8b5e85e026cbca410463/tenor.gif',
            'https://media1.tenor.com/images/634b7ee8ffef2cd9e3c8ecb5be882fc5/tenor.gif',
            'https://media1.tenor.com/images/54722063c802bac30d928db3bf3cc3b4/tenor.gif',
            'https://media1.tenor.com/images/c0bcaeaa785a6bdf1fae82ecac65d0cc/tenor.gif',
            'https://media1.tenor.com/images/f330c520a8dfa461130a799faca13c7e/tenor.gif',
            'https://media1.tenor.com/images/f5faaccf8cc78a9c6138b3a8f8d875b6/tenor.gif',
            'https://media1.tenor.com/images/5466adf348239fba04c838639525c28a/tenor.gif',
            'https://media1.tenor.com/images/28f4f29de42f03f66fb17c5621e7bedf/tenor.gif',
            'https://media1.tenor.com/images/d3c117054fb924d66c75169ff158c811/tenor.gif',
            'https://media1.tenor.com/images/755b519f860ef65a4b9f889aece000fe/tenor.gif',
            'https://media1.tenor.com/images/c0c1c5d15f8ad65a9f0aaf6c91a3811e/tenor.gif',
            'https://media1.tenor.com/images/13f385a3442ac5b513a0fa8e8d805567/tenor.gif',
            'https://media1.tenor.com/images/63924d378cf9dbd6f78c2927dde89107/tenor.gif',
            'https://media1.tenor.com/images/398c9c832335a13be124914c23e88fdf/tenor.gif',
            'https://media1.tenor.com/images/7e14f666c08374c22e111e843be1f707/tenor.gif',
            'https://media1.tenor.com/images/8c1f6874db27c8227755a08b2b07740b/tenor.gif',
            'https://media1.tenor.com/images/37b0ba8252f8698d23c83d889768540b/tenor.gif',
            'https://media1.tenor.com/images/57b6168e77f77046f4f6b1158de7ba3d/tenor.gif',
            'https://media1.tenor.com/images/7b7cf23988e44d58b662cab127ba7ed0/tenor.gif',
            'https://media1.tenor.com/images/78421fd64eba6902f18a0574cce1b5f5/tenor.gif',
            'https://media1.tenor.com/images/bb5608910848ba61808c8f28caf6ec7d/tenor.gif',
            'https://media1.tenor.com/images/423c79d0c794a3aa2d9b8f460c454009/tenor.gif',
            'https://media1.tenor.com/images/da2e7e096c87fbb0ac422944c4941337/tenor.gif',
            'https://media1.tenor.com/images/9bf3e710f33cae1eed1962e7520f9cf3/tenor.gif',
            'https://media1.tenor.com/images/088c36ab54dc2908f0fce306443d7c04/tenor.gif'
        ]
        gif = str(random.choices(gif)[0])
        
        print(gif)
        embed = discord.Embed(
            description=description,
            colour = discord.Colour.from_rgb(88,160,227)
        )
        embed.set_image(url=(gif))
        await ctx.send(embed=embed)
        
    @pat.error
    async def pat_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send('Please mention a valid user')
        else:
            print(error,type(error))
            
    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def bite(self, ctx,*, users = None):
        if ctx.author.bot == True:
            return
        if users == ctx.author:
            users = None
        if users == None:
            description = 'I will bite you '+str(ctx.author.mention)            
        else:
            description = str(ctx.author.mention)+' bites '+str(users)+' Ouch! '            

        gif = [
            'https://media1.tenor.com/images/128c1cfb7f4e6ea4a4dce9b487648143/tenor.gif',
            'https://media1.tenor.com/images/1169d1ab96669e13062c1b23ce5b9b01/tenor.gif',
            'https://media1.tenor.com/images/f308e2fe3f1b3a41754727f8629e5b56/tenor.gif',
            'https://media1.tenor.com/images/8409bd65be28e7bcc5a7630c4ebbdcca/tenor.gif',
            'https://media1.tenor.com/images/785facc91db815ae613926cddb899ed4/tenor.gif',
            'https://media1.tenor.com/images/6dd67bd831780c4a754cb33697cddcb6/tenor.gif',
            'https://media1.tenor.com/images/6b42070f19e228d7a4ed76d4b35672cd/tenor.gif',
            'https://media1.tenor.com/images/a74770936aa6f1a766f9879b8bf1ec6b/tenor.gif',
            'https://media1.tenor.com/images/3e6d433baf1b18579149b8193eff63b1/tenor.gif'
        ]
        gif = str(random.choices(gif)[0])
        print(gif)
        embed = discord.Embed(
            description=description,
            colour = discord.Colour.from_rgb(88,160,227)
        )
        embed.set_image(url=(gif))
        await ctx.send(embed=embed)
    
    
    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def kick(self, ctx,*, users = None):
        if ctx.author.bot == True:
            return
        if users == ctx.author:
            users = None
        if users == None:
            description = 'So you need kick '+str(ctx.author.mention)            
        else:
            description = str(ctx.author.mention)+' kicks '+str(users)+' Tsundere much? '            

        gif = [
            'https://media1.tenor.com/images/fb2a19c9b689123e6254ad9ac6719e96/tenor.gif',
            'https://media1.tenor.com/images/ea2c3b49edf2080e0ef2a2325ddb4381/tenor.gif',
            'https://media1.tenor.com/images/577ecef137a88a9149f375d225724b34/tenor.gif',
            'https://media1.tenor.com/images/e2853aff4a34f7487edce8f69cfb2d01/tenor.gif',
            'https://media1.tenor.com/images/2ce5a017f6556ff103bce87b273b89b7/tenor.gif',
            'https://media1.tenor.com/images/7ad8cdd67a2937de54a75e7858f430c6/tenor.gif',
            'https://media1.tenor.com/images/04c7df6dc73f3e5ee695bd158e64411a/tenor.gif',
            'https://media1.tenor.com/images/48de12a433d1a1703d1642f5b3f361f5/tenor.gif',
            'https://media1.tenor.com/images/4dd99934237218f35c02b7cbf4ac9f9f/tenor.gif',
            'https://media1.tenor.com/images/a4d131854a2bf2ac5b72875f16ee0826/tenor.gif',
            'https://media1.tenor.com/images/e64d51fe859970926e3a00764021cfe7/tenor.gif',
            'https://media1.tenor.com/images/02545f66a6042af83b06bacaa7a5eadc/tenor.gif',
            'https://media1.tenor.com/images/3ea699f39e92d762f906ecff27d11a2c/tenor.gif',
            'https://media1.tenor.com/images/a055c6f8169a59ece905f63f48dec0c7/tenor.gif',
            'https://media1.tenor.com/images/52893e2504d5f0754c3e44c086cdc352/tenor.gif'
        ]
        gif = str(random.choices(gif)[0])
        print(gif)
        embed = discord.Embed(
            description=description,
            colour = discord.Colour.from_rgb(88,160,227)
        )
        embed.set_image(url=(gif))
        await ctx.send(embed=embed)
        
       
    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def bonk(self, ctx,*, users = None):
        if ctx.author.bot == True:
            return
        if users == ctx.author:
            users = None
        if users == None:
            description = str(ctx.author.mention)+' did bad, and got bonked!'          
        else:
            description = str(users)+' did bad and got bonked by '+str(ctx.author.mention)+' Oof!!!'          

        gif = [
            'https://media1.tenor.com/images/e2e5d72bed5d48c128363df24d1672c3/tenor.gif',
            'https://media1.tenor.com/images/cf9f90ce4ccca4fe6d82bb445ca4759e/tenor.gif',
            'https://media1.tenor.com/images/dc4329d27745a6707219cb658f5b2c46/tenor.gif',
            'https://media1.tenor.com/images/119ca32322ba24e4ffc4f0d84a6839f1/tenor.gif',
            'https://media1.tenor.com/images/194c7b9dd6fdc1e1580afca803a26d3a/tenor.gif',
            'https://media1.tenor.com/images/79e0ed5c2ed5397fa79f48fccd6265d1/tenor.gif',
            'https://media1.tenor.com/images/31fd99b00d99f7861c63aa55066ceda0/tenor.gif',
            'https://media1.tenor.com/images/2e5d3da772f126a79098f7a4d38cb3fa/tenor.gif',
            'https://media1.tenor.com/images/8cd54ee389b04a2366e85332125c5475/tenor.gif'
        ]
        gif = str(random.choices(gif)[0])
        print(gif)
        embed = discord.Embed(
            description=description,
            colour = discord.Colour.from_rgb(88,160,227)
        )
        embed.set_image(url=(gif))
        await ctx.send(embed=embed)
            
            
            

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def cuddle(self, ctx, *, users = None):
        if ctx.author.bot == True:
            return
        if users == ctx.author:
            users = None
        if users == None:
            description = 'I will cuddle you '+str(ctx.author.mention)            
        else:
            description = str(ctx.author.mention)+' cuddles '+str(users)+' how adorable.'            

        gif = [
            'https://media.tenor.com/images/70b1f80335ce0ec7627c86b9943b2206/tenor.gif',
            'https://media1.tenor.com/images/a829b33d49f61a042728c06347bddd57/tenor.gif',
            'https://media1.tenor.com/images/08de7ad3dcac4e10d27b2c203841a99f/tenor.gif?itemid=4885268',
            'https://media1.tenor.com/images/d87c5cdd0a68caf2b6feeec0f7da7315/tenor.gif',
            'https://media.giphy.com/media/Z7x24IHBcmV7W/source.gif',
            'https://media1.tenor.com/images/f2805f274471676c96aff2bc9fbedd70/tenor.gif',
            'https://media1.tenor.com/images/c2e8c095f01a2c5a4ab20aa79d370876/tenor.gif',
            'https://media1.tenor.com/images/f5df55943b64922b6b16aa63d43243a6/tenor.gif',
            'https://media1.tenor.com/images/a2b938d651a8f6b89ed4c02f9f8c13ed/tenor.gif',
            'https://media1.tenor.com/images/ec14f1673479a72db6083c0be2bee335/tenor.gif',
            'https://media1.tenor.com/images/d16a9affe8915e6413b0c1f1d380b2ee/tenor.gif',
            'https://media1.tenor.com/images/62c89d9d357a05fae42887ea732deaf9/tenor.gif',
            'https://media1.tenor.com/images/ab9c10fb601d70c8049affb288ec7eac/tenor.gif',
            'https://media1.tenor.com/images/26b91d49ece30b8ec732ac5ba3ad8e2d/tenor.gif',
            'https://media1.tenor.com/images/bfdeb9ec7f89aad86170d06fe4189bec/tenor.gif',
            'https://media1.tenor.com/images/bd8d54e9127ee5c43ecc9503858f0f49/tenor.gif'
            

        ]
        gif = str(random.choices(gif)[0])
        print(gif)
        embed = discord.Embed(
            description=description,
            colour = discord.Colour.from_rgb(88,160,227)
        )
        embed.set_image(url=(gif))
        await ctx.send(embed=embed)
        
    @cuddle.error
    async def cuddle_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send('Please mention a valid user')
        else:
            print(error,type(error))

##    @commands.command()
##    @commands.guild_only()
##    async def kiss(self, ctx, *, users = None):
##        if ctx.author.bot == True:
##            return
##        if users == ctx.author:
##            users = None
##        if user == None:
##            description = 'UwU '+str(ctx.author.mention)+', I will kiss you.'
##            await ctx.send(description)
##        else:
##            await ctx.send('Currently disabled. **Kissing** in public is lewd.')
##            
##            description = str(ctx.author.mention)+' pats '+str(users)
##            return
##
##        gif = await self.search_gifs('anime kissing')
##        while 'animal' in gif:
##            gif = await self.search_gifs('anime kissing')
##        embed = discord.Embed(
##            description=description,
##            colour = discord.Colour.from_rgb(88,160,227)
##        )
##        embed.set_image(url=(gif))
##        await ctx.send(embed=embed)
##        
##    @kiss.error
##    async def kiss_error(self, ctx, error):
##        if isinstance(error, commands.BadArgument):
##            await ctx.send('Please mention a valid user')
##        else:
##            print(error,type(error))

    @commands.command()
    @commands.is_owner()
    async def emgif(self, ctx, url):
        embed = discord.Embed(
            colour = discord.Colour.from_rgb(88,160,227)
        )
        embed.set_image(url=(url))
        await ctx.send(embed=embed)







def setup(client):
    client.add_cog(Emotes(client))
