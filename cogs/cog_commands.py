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
from discordTogether import DiscordTogether


class CogCommands(commands.Cog):
    def __init__(self, client):
        self.client = client
        together_controls = DiscordTogether(client)

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
        
        @party.slash_cmd(name='youtube')
        async def cmd_party_youtube(ctx: slash.Context):
            """Create a youtube party."""
            link = together_controls.create_link(ctx.author.voice.channel.id, 'youtube')
            await ctx.respond(f"Click the blue link!\n{link}")

        @party.slash_cmd(name='other')
        async def cmd_party_other(ctx: slash.Context, activity: slash.Option(description='Activity', required=True, choices=['youtube', 'poker', 'chess', 'betrayal', 'fishing'])):
            """Create a discord party."""
            link = together_controls.create_link(ctx.author.voice.channel.id, activity)
            await ctx.respond(f"Click the blue link!\n{link}")

        
        @self.client.slash_cmd(name='poll')
        async def cmd_poll(ctx: slash.Context, question: slash.Option(description='Question', required=True), 
        option1: slash.Option(description='Answer', required=True) = '',
        option2: slash.Option(description='Answer', required=True) = '',
        option3: slash.Option(description='Answer') = '',
        option4: slash.Option(description='Answer') = '',
        option5: slash.Option(description='Answer') = '',
        option6: slash.Option(description='Answer') = '',
        option7: slash.Option(description='Answer') = '',
        option8: slash.Option(description='Answer') = '',
        option9: slash.Option(description='Answer') = ''):
            """Create a poll."""

            emojis = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣']

            options = []
            if option1 != '':
                options.append(option1)
            if option2 != '':
                options.append(option2)
            if option3 != '':
                options.append(option3)
            if option4 != '':
                options.append(option4)
            if option5 != '':
                options.append(option5)
            if option6 != '':
                options.append(option6)
            if option7 != '':
                options.append(option7)
            if option8 != '':
                options.append(option8)
            if option9 != '':
                options.append(option9)

            if len(options) > 1:
                if len(options) <= 9:
                    embed = discord.Embed(title=question, color=discord.Color.blurple())
                    embed.set_thumbnail(url=ctx.author.avatar_url)
                    embed.set_footer(text='Poll by {}'.format(ctx.author.name))
                    for i in range(len(options)):
                        embed.add_field(name=options[i], value=emojis[i])
                    
                    await ctx.respond('Created poll!', ephemeral=True)

                    message = await ctx.send(embed=embed) 

                    for i in range(len(options)):
                        await message.add_reaction(emojis[i])
                else:
                    await ctx.respond('To many options!', ephemeral=True)
            else:
                await ctx.respond('You need atleast two options!', ephemeral=True)


def setup(client):
    client.add_cog(CogCommands(client))
