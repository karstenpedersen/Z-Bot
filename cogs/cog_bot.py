import discord
from discord.ext import commands, slash
from replit import db


class CogBot(commands.Cog):
    def __init__(self, client):
        self.client = client

        @self.client.slash_group()
        async def bot(ctx: slash.Context):
            """Bot commands."""
            print('Options:', ctx.options)

        @bot.slash_cmd(name='status')
        async def cmd_bot_status(ctx: slash.Context,
                                 status: slash.Option(description='New status',
                                                      required=True)):
            """Set the bots status."""
            if len(status) < 32:
                await client.change_presence(status=discord.Status.online,
                                             activity=discord.Game(name=status,
                                                                   type=3))
                await ctx.respond('Sat the bots status to "{}"'.format(status))
                db['bot_status'] = status
            else:
                await ctx.respond('Failed: Max length is 16 characters!')

        @bot.slash_cmd(name='info')
        async def cmd_bot_info(ctx: slash.Context):
            """Gets the bots status."""
            embed = discord.Embed(
                title=f'Z-bot',
                description=
                'Z-bot is an Discord bot that uses slash commands. Find more info here:\nhttps://github.com/karstenpedersen/z-bot',
                color=discord.Color.blurple())
            embed.set_thumbnail(url=client.user.avatar_url)
            embed.add_field(name='Profile status',
                            value=db['bot_status'],
                            inline=False)
            embed.add_field(name='Cogs', value=self.client.cogs, inline=False)
            embed.add_field(name='Extensions',
                            value=self.client.extensions,
                            inline=False)
            embed.add_field(name='Commands',
                            value=self.client.commands,
                            inline=False)
            await ctx.respond(embed=embed)


def setup(client):
    client.add_cog(CogBot(client))
