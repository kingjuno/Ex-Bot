import discord
from discord.ext import commands
from urllib import parse, request
import re


class Fun(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f"pong! {round(self.client.latency*1000)}ms")

    @commands.command()
    async def slap(
        self, ctx, members: commands.Greedy[discord.Member], *, reason="no reason"
    ):
        slapped = ", ".join(x.name for x in members)
        await ctx.send("{} just got slapped for {}".format(slapped, reason))

    @commands.command()
    async def youtube(self, ctx, *, search):
        query_string = parse.urlencode({"search_query": search})
        html_content = request.urlopen("http://www.youtube.com/results?" + query_string)
        search_content = html_content.read().decode()
        search_results = re.findall(r"\/watch\?v=\w+", search_content)
        print(search_results)
        await ctx.send("https://www.youtube.com" + search_results[0])
        await ctx.send("https://www.youtube.com" + search_results[1])
        await ctx.send("https://www.youtube.com" + search_results[2])


def setup(client):
    client.add_cog(Fun(client))
