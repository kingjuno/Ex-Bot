import discord
from dotenv import load_dotenv
from discord.ext import commands, tasks
import os
from discord.http import Route


load_dotenv('.env')


intents = discord.Intents.all()
discord.member = True
client = commands.Bot(command_prefix="$", intents=intents, activity=discord.Activity(
    type=discord.ActivityType.listening, name="Commands"), status=discord.Status.do_not_disturb)
# client.remove_command('help')

@client.event
async def on_disconnect():
    general_channel = client.get_channel(881852800517173258)
    await general_channel.send('Bot has disconnected!')


@client.event
async def on_message(message):
    if message.content.lower() == '$jhelp':
        myembed = discord.Embed(
            title="Help", description="Help command for the current bot", color=0x00ff00)
        myembed.add_field(
            name="Bot Prefix", value="$  -->  Use the prefix before typing a command", inline=False)
        myembed.add_field(
            name="Clear Message", value="$clear  -->  Clears the messages upto the limit specified", inline=False)
        myembed.add_field(
            name="Kick User", value="$kick  -->  Allows a user to kick a specified user(Conditions Applied)", inline=False)
        myembed.add_field(
            name="Ping", value="$ping  -->  Shows the client latency", inline=False)
        myembed.add_field(
            name="Slap User", value="$slap  -->  Slap the @mentioned user", inline=False)
        myembed.add_field(
            name="Youtube", value="$youtube  -->   Displays the latest videos of the channel specified.", inline=False)
        myembed.set_footer(text="This is an embed for help command")
        myembed.set_thumbnail(
            url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR43bel3p1GPP1VX5WR-nsu1CD1QMMLV2nNOg&usqp=CAU")
        myembed.set_author(name="Admin")
        print(type(message), message)
        myembed.set_footer(
            text="Information requested by: {}".format(message.author.name))
        await message.channel.send(embed=myembed)
    await client.process_commands(message)


@client.command()
@commands.has_permissions(manage_messages=True)
async def load(_, extensions):
    client.load_extension(f'cogs.{extensions}')


@client.command()
@commands.has_permissions(manage_messages=True)
async def unload(_, extensions):
    client.unload_extension(f'cogs.{extensions}')


@client.command()
@commands.has_permissions(manage_messages=True)
async def reload(_, extensions):
    client.unload_extension(f'cogs.{extensions}')
    client.load_extension(f'cogs.{extensions}')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')


@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')


@client.event
async def on_member_join(member):
    embed = discord.Embed(title=member.display_name,
                          description="Hi!, Welcome to the Discord server!", color=discord.Color.blue())
    embed.add_field(
        name="Type the help command to know more about the bot commands!", value="$help", inline=False)
    embed.set_thumbnail(
        url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR43bel3p1GPP1VX5WR-nsu1CD1QMMLV2nNOg&usqp=CAU")
    embed.set_author(name="Admin")
    embed.set_footer(
        text="This is an embed displayed when a new member joins the server!")
    await member.send(embed=embed)

###########################################################################################################################
client.run(os.getenv('BOT_TOKEN'))
