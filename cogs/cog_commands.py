import os
import logging
import discord
from discord.ext import commands, slash
from keep_alive import keep_alive
import random
import methods
from settings import SETTINGS
import datetime
from replit import db
#from discordTogether import DiscordTogether


class CogCommands(commands.Cog):
    def __init__(self, client):
        self.client = client
        #together_controls = DiscordTogether(client)

        @self.client.slash_cmd(name='hack')
        async def cmd_hack(ctx: slash.Context, user: slash.Option(
            description='A user',
            required=True,
            type=slash.ApplicationCommandOptionType.USER)):
            """Hack a persons computer."""
            action = random.choice([
                'Hacked ip', 'Destroyed router', 'Inserted Amogus',
                'Downloaded mod', 'Snipped wires', 'Hacked router',
                'Deleted homework_folder', 'Deleted System32', 'Inserted sus'
            ])
            await ctx.respond('Hacked {}, {}'.format(user, action))

        @self.client.slash_cmd(name='roll')
        async def cmd_roll(
            ctx: slash.Context,
            sides: slash.Option(
                description='Dice sides',
                type=slash.ApplicationCommandOptionType.INTEGER) = 6):
            """Roll a dice."""
            await ctx.respond('Rolled: {}'.format(random.randint(1, sides)))

        @self.client.slash_cmd(name='test')
        async def cmd_test(
            ctx: slash.Context,
            user: slash.Option(
                description='A user',
                type=slash.ApplicationCommandOptionType.USER) = None):
            """Corona test."""
            if user == None:
                user = ctx.author
            await ctx.respond('{} tested {} for corona'.format(
                user, random.choice(['negative', 'positive'])))

        @self.client.slash_cmd(name='match')
        async def cmd_match(
            ctx: slash.Context,
            user1: slash.Option(description='A user',
                                required=True,
                                type=slash.ApplicationCommandOptionType.USER),
            user2: slash.Option(description='A user',
                                required=True,
                                type=slash.ApplicationCommandOptionType.USER)):
            """Test a match."""
            await ctx.respond('= {}% match'.format(random.randint(0, 100)))

        @self.client.slash_cmd(name='flip')
        async def cmd_flip(ctx: slash.Context):
            """Flip a coin."""
            await ctx.respond('Coin landed on **{}**'.format(
                random.choice(['heads', 'tails'])))

        @self.client.slash_cmd(name='8ball')
        async def cmd_8ball(ctx: slash.Context, question: slash.Option(
            description='Question to ask', required=True)):
            """Get the answer to a question."""
            await ctx.respond(
                random.choice([
                    'It is certain',
                    'It is decidedly so',
                    'Without a doubt',
                    'Yes, definitely',
                    'You may rely on it',
                    'As I see it, yes',
                    'Most likely',
                    'Outlook good',
                    'Yes',
                    'No',
                    'Signs point to yes',
                    'Reply hazy try again',
                    'Ask again later',
                    'Better not tell you now',
                    'Cannot predict now',
                    'Concentrate and ask again',
                    'Don\'t count on it',
                    'My reply is no',
                    'My sources say no',
                    'Outlook not so good',
                    'Very doubtful',
                ]))

        @self.client.slash_cmd(name='mock')
        async def cmd_mock(ctx: slash.Context,
                           text: slash.Option(description='Text to convert',
                                              required=True)):
            """Convert to mocking text."""
            text = ' '.join(text)
            text = text.lower()
            new_text = ''
            for c in text:
                if random.choice([True, False]):
                    new_text += c.upper()
                else:
                    new_text += c
            await ctx.respond(new_text)

        @self.client.slash_cmd(name='roulette')
        async def cmd_roulette(ctx: slash.Context):
            """Try your luck."""
            if random.randint(1, 6) == 6:
                await ctx.respond('Bang! You died :(')
            else:
                await ctx.respond('You get to live!')

        # Party
        @self.client.slash_group()
        async def party(ctx: slash.Context):
            """Party commands."""
            print('Options:', ctx.options)
        
        #@party.slash_cmd(name='youtube')
        #async def cmd_party_youtube(ctx: slash.Context):
            """Create a youtube party."""
            #link = together_controls.create_link(ctx.author.voice.channel.id, 'youtube')
            #await ctx.respond(f"Click the blue link!\n{link}")

        #@party.slash_cmd(name='other')
        #async def cmd_party_other(ctx: slash.Context, activity: slash.Option(description='Activity', required=True, choices=['youtube', 'poker', 'chess', #'betrayal', 'fishing'])):
            #"""Create a discord party."""
            #link = together_controls.create_link(ctx.author.voice.channel.id, activity)
            #await ctx.respond(f"Click the blue link!\n{link}")

        # Level
        @self.client.slash_cmd(name='level')
        async def cmd_level(
            ctx: slash.Context,
            user: slash.Option(
                description='A user',
                type=slash.ApplicationCommandOptionType.USER) = None):
            """Get a users level."""
            if user == None:
                user = ctx.author
            methods.check_user(user)
            userdata = methods.get_userdata(user)
            user_level = userdata['level']
            user_experience = userdata['experience']
            user_needed_experience = user_level * SETTINGS['XP_MULTIPLIER']
            embed = discord.Embed(title=f"{user.name}'s level",
                                  color=discord.Color.greyple())
            embed.set_thumbnail(url=user.avatar_url)
            embed.add_field(name='Level', value='{}'.format(user_level))
            embed.add_field(name='Experience',
                            value='{}/{}'.format(user_experience,
                                                 user_needed_experience))
            await ctx.respond(embed=embed)

        # Roles
        @self.client.slash_group()
        async def role(ctx: slash.Context):
            """Role commands."""
            print('Options:', ctx.options)

        role_opt = slash.Option(description='Account',
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


def setup(client):
    client.add_cog(CogCommands(client))
