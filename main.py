import os
import logging
import discord
from discord.ext import slash
from keep_alive import keep_alive
import methods
from settings import SETTINGS
import datetime
from replit import db

#Variables
client = slash.SlashBot(
    command_prefix='/',
    description='A custom Discord bot.',
    help_command=None,
    debug_guild=int(os.environ.get('DISCORD_DEBUG_GUILD', 0)) or None,
    resolve_not_fetch=False,
    fetch_if_not_get=True)


# Client events
@client.event
async def on_ready():
    print('\nStarting the bot')
    print(' * Validating database')
    methods.check_database()

    await client.change_presence(status=discord.Status.online,
                                 activity=discord.Game(name=str(
                                     db['bot_status']),
                                                       type=3))
    
    # Load extensions
    print(' * Loading cog extensions')
    for extension in SETTINGS['EXTENSIONS']:
        client.load_extension('cogs.{}'.format(extension))
        print('   * {}'.format(extension))

    print(' * The bot is now ready\n')


@client.event
async def on_slash_permissions():
    await client.register_permissions()
    print(' * Registered permissions\n')


@client.event
async def on_message(message):
    # Earn currency from chatting
    if not message.author.bot:
        methods.check_user(message.author)
        userdata = methods.get_userdata(message.author)

        # Reset money earnings
        if userdata['money_earn_count'] >= SETTINGS[
                'MAX_MONEY_EARNING'] and datetime.datetime.now().strftime(
                    "%m/%d/%Y") != userdata['money_earn_date']:
            userdata['money_earn_count'] = 0
            methods.save_userdata(message.author, userdata)

        if not message.content.startswith(SETTINGS['PREFIX']):
            # Level system
            time_string = datetime.datetime.now().strftime("%H/%M/%S")
            if time_string != userdata['xp_earn']:
                userdata['experience'] += 1
                userdata['xp_earn'] = time_string
                if userdata['experience'] >= userdata['level'] * SETTINGS[
                        'XP_MULTIPLIER']:
                    userdata['experience'] -= userdata['level'] * SETTINGS[
                        'XP_MULTIPLIER']
                    userdata['level'] += 1

            # Money system
            if userdata['money_earn_count'] < SETTINGS[
                    'MAX_MONEY_EARNING'] and userdata[
                        'wallet'] + 1 <= userdata['wallet_size']:
                userdata['wallet'] += 1
                userdata['money_earn_count'] += 1
                userdata['money_earn_date'] = datetime.datetime.now().strftime(
                    "%m/%d/%Y")
                methods.save_userdata(message.author, userdata)


# show extension logs
if SETTINGS['DEBUG']:
    logger = logging.getLogger('discord.ext.slash')
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())

try:
    keep_alive()
    client.run(os.environ['TOKEN'])
finally:
    print('Goodbye.')
