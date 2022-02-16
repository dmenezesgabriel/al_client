import asyncio
import logging
import os
import sys

from game import Game
from log import setup_loggers
from login import LoginFacade
from user import User

logger = logging.getLogger("adventure_land")


async def main():
    setup_loggers()
    email = os.environ["EMAIL"]
    password = os.environ["PASSWORD"]
    user = User(email, password)
    print(user.email)
    await LoginFacade.loginApi(user)
    await user.post_code("./code/test.js", "2", "test_post_code")
    game = Game(user)
    server = game.select_server("EUI")
    character = game.select_characters("BjornOak")
    print(character.name)
    # Connect Character
    await character.connect(server.uri)
    await asyncio.sleep(3)
    await character.stop()
    logout_response = await user.logout_everywhere()
    print(logout_response)


if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
