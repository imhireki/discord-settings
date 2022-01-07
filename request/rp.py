import discord


token = ''

class MyClient(discord.Client):
    async def on_ready(self, *args, **kwargs):
        data = {'name': 'DOOM Emacs',
                'url': 'https://www.twitch.tv/xd'}

        _ = discord.Streaming(**data)

        await self.change_presence(activity=_)

c = MyClient()
c.run(token, bot=False)
