import discord
from discord.ext import commands, slash
import methods
from replit import db


class CogCreator(commands.Cog):
    def __init__(self, client):
        self.client = client

        @self.client.slash_group()
        async def database(ctx: slash.Context):
            """Creator commands."""
            print('Options:', ctx.options)

        @database.check
        async def database_check(ctx: slash.Context):
            if methods.is_creator(ctx.author):
                return True
            else:
                await ctx.respond(embeds=[
                    discord.Embed(title='Not the creator!', color=0xff0000)
                ])
                return False

        @database.slash_cmd(name='clear')
        async def cmd_database_clear(ctx: slash.Context):
            """Clears the entire database."""
            db.clear()
            methods.check_database()
            await ctx.respond('Cleared the database.')

        @database.slash_cmd(name='print')
        async def cmd_database_user(ctx: slash.Context):
            """Shows the entire database."""
            methods.check_database()
            message = ''
            for k in db:
                message += '{} - {}\n'.format(k, db[str(k)])

            print('Database:')
            for key in db:
                if key == 'guilds':
                    print(' - Guilds:')
                    for guild_id in db['guilds']:
                        guild = client.get_guild(int(guild_id))
                        print('    - {} : ID {}'.format(guild.name, guild_id))
                        print('      - Users:')
                        for user_id in db['guilds'][guild_id]['users']:
                            print('        - {} : ID {}'.format(
                                'user.name', user_id))
                            print('          - {}'.format(
                                db['guilds'][guild_id]['users'][str(user_id)]))
                else:
                    print(' - {} : {}'.format(key, db[key]))

            await ctx.respond(message)

        @database.slash_cmd(name='user')
        async def cmd_database_user(
            ctx: slash.Context,
            user: slash.Option(
                description='A user',
                type=slash.ApplicationCommandOptionType.USER) = None):
            """Get a members userdata."""
            if user == None:
                user = ctx.author

            methods.check_user(user)
            await ctx.respond(methods.get_userdata(user))


def setup(client):
    client.add_cog(CogCreator(client))
