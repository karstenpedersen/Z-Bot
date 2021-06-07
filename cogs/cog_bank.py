import discord
from discord.ext import commands, slash
import methods


class CogBank(commands.Cog):
    def __init__(self, client):
        self.client = client

        @self.client.slash_group()
        async def bank(ctx: slash.Context):
            """Bank commands."""
            print('Options:', ctx.options)

        @bank.slash_cmd(name='balance')
        async def cmd_bank_balance(
            ctx: slash.Context,
            user: slash.Option(
                description='A user',
                type=slash.ApplicationCommandOptionType.USER) = None):
            """Check balance."""
            if user == None:
                user = ctx.author
            methods.check_user(user)
            userdata = methods.get_userdata(user)

            user_wallet = userdata['wallet']
            user_wallet_size = userdata['wallet_size']
            user_bank = userdata['bank']
            user_bank_size = userdata['bank_size']
            embed = discord.Embed(title=f"{user.name}'s balance",
                                  color=discord.Color.blurple())
            embed.set_thumbnail(url=user.avatar_url)
            embed.add_field(name='Wallet',
                            value='{}/{}'.format(user_wallet,
                                                 user_wallet_size))
            embed.add_field(name='Bank',
                            value='{}/{}'.format(user_bank, user_bank_size))
            await ctx.respond(embed=embed)

        @bank.slash_cmd(name='send')
        async def cmd_bank_send(
            ctx: slash.Context,
            user: slash.Option(description='A user',
                               required=True,
                               type=slash.ApplicationCommandOptionType.USER),
            amount: slash.Option(
                description='Amount',
                type=slash.ApplicationCommandOptionType.INTEGER)):
            """Send z's to a person."""
            await ctx.respond(methods.send_money(ctx.author, user, amount))

        @bank.slash_cmd(name='tip')
        async def cmd_bank_tip(ctx: slash.Context, user: slash.Option(
            description='A user',
            required=True,
            type=slash.ApplicationCommandOptionType.USER)):
            """Tip a person 1z."""
            await ctx.respond(methods.send_money(ctx.author, user, 1))

        @bank.slash_cmd(name='transfer')
        async def cmd_bank_transfer(ctx: slash.Context, amount: slash.Option(
            description='Amount',
            type=slash.ApplicationCommandOptionType.INTEGER),
                                    account: slash.Option(
                                        description='Account',
                                        required=True,
                                        choices=['bank', 'wallet'])):
            """Transfer money between accounts."""
            methods.check_user(ctx.author)
            userdata = methods.get_userdata(ctx.author)
            message = ''

            if 'bank'.startswith(account):
                if userdata['wallet'] >= amount:
                    if userdata['bank'] + amount > userdata['bank_size']:
                        amount = userdata['bank_size'] - userdata['bank']

                    userdata['wallet'] -= amount
                    userdata['bank'] += amount

                    if amount == 1:
                        message = f'Transferred {amount} to bank'
                    else:
                        message = f'Transferred {amount} z\'s to bank'
                else:
                    await ctx.respond(
                        'Error: Not enough money. You tried to send {}, you have {}'
                        .format(amount, userdata['wallet']))
            elif 'wallet'.startswith(account):
                if userdata['bank'] >= amount:
                    if userdata['wallet'] + amount > userdata['wallet_size']:
                        amount = userdata['wallet_size'] - userdata['wallet']

                    userdata['wallet'] += amount
                    userdata['bank'] -= amount

                    if amount == 1:
                        message = f'Transferred {amount} to bank'
                    else:
                        message = f'Transferred {amount} z\'s to bank'
                else:
                    await ctx.respond(
                        'Error: Not enough money. You tried to send {}, you have {}'
                        .format(amount, userdata['bank']))

            embed = discord.Embed(title=f"{ctx.author.name}'s balance",
                                  color=discord.Color.blurple())
            embed.set_thumbnail(url=ctx.author.avatar_url)
            embed.add_field(name='Transfer', value=message, inline=False)
            embed.add_field(name='Wallet',
                            value='{}/{}'.format(userdata['wallet'],
                                                 userdata['wallet_size']))
            embed.add_field(name='Bank',
                            value='{}/{}'.format(userdata['bank'],
                                                 userdata['bank_size']))
            await ctx.respond(embed=embed)


def setup(client):
    client.add_cog(CogBank(client))
