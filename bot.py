import logging
from discord.ext import commands
import discord

from config import TOKEN
from cog import Stats


class Help(commands.DefaultHelpCommand):
    brief = 'Shows this message.'
    help = 'Provides help on a command.'

    async def send_bot_help(self, cogs):
        text = ''
        for cog in cogs:
            for command in cogs[cog]:
                text += '**{}**   *{}*\n'.format(
                    self.get_command_signature(command),
                    command.brief or Help.brief
                )
        e = discord.Embed(title='Help', color=0x00FF00, description=text)
        await self.get_destination().send(embed=e)

    async def send_command_help(self, command):
        desc = command.help or Help.help
        title = self.get_command_signature(command)
        e = discord.Embed(title=title, color=0x00FF00, description=desc)
        await self.get_destination().send(embed=e)

    async def send_cog_help(self, cog):
        await self.send_bot_help()


logging.basicConfig(level=logging.INFO)
bot = commands.Bot(command_prefix='**')
bot.add_cog(Stats())
bot.help_command = Help()


@bot.command(brief='Get the invite link.')
async def invite(ctx):
    '''Get the invite link to add the bot to another server.
    '''
    invite = (
        'https://discordapp.com/oauth2/authorize?client_id=691369979186249799'
        '&permissions=604359745&scope=bot'
    )
    e = discord.Embed(title='Invite', description=f'[Click here]({invite})')
    await ctx.send(embed=e)


@bot.command(brief='Basic bot info.')
async def about(ctx):
    '''Information about the bot.
    '''
    about = (
        'This bot was made by Artemis#8799 and provides graphs and stats for '
        'the novel Coronavirus (COVID-19).'
    )
    e = discord.Embed(title='About', description=about)
    e.add_field(
        name='Discord API ping', value=f'{str(bot.latency * 1000)[:3]}ms'
    )
    e.add_field(name='Servers', value=len(bot.guilds))
    e.add_field(name='Users', value=len(bot.users))
    await ctx.send(embed=e)


bot.run(TOKEN)