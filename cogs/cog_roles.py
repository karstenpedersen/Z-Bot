import discord
from discord.ext import commands, slash
from settings import SETTINGS


class CogRole(commands.Cog):
    def __init__(self, client):
        self.client = client

        @self.client.slash_group()
        async def role(ctx: slash.Context):
            """Role commands."""
            print('Options:', ctx.options)

        role_opt = slash.Option(description='Role',
                                required=True,
                                choices=SETTINGS['JOINABLE_ROLES'])

        @role.slash_cmd(name='join')
        async def cmd_role_join(ctx: slash.Context, role_name: role_opt):
            """Join a joinable role."""

            role = discord.utils.get(ctx.author.guild.roles, name=role_name)

            if role not in ctx.author.roles:
                await ctx.author.add_roles(role)
                await ctx.respond('{} joined "{}"'.format(
                    ctx.author, role_name))
            else:
                await ctx.respond('You already have the role.'.format(
                    ctx.author, role_name))

        @role.slash_cmd(name='leave')
        async def cmd_role_leave(ctx: slash.Context, role_name: role_opt):
            """Leave a joinable role."""

            role = discord.utils.get(ctx.author.guild.roles, name=role_name)

            if role in ctx.author.roles:
                await ctx.author.remove_roles(role)
                await ctx.respond('{} leaved "{}"'.format(
                    ctx.author, role_name))
            else:
                await ctx.respond('You already don\'t have the role.'.format(
                    ctx.author, role_name))
        
        @role.slash_cmd(name='create')
        async def cmd_role_create(ctx: slash.Context, role_name: slash.Option(description='Name', required=True)):
            """Create a new role."""
            await ctx.guild.create_role(name=role_name)
            await ctx.respond('Created role "{}"'.format(role_name))

        @role.slash_cmd(name='delete')
        async def cmd_role_delete(ctx: slash.Context, role_id: slash.Option(description='Name', required=True)):
            """Delete a role."""
            #await ctx.guild.delete_roll()
            await ctx.respond('Not working!')


def setup(client):
    client.add_cog(CogRole(client))