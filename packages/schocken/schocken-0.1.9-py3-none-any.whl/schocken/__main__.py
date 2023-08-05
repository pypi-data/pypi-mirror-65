import os

import discord
from discord.utils import get
from dotenv import load_dotenv

from schocken import __version__
from schocken.exceptions import FalscherServer
from schocken.bot import SchockenBot


def run_bot():
    load_dotenv()
    TOKEN = os.getenv("DISCORD_TOKEN")
    GUILD = os.getenv("DISCORD_GUILD")
    client = discord.Client()

    # when connecting
    @client.event
    async def on_ready():
        client.bot = SchockenBot(client)
        # check if server is correct:
        for guild in client.guilds:
            if guild.name != client.bot.valid_guild_name:
                raise FalscherServer("Dieser Bot darf nur ins Café A")

        ch = client.get_channel(690929770355097610)  # schocktresen
        await ch.send(f"Schocken (v{__version__}) kann jetzt losgehen. :muscle:")
        print("Success")
        return

    # when a message is read by the bot
    @client.event
    async def on_message(message):
        await client.bot.parse_input(message)
        return

    @client.event
    async def on_error(error, *args, **kwargs):
        import traceback

        ch = client.get_channel(694603857950539887)  # errorland
        trace = traceback.format_exc()
        await ch.send(f"Error: {error}({args}, {kwargs})\n```\n{trace}\n```")
        return

    client.run(TOKEN)


if __name__ == "__main__":
    run_bot()
