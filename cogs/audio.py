import discord
from discord.ext import commands, tasks
import youtube_dl
import asyncio
import re
from ex_bot.youtube import youtube_search
import validators

class Audio(commands.Cog):
    def __init__(self, client):
        self.client = client

    ##############################
    ####   YTDL STUFF  ###########
    ##############################

    class YTDLSource(discord.PCMVolumeTransformer):
        def __init__(self, source, *, data, volume=0.5):
            super().__init__(source, volume)
            self.data = data
            self.title = data.get("title")
            self.url = ""

        @classmethod
        async def from_url(cls, url, *, loop=None, stream=False):
            youtube_dl.utils.bug_reports_message = lambda: ""

            ytdl_format_options = {
                "format": "bestaudio/best",
                "restrictfilenames": True,
                "noplaylist": True,
                "nocheckcertificate": True,
                "ignoreerrors": False,
                "logtostderr": False,
                "quiet": True,
                "no_warnings": True,
                "default_search": "auto",
                "source_address": "0.0.0.0",
            }

            ffmpeg_options = {"options": "-vn"}

            ytdl = youtube_dl.YoutubeDL(ytdl_format_options)
            loop = loop or asyncio.get_event_loop()
            data = await loop.run_in_executor(
                None, lambda: ytdl.extract_info(url, download=not stream)
            )
            if "entries" in data:
                # take first item from a playlist
                data = data["entries"][0]
            filename = data["title"] if stream else ytdl.prepare_filename(data)
            return filename

    @commands.command(name="join", help="Tells the bot to join the voice channel")
    async def join(self, ctx):
        if not ctx.message.author.voice:
            await ctx.send(
                "{} is not connected to a voice channel".format(ctx.message.author.name)
            )
            return
        else:
            channel = ctx.message.author.voice.channel
        await channel.connect()

    @commands.command(name="leave", help="To make the bot leave the voice channel")
    async def leave(self, ctx):
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_connected():
            await voice_client.disconnect()
        else:
            await ctx.send("The bot is not connected to a voice channel.")

    @commands.command(name="play_song", help="To play song")
    async def play(self, ctx, *,search):
        server = ctx.message.guild
        voice_channel = server.voice_client
        print(search)
        if validators.url(search) == True:
            url = search
        else:
            search = search.replace(" ", "+")
            print(youtube_search(search))
            url =  youtube_search(search)
            
        print(validators.url(search))
        async with ctx.typing():
            filename = await self.YTDLSource.from_url(
                url, loop=asyncio.get_event_loop()
            )
            voice_channel.play(discord.FFmpegPCMAudio(source=filename))
        await ctx.send("**Now playing:** {}".format(search))
        # except:
        #     await ctx.send("The bot is not connected to a voice channel.")

    @commands.command(name="pause", help="This command pauses the song")
    async def pause(self, ctx):
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_playing():
            await voice_client.pause()
        else:
            await ctx.send("The bot is not playing anything at the moment.")

    @commands.command(name="resume", help="Resumes the song")
    async def resume(self, ctx):
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_paused():
            await voice_client.resume()
        else:
            await ctx.send(
                "The bot was not playing anything before this. Use play_song command"
            )

    @commands.command(name="stop", help="Stops the song")
    async def stop(self, ctx):
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_playing():
            await voice_client.stop()
        else:
            await ctx.send("The bot is not playing anything at the moment.")


def setup(client):
    client.add_cog(Audio(client))
