import logging
import os
import sys

import discord

from announcement import AnnouncementClient

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
    stream=sys.stdout,
)


def announcement() -> None:
    client = AnnouncementClient(intents=discord.Intents().default())
    client.run(os.environ["BOT_TOKEN"])


if __name__ == "__main__":
    announcement()  # pragma: no cover
