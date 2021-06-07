import os
from replit import db
from settings import SETTINGS
import discord


def add_balance(user, amount):
    check_user(user)
    userdata = get_userdata(user)
    userdata['wallet'] += amount
    if userdata['wallet'] > userdata['wallet_size']:
        userdata['wallet'] = userdata['wallet_size']
    elif userdata['wallet'] < 0:
        userdata['wallet'] = 0
    save_userdata(user, userdata)


def send_money(user1, user2, amount):
    if user1 != user2:
        check_users(user1, user2)
        userdata1 = get_userdata(user1)
        userdata2 = get_userdata(user2)

        if userdata1['wallet'] >= amount:
            if userdata2['wallet'] + amount < userdata2['wallet_size']:
                userdata1['wallet'] -= amount
                userdata2['wallet'] += amount
                save_userdata(user1, userdata1)
                save_userdata(user2, userdata2)
                return '{} send {}{} to {}'.format(user1.name, amount,
                                                   SETTINGS['CURRENCY_SYMBOL'], user2.name)
            else:
                return 'The receiver does not have enough room in their wallet!'
        else:
            return 'Error: You do not have {} in your wallet!'.format(amount)
    else:
        return 'Error: You can not send money to your self!'


def check_user(user):
    # Check guild
    if str(user.guild.id) not in db['guilds'].keys():
        print('Created default guild : {}'.format(user.guild.name))
        db['guilds'][str(user.guild.id)] = guilddata_default()

    # Create guild userdata
    if str(user.id) not in db['guilds'][str(user.guild.id)]['users'].keys():
        print('Created default user : {}'.format(user.name))
        save_userdata(user, userdata_default())


def check_users(*users: discord.user):
    for user in users:
        check_user(user)


def guilddata_default():
    return {
        'users': {},
    }


def userdata_default():
    return {
        'wallet': 0,
        'wallet_size': 500,
        'bank': 0,
        'bank_size': 1000,
        'money_earn_count': 0,
        'money_earn_date': '',
        'xp_earn': '',
        'level': 1,
        'experience': 0,
    }


def save_userdata(user, userdata):
    print('Saved userdata : {}'.format(user.name))
    db['guilds'][str(user.guild.id)]['users'][str(user.id)] = userdata


def get_userdata(user):
    return db['guilds'][str(user.guild.id)]['users'][str(user.id)]


def is_creator(user):
    return str(user.id) == os.environ['ID_CREATOR']


def get_log_channel(bot):
    return bot.get_channel(int(os.environ['LOG_CHANNEL']))


async def achievement(bot, user, role_name):
    role = discord.utils.get(user.guild.roles, name=role_name)
    await user.add_roles(role)


def check_database():
    if 'bot_status' not in db:
        db['bot_status'] = '/bot status'

    if 'guilds' not in db:
        db['guilds'] = {}
