import logging
import os
import sys

import discord

from client import Client

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
    stream=sys.stdout,
)


def main() -> None:
    intents = discord.Intents().default()
    intents.message_content = True

    client = Client(intents=intents)
    client.run(os.environ["BOT_TOKEN"])


if __name__ == "__main__":
    main()  # pragma: no cover
