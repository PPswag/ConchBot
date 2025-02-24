import aiosqlite
import discord
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
from dotenv import load_dotenv
import os
import datetime

env = load_dotenv()


class Support(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def support(self, ctx):
        embed = discord.Embed(
            title="ConchBot Support",
            colour=discord.Colour.gold()
        )
        embed.add_field(name="You Just Used the Support Command!", value="This means you either have a question about ConchBot,"
        " would like to report an error or bug, or just want to join the ConchBot community!")
        embed.add_field(name="ConchBot Discord Server", value="You can join ConchBot's support server [here](https://discord.gg/PyAcRfukvc)")
        embed.add_field(name="Or, if you don't want to join a server...", value="You can submit bugs or errors via 'cb report {description of bug}.")
        await ctx.send(embed=embed)
    
    @commands.command()
    @commands.cooldown(1, 86400, commands.BucketType.user)
    async def report(self, ctx, *, content):
        channel = self.client.get_channel(795711741606101024)
        db = await aiosqlite.connect('./bot/db/config.db')
        cursor = await db.cursor()
        await cursor.execute('SELECT num FROM bugnum WHERE placeholder = 1')
        result = await cursor.fetchone()
        num = result[0]+1
        embed = discord.Embed(
            title=f"Bug Report #{num}",
            colour=discord.Colour.red()
        )
        embed.add_field(name="Submitted By:", value=ctx.author)
        embed.add_field(name="Bug Description:", value=content)
        await cursor.execute(f'UPDATE bugnum SET num = {num} WHERE placeholder = 1')
        await channel.send(embed=embed)
        await ctx.send("Thank you for the bug report! Our team will identify and fix the problem as soon as possible!")
        await db.commit()
        await cursor.close()
        db.close

    @commands.command()
    @commands.cooldown(1, 86400, BucketType.user)
    async def suggest(self, ctx, *, suggestion):
        channel = self.client.get_channel(819029394534039604)
        if channel is None:
            await ctx.guild.create_text_channel('suggestions')
            channel = discord.utils.get(ctx.guild.channels, name="suggestions")
        if len(suggestion)>100:
            await ctx.send("Please keep your suggestion under 100 characters as to not flood the suggestions channel.")
        elif len(suggestion)<10:
            await ctx.send("That suggestion is too short. Your suggestion must be more than 10 characters long.")
        else:
            embed = discord.Embed(
                title=f"{ctx.author.name}#{ctx.author.discriminator} has a suggestion!",
                colour=ctx.author.colour
            )
            embed.add_field(name="Submitted by:", value=ctx.author.name)
            embed.add_field(name="Suggestion:", value=suggestion)
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            await ctx.send("Your suggestion has been submitted!")
            suggestion_message = await channel.send(embed=embed)
            await suggestion_message.add_reaction("⬆️")
            await suggestion_message.add_reaction("⬇️")

    


    @suggest.error
    async def suggest_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You must input a suggestion for ConchBot.")
            return

            
def setup(client):
    client.add_cog(Support(client))
