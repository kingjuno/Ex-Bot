import discord
from discord.ext import commands


class Admin(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="kick", pass_context=True)
    @commands.has_role("Moderator")
    async def kick(self, ctx, member: discord.Member):
        await member.kick()
        await ctx.send(" User " + member.display_name + " has been kicked.")

    @commands.command(name="clear")
    async def clear(self, ctx, arg=5):
        await ctx.channel.purge(limit=int(arg))


def setup(client):
    client.add_cog(Admin(client))
