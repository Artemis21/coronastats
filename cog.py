from discord.ext import commands

import embeds


class Stats(commands.Cog):
    '''Various coronavirus stats.
    '''
    @commands.command(brief='Check affected countries.')
    async def affected(self, ctx):
        '''See a list of currently affected countries.
        '''
        await ctx.send(**embeds.affected())

    @commands.command(brief="Check a country's history.")
    async def history(self, ctx, *, country):
        '''See a graph of the disease over time for a country.
        '''
        async with ctx.typing():
            await ctx.send(**embeds.country_history(country))

    @commands.command(brief='View stats by country.')
    async def countries(self, ctx):
        '''See various stats by country.
        '''
        async with ctx.typing():
            await ctx.send(**embeds.by_country())

    @commands.command(brief='Current USA stats.')
    async def usa(self, ctx):
        '''See various stats for the USA.
        '''
        await ctx.send(**embeds.usa())

    @commands.command(brief='See initial USA cases.')
    async def cases(self, ctx):
        '''See the first 19 USA cases.
        '''
        async with ctx.typing():
            await ctx.send(**embeds.by_state())

    @commands.command(brief="Check a country's stats.")
    async def country(self, ctx, *, country):
        '''See current stats for a country.
        '''
        async with ctx.typing():
            await ctx.send(**embeds.country_latest(country))

    @commands.command(brief='View world stats.')
    async def world(self, ctx):
        '''Check global stats.
        '''
        async with ctx.typing():
            await ctx.send(**embeds.world())
