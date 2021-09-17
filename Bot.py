import discord
from dotenv import load_dotenv
from discord.ext import commands,tasks
import random
import math
import os
from urllib import parse, request
import re
from discord.http import Route
import youtube_dl
import ffmpeg
import asyncio


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


youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' 
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = ""

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]
        filename = data['title'] if stream else ytdl.prepare_filename(data)
        return filename

@client.command(name='join', help='Tells the bot to join the voice channel')
async def join(ctx):
    if not ctx.message.author.voice:
        await ctx.send("{} is not connected to a voice channel".format(ctx.message.author.name))
        return
    else:
        channel = ctx.message.author.voice.channel
    await channel.connect()

@client.command(name='leave', help='To make the bot leave the voice channel')
async def leave(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_connected():
        await voice_client.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")

@client.command(name='play_song', help='To play song')
async def play(ctx,url):
    try :
        server = ctx.message.guild
        voice_channel = server.voice_client

        async with ctx.typing():
            filename = await YTDLSource.from_url(url, loop=client.loop)
            voice_channel.play(discord.FFmpegPCMAudio(executable="C:\\Users\\sande\\AppData\\Local\\Programs\\LNV\\Stremio-4\\ffmpeg.exe", source=filename))
        await ctx.send('**Now playing:** {}'.format(filename))
    except:
        await ctx.send("The bot is not connected to a voice channel.")


@client.command(name='pause', help='This command pauses the song')
async def pause(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.pause()
    else:
        await ctx.send("The bot is not playing anything at the moment.")
    
@client.command(name='resume', help='Resumes the song')
async def resume(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_paused():
        await voice_client.resume()
    else:
        await ctx.send("The bot was not playing anything before this. Use play_song command")

@client.command(name='stop', help='Stops the song')
async def stop(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.stop()
    else:
        await ctx.send("The bot is not playing anything at the moment.")

    

client.run(os.getenv('BOT_TOKEN'))



