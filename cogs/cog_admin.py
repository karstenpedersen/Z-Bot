import discord
from discord.ext import commands, slash
import methods


class CogAdmin(commands.Cog):
    def __init__(self, client):
        self.client = client

        @self.client.slash_group()
        async def admin(ctx: slash.Context):
            """Admin commands."""
            print('Options:', ctx.options)

        @admin.check
        async def admin_check(ctx: slash.Context):
            if methods.is_creator(ctx.author):
                return True
            else:
                await ctx.respond(embeds=[
                    discord.Embed(title='Not an admin!', color=0xff0000)
                ])
                return False

        @admin.slash_cmd(name='purge')
        async def cmd_purge(ctx: slash.Context, amount: slash.Option(
            description='Amount',
            type=slash.ApplicationCommandOptionType.INTEGER)):
            """Delete messages."""
            await ctx.channel.purge(limit=amount)
            await ctx.respond('Purged {} messages in {}'.format(
                amount, ctx.channel))


def setup(client):
    client.add_cog(CogAdmin(client))
