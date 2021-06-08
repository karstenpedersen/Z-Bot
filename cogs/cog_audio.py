import discord
from discord.ext import commands, slash
import methods


class CogAudio(commands.Cog):
    def __init__(self, client):
        self.client = client
        players = {}

        @self.client.slash_group()
        async def audio(ctx: slash.Context):
            """Audio commands."""
            print('Options:', ctx.options)

        @audio.check
        async def admin_check(ctx: slash.Context):
            return True
        
        @audio.slash_cmd(name='join')
        async def cmd_audio_join(ctx: slash.Context):
            """Make the bot join voice channel."""
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
                await ctx.respond('The bot joined', ephemeral=True)
            else:
                await ctx.respond('You need to be in a voice channel!', ephemeral=True)

        @audio.slash_cmd(name='leave')
        async def cmd_audio_leave(ctx: slash.Context):
            """Make the bot leave."""
            print(self.client.voice_clients)
            voice_client = self.client.voice_clients[0]
            await voice_client.disconnect()
            await ctx.respond('The bot left', ephemeral=True)
            #else:
            #    await ctx.respond('The bot is not in a channel!', ephemeral=True)

        @audio.slash_cmd(name='play')
        async def cmd_audio_add(ctx: slash.Context, url: slash.Option(description='Link')):
            """Add a video to the queue."""
            voice_client = self.client.voice_clients[0]
            player = await voice_client.create_ytdl_player(url)
            players[ctx.author.guild.id] = player
            player.start()

            #https://www.youtube.com/watch?v=MEg-oqI9qmw


def setup(client):
    client.add_cog(CogAudio(client))
