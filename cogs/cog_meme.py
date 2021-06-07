from discord.ext import commands, slash
import random


class CogMeme(commands.Cog):
    def __init__(self, client):
        self.client = client

        @self.client.slash_cmd(name='amogustid')
        async def cmd_amogustid(ctx: slash.Context):
            """Checks if it is Amogus time."""
            await ctx.respond('Nej Victor, det er ikke Amogus tid 😐.')

        @self.client.slash_cmd(name='obamapic')
        async def cmd_obamapic(ctx: slash.Context):
            """Sends a picture of obama."""
            pictures = [
                'https://upload.wikimedia.org/wikipedia/commons/8/8d/President_Barack_Obama.jpg',
                'https://veja.abril.com.br/wp-content/uploads/2016/05/alx_mundo-obama-jantar-correspondentes-20160501-001_original.jpeg',
                'https://veja.abril.com.br/wp-content/uploads/2016/05/posse-presidencial-barack-obama-20130120-0597-original1.jpeg',
                'http://www.entrevistanews.com.br/fotos/noticias/3795_0.jpg',
                'https://www.hoganassessments.com/wp-content/uploads/2018/06/image-2953-640_panofree-rejo-2953.jpg',
                'https://pbs.twimg.com/media/ETAi5IJXkAA7mre.jpg',
                'https://web.static-rmg.be/if/c_crop,w_1200,h_800,x_0,y_0,g_center/c_fit,w_940,h_626/4e6d1d9cbd872048d3c7256dc6cb005c.jpg',
                'https://image.gala.de/22417082/t/JJ/v4/w1440/r1.5/-/barack-obama.jpg',
                'https://foreignpolicy.com/wp-content/uploads/2015/04/120688369.jpg?w=800&h=609&quality=90',
            ]
            await ctx.respond('{}'.format(random.choice(pictures)))

        @self.client.slash_cmd(name='dreampic')
        async def cmd_dreampic(ctx: slash.Context):
            """Sends a picture of the king."""
            pictures = [
                'https://www.elecspo.com/static/uploads/13/2021/04/Dream-phone-number.jpg',
                'https://1.bp.blogspot.com/-GWU_W1JFrA8/X4MJehAs_fI/AAAAAAAAD18/pXT8YkohglQW8XUeUgvHEk-x6w1OC-jDgCLcBGAsYHQ/s900/Dream%2B%2528YouTuber%2529.webp',
                'https://static.wikia.nocookie.net/youtube/images/9/99/DreamMask.jpg/revision/latest?cb=20210505061253',
                'https://i.pinimg.com/736x/1d/a5/04/1da504e860d05745e1481400ab5afde3.jpg',
                'https://i.scdn.co/image/521ef38618ac1b1b67c2e341575c4d1eade1036b',
                'https://brhscatseyeview.org/wp-content/uploads/2021/03/pasted-image-0-8-e1617030814627.png',
                'https://www.ginx.tv/uploads/DreamMilestoneMain.jpg',
                'https://i.pinimg.com/originals/7b/ae/df/7baedfb0a2a9c2766849f23100b59bc3.jpg',
            ]
            await ctx.respond('{}'.format(random.choice(pictures)))


def setup(client):
    client.add_cog(CogMeme(client))
