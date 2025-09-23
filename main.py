import os

import discord

from client import Client


def main() -> None:
    intents = discord.Intents().default()
    intents.message_content = True

    client = Client(intents=intents)
    client.run(os.environ["BOT_TOKEN"])


if __name__ == "__main__":
    main()  # pragma: no cover
