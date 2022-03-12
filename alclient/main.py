import asyncio
import logging
import os

from alclient.game import Game
from alclient.log import setup_loggers
from alclient.login.facade import LoginFacade
from alclient.user.user import User

logger = logging.getLogger("adventure_land")


async def main():
    setup_loggers()
    email = os.environ["EMAIL"]
    password = os.environ["PASSWORD"]
    user = User(email, password)
    print(user.email)
    login_facade = LoginFacade()
    await login_facade.login_api(user)
    # await user.post_code("./code/hello.js", "2", "test_post_code")
    game = Game(user)
    server = game.select_server("EUI")
    character = game.select_characters("BjornOak")
    character.session = user.session
    character.user_id = user.id
    print(character.name)
    # Connect Character
    await character.connect(server.uri)
    await asyncio.sleep(20)
    await character.stop()
    logout_response = await user.logout_everywhere()
    print(logout_response)
