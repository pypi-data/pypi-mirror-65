import asyncio
import logging

import discord
import a2s

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('conan-bot')

from conan_bot.config import config

if config['bot'].getboolean('debug', fallback=False):
    logging.basicConfig(level=logging.DEBUG)

TOKEN = config.get('discord', 'token')
address = (config.get('server', 'ip'), config.getint('server', 'port'))
name = config.get('server', 'name')
status_channel = config.getint('discord', 'channel')


async def async_a2s_info(addr):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, a2s.info, addr)


class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # create the background task and run it in the background
        self.bg_task = self.loop.create_task(self.my_background_task())

    async def on_ready(self):
        logger.info(f'Logged in as {self.user.name} {self.user.id} starting updates')
        activity = discord.Activity(name=name, type=discord.ActivityType.watching)
        await self.change_presence(activity=activity)

    async def my_background_task(self):
        await self.wait_until_ready()
        channel = self.get_channel(status_channel)
        while not self.is_closed():
            i = await async_a2s_info(address)
            await discord.VoiceChannel.edit(channel, name=f"Online Players : {i.player_count} / {i.max_players}")
            await asyncio.sleep(60)  # task runs every 60 seconds


def main():
    client = MyClient()
    client.run(TOKEN)


if __name__ == "__main__":
    main()
