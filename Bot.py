import discord
from dotenv import load_dotenv
from discord.ext import commands,tasks
import random
import math
import os
from urllib import parse, request
import re
from discord.http import Route

load_dotenv('.env')



intents = discord.Intents.all()
discord.member = True
client = commands.Bot(command_prefix="$",intents = intents, activity=discord.Activity(type=discord.ActivityType.listening, name="Commands"), status=discord.Status.do_not_disturb)
client.remove_command('help')

       

@client.event
async def on_disconnect():
    general_channel = client.get_channel(881852800517173258)
    await general_channel.send('Bot has disconnected!')


    
@client.command(name='kick', pass_context = True)
@commands.has_role('Moderator')
async def kick(context, member: discord.Member):
    await member.kick()
    await context.send(' User ' + member.display_name + ' has been kicked.')


    
@client.command(name='clear')
async def clear(ctx,arg=5):
    await ctx.channel.purge(limit=int(arg))    
    


@client.command()
async def ping(ctx):
    await ctx.send(f'pong! {round(client.latency*1000)}ms')


    
@client.event
async def on_message(message):
    if message.content.lower() == '$help':
        # general_channel = client.get_channel(881852800517173258)


        myembed = discord.Embed(title="Help", description="Help command for the current bot", color=0x00ff00)
        myembed.add_field(name="Bot Prefix", value="$  -->  Use the prefix before typing a command", inline=False)
        myembed.add_field(name="Clear Message", value="$clear  -->  Clears the messages upto the limit specified", inline=False)
        myembed.add_field(name="Kick User", value="$kick  -->  Allows a user to kick a specified user(Conditions Applied)", inline=False)
        myembed.add_field(name="Ping", value="$ping  -->  Shows the client latency", inline=False)
        myembed.add_field(name="Slap User", value="$slap  -->  Slap the @mentioned user", inline=False)
        myembed.add_field(name="Youtube", value="$youtube  -->   Displays the latest videos of the channel specified.", inline=False)
        myembed.set_footer(text="This is an embed for help command")
        myembed.set_thumbnail(url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR43bel3p1GPP1VX5WR-nsu1CD1QMMLV2nNOg&usqp=CAU")
        myembed.set_author(name="Admin")
        print(type(message),message)
        myembed.set_footer(text="Information requested by: {}".format(message.author.name))
        await message.channel.send(embed=myembed)
    await client.process_commands(message) 



@client.command()
async def slap(ctx, members: commands.Greedy[discord.Member], *, reason='no reason'):
    slapped = ", ".join(x.name for x in members)
    await ctx.send('{} just got slapped for {}'.format(slapped, reason))

    
    
@client.command()
async def youtube(ctx, *, search):
    query_string = parse.urlencode({'search_query': search})
    html_content = request.urlopen('http://www.youtube.com/results?' + query_string)
    search_content= html_content.read().decode()
    search_results = re.findall(r'\/watch\?v=\w+', search_content)
    print(search_results)
    await ctx.send('https://www.youtube.com' + search_results[0])
    await ctx.send('https://www.youtube.com' + search_results[1])
    await ctx.send('https://www.youtube.com' + search_results[2])


    
@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

    
    
@client.event
async def on_member_join(member):
    embed=discord.Embed(title=member.display_name,description="Hi!, Welcome to the Discord server!", color=discord.Color.blue())
    embed.add_field(name="Type the help command to know more about the bot commands!", value="$help", inline=False)
    embed.set_thumbnail(url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR43bel3p1GPP1VX5WR-nsu1CD1QMMLV2nNOg&usqp=CAU")
    embed.set_author(name="Admin")
    embed.set_footer(text="This is an embed displayed when a new member joins the server!")
    await member.send(embed=embed)
    

client.run(os.getenv('BOT_TOKEN'))



