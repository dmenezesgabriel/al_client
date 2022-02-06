import asyncio
import logging
import os

from game import Game
from log import setup_loggers
from user import User

logger = logging.getLogger("adventure_land")


async def main():
    setup_loggers()
    email = os.environ["EMAIL"]
    password = os.environ["PASSWORD"]
    user = User(email, password)
    print(user.email)
    await user.login()
    game = Game(user)
    server = game.select_server("EUI")
    print(server.uri)
    character = game.select_characters("BjornOak")
    print(character.name)
    await asyncio.sleep(3)
    # Connect Character
    logout_response = await user.logout_everywhere()
    print(logout_response)


asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(main())
