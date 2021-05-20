import discord
from discord.ext import commands
import platform
import datetime
import traceback
import asyncio
import json



class Help(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

    
    @commands.group(aliases=['h','Commands', 'Command'],case_insensitive=True)
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def help(self,ctx):
        if ctx.author.bot == True:
            return

        if ctx.invoked_subcommand is not None:
            return
        
        text = 'These are all the commands.'
        text += '\nIf you need further help with something please join our [Support Server](https://discord.gg/vq32pgv)'
        help_embed = discord.Embed(
                colour = discord.Colour.blue(),
                description = text
            )
        prefix = ctx.prefix
        ## Kaori roles
        text = '`ping`, `botstats`, `invite`, `support`, `help`'
        help_embed.add_field(name='• Kaori Commands', value = text, inline = False)

        
        ## Leveling roles
        text = '`rank`, `levels`'
        text += '\n[Administrator Commands]: `disableLeveling`, `disabledchannels`, `levelrole`'
        #help_embed.add_field(name='• Leveling Commands', value = text, inline = False)

        ##Welcome message
        text = '\n[Administrator Commands]: `welcome`, `welcome channel`, `welcome message`, `welcome image`, `welcome preview`, `welcome disable`, `autorole`'
        help_embed.add_field(name='• Welcome Commands', value = text, inline = False)

        ##Shoob Help
        text = '`recent`, `leaderboard`, `season`, `stats`, `card`'
        text += '\n[Administrator Commands]: `setshoob`, `shooblogs`, `shoobtimer`, `checkping`'
        help_embed.add_field(name='• Shoob Commands', value = text, inline = False)

        ## Emotes roles
        text = '`hug`, `pat`, `cuddle`, `kick`, `bite`'
        help_embed.add_field(name='• Emote Commands', value = text, inline = False)

        ##Server Help
        text = '\n[Administrator Commands]: `setstats`, `prefix`'
        help_embed.add_field(name='• Server Commands', value = text, inline = False)

        ## Misc. roles
        text = '`f`, `greet`'
        help_embed.add_field(name='• Misc. Commands', value = text, inline = False)

        footer = "For more information about a command use: `"+str(prefix)+"help command`.\nExample: `"+str(prefix)+"help ping`.\nCommands are case-insensetive."

        help_embed.add_field(name='\u200b', value = footer, inline = False)
        
        await ctx.send(embed=help_embed)


    ##KAORI

    @help.group()
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def ping(self, ctx, *, message=None):
        if ctx.author.bot == True:
            return
        text = 'Returns the ping(latency) of the Bot.'
        text += '\nUsage: `'+str(ctx.prefix)+'ping`'
        embed = discord.Embed(
                colour = discord.Colour.blue(),
                description = text
            )
        await ctx.send(embed=embed)

    @help.group()
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def botstats(self, ctx, *, message=None):
        if ctx.author.bot == True:
            return
        text = 'Returns the botstats(total servers, users, developer, version etc.).'
        text += '\nUsage: `'+str(ctx.prefix)+'botstats`'
        embed = discord.Embed(
                colour = discord.Colour.blue(),
                description = text
            )
        await ctx.send(embed=embed)

    @help.group()
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def invite(self, ctx, *, message=None):
        if ctx.author.bot == True:
            return
        text = 'Returns the bot invite link.'
        text += '\nUsage: `'+str(ctx.prefix)+'invite`'
        embed = discord.Embed(
                colour = discord.Colour.blue(),
                description = text
            )
        await ctx.send(embed=embed)

    @help.group()
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def support(self, ctx, *, message=None):
        if ctx.author.bot == True:
            return
        text = 'Returns the link for joining support server of Kaori Bot.'
        text += '\nUsage: `'+str(ctx.prefix)+'support`'
        embed = discord.Embed(
                colour = discord.Colour.blue(),
                description = text
            )
        await ctx.send(embed=embed)


    ##LEVELING COMMANDS

    @help.group()
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def rank(self, ctx, *, message=None):
        if ctx.author.bot == True:
            return
        text = '**CURRENTLY DISABLED**\nReturns the leveling rank of user.'
        text += '\nUsage: `'+str(ctx.prefix)+'rank` or `'+str(ctx.prefix)+'rank <user>`'
        embed = discord.Embed(
                colour = discord.Colour.blue(),
                description = text
            )
        await ctx.send(embed=embed)


    @help.group()
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def levels(self, ctx, *, message=None):
        if ctx.author.bot == True:
            return
        text = '**CURRENTLY DISABLED**\nReturns the list of top 20 users of this server based on levels(experience).'
        text += '\nUsage: `'+str(ctx.prefix)+'levels`'
        embed = discord.Embed(
                colour = discord.Colour.blue(),
                description = text
            )
        await ctx.send(embed=embed)

    @help.group()
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def disableLeveling(self, ctx, *, message=None):
        if ctx.author.bot == True:
            return
        text = '**CURRENTLY DISABLED**\nDisable experience gain in specific channel.'
        text += '\nUsage: `'+str(ctx.prefix)+'disableLeveling` or `'+str(ctx.prefix)+'disableLeveling <channel>`'
        text += "\nCurrently you can't enable exp again by yourself,[have to join support server and ask an developer. So beaware before using it."
        embed = discord.Embed(
                colour = discord.Colour.blue(),
                description = text
            )
        await ctx.send(embed=embed)

    @help.group()
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def disabledchannels(self, ctx, *, message=None):
        if ctx.author.bot == True:
            return
        text = '**CURRENTLY DISABLED**\nReturns the list of channels where experience gain is disabled.'
        text += '\nUsage: `'+str(ctx.prefix)+'disabledchannels`'
        embed = discord.Embed(
                colour = discord.Colour.blue(),
                description = text
            )
        await ctx.send(embed=embed)

    @help.group()
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def levelrole(self, ctx, *, message=None):
        if ctx.author.bot == True:
            return
        text = '**CURRENTLY DISABLED**\nSet up level roles. When users gain a certain level they are automatically given the certain role.\nBot needs `Manage Role permission` for this. Also the role must be in lower postion than the bot.'
        text += '\nUsage: `'+str(ctx.prefix)+'levelrole <level> <role>`'
        embed = discord.Embed(
                colour = discord.Colour.blue(),
                description = text
            )
        await ctx.send(embed=embed)


    ##WELCOME COMMANDS

    @help.group()
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def welcome(self, ctx, *, message=None):
        if ctx.author.bot == True:
            return
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

    @help.group()
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def autorole(self, ctx, *, message=None):
        if ctx.author.bot == True:
            return
        text = 'To give a role when a member joins.\nNote: Bot must have `Manage Role permission`, and role must be in lower position than the bot.'
        text += '\nUsage: `'+str(ctx.prefix)+'autorole <role>`'
        embed = discord.Embed(
                colour = discord.Colour.blue(),
                description = text
            )
        await ctx.send(embed=embed)

    
    ##Shoob Commands

    @help.group()
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def recent(self, ctx, *, message=None):
        if ctx.author.bot == True:
            return
        text = 'To see last 5 recent spawns of Shoob cards in the server or last 5 specific tier card spawns.'
        text += '\nUsage: `'+str(ctx.prefix)+'recent` or `'+str(ctx.prefix)+'recent t<tier>`'
        text += '\nExample: `'+str(ctx.prefix)+'recent t4` to see last 5 T4 cards spawned in the server.'
        text += '\nAliases: `r`.'
        embed = discord.Embed(
                colour = discord.Colour.blue(),
                description = text
            )
        await ctx.send(embed=embed)

    @help.group()
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def leaderboard(self, ctx, *, message=None):
        if ctx.author.bot == True:
            return
        text = 'Return the Overall leaderboard of the server.[Overall top 20 players according to claims]'
        text += '\nUsage: `'+str(ctx.prefix)+'leaderboard`'
        text += '\nAliases: `olb`.'
        embed = discord.Embed(
                colour = discord.Colour.blue(),
                description = text
            )
        await ctx.send(embed=embed)
        
    @help.group()
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def season(self, ctx, *, message=None):
        if ctx.author.bot == True:
            return
        text = 'Return the Season leaderboard of the server.[Season top 20 players according to claims]'
        text += '\nUsage: `'+str(ctx.prefix)+'season`'
        text += '\nAliases: `lb`, `slb`.'
        embed = discord.Embed(
                colour = discord.Colour.blue(),
                description = text
            )
        await ctx.send(embed=embed)
        
    @help.group()
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def stats(self, ctx, *, message=None):
        if ctx.author.bot == True:
            return
        text = 'Return the stats of the member in Shoob bot for this server.'
        text += '\nUsage: `'+str(ctx.prefix)+'stats` or `'+str(ctx.prefix)+'stats <member>`'
        embed = discord.Embed(
                colour = discord.Colour.blue(),
                description = text
            )
        await ctx.send(embed=embed)

    @help.group()
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def card(self, ctx, *, message=None):
        if ctx.author.bot == True:
            return
        text = 'Returns the image and link of certain card.'
        text += '\nUsage: `'+str(ctx.prefix)+'card <card-name>`'
        text += '\nExample: `'+str(ctx.prefix)+'card Naruto`'
        text += '\nIt will show all the matching cards, you need to react to view the card'
        embed = discord.Embed(
                colour = discord.Colour.blue(),
                description = text
            )
        await ctx.send(embed=embed)


    @help.group()
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def setshoob(self, ctx, *, message=None):
        if ctx.author.bot == True:
            return
        text = 'Set Shoob ping for a certain tier. Bot pings the role when that tier of Crad spawns'
        text += '\nUsage: `'+str(ctx.prefix)+'setshoob <tier-number> <role>`'
        text += '\nUsage: `'+str(ctx.prefix)+'setshoob` to disable shoob pings for all tiers.'
        text += '\nUsage: `'+str(ctx.prefix)+'setshoob <tier-number>` to disable shoob pings for a specific tier.'
        text += '\nExample: `'+str(ctx.prefix)+'setshoob 5 @<Tier 5-Role>`'
        text += '\nAliases: `ss`.'
        embed = discord.Embed(
                colour = discord.Colour.blue(),
                description = text
            )
        await ctx.send(embed=embed)

    @help.group()
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def shooblogs(self, ctx, *, message=None):
        if ctx.author.bot == True:
            return
        text = 'Returns the image and link of certain card.'
        text += '\nUsage: `'+str(ctx.prefix)+'shooblogs <channel>` to activate shoob logs in that channel.'
        text += '`'+str(ctx.prefix)+'shooblogs` to disable Shoob Logs.'
        text += '\nAliases: `sl`.'
        embed = discord.Embed(
                colour = discord.Colour.blue(),
                description = text
            )
        await ctx.send(embed=embed)


    @help.group()
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def shoobtimer(self, ctx, *, message=None):
        if ctx.author.bot == True:
            return
        text = 'Activate or deactivate Shoob despawn timer in server.'
        text += '\nUsage: `'+str(ctx.prefix)+'shoobtimer`.'
        text += '\nAliases: `st`.'
        embed = discord.Embed(
                colour = discord.Colour.blue(),
                description = text
            )
        await ctx.send(embed=embed)

    @help.group()
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def checkping(self, ctx, *, message=None):
        if ctx.author.bot == True:
            return
        text = 'Returns the list of All active Shoob Pings in the server.'
        text += '\nUsage: `'+str(ctx.prefix)+'checkping`'
        embed = discord.Embed(
                colour = discord.Colour.blue(),
                description = text
            )
        await ctx.send(embed=embed)

    @help.group()
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def setstats(self, ctx, *, message=None):
        if ctx.author.bot == True:
            return
        text = 'Sets three audio channel for Member counter stats.All Member, Member, Bots.'
        text += '\nRequires `Manage Channel` and `Manage Role` permissions.'
        text += '\nUsage: `'+str(ctx.prefix)+'setstats`'
        embed = discord.Embed(
                colour = discord.Colour.blue(),
                description = text
            )
        await ctx.send(embed=embed)

    @help.group()
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def prefix(self, ctx, *, message=None):
        if ctx.author.bot == True:
            return
        text = "To change the bot's server prefix"
        text += '\nUsage: `'+str(ctx.prefix)+'prefix` to reset to default prefix. or `'+str(ctx.prefix)+'prefix <new-prefix>` to change to new prefix.'
        embed = discord.Embed(
                colour = discord.Colour.blue(),
                description = text
            )
        await ctx.send(embed=embed)
    


    


    @commands.command()
    @commands.is_owner()
    async def heplo(self, ctx):
        pass

def setup(client):
    client.add_cog(Help(client))
