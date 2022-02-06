import asyncio
import os

from character import Character
from game import Game
from server import Server


async def select_server(game, key):
    return [server for server in game.servers if server.get("key") == key][0]


async def select_characters(game, name):
    return [
        character
        for character in game.characters
        if character.get("name") == name
    ][0]


async def main():
    game = Game()
    email = os.environ["EMAIL"]
    password = os.environ["PASSWORD"]
    print(email)
    session_data = await game.get_session(email, password)
    print(session_data)
    await game.set_servers_and_characters()
    server_attributes = await select_server(game, "EUI")
    server = Server(**server_attributes)
    server_uri = server.uri
    print(server_uri)
    character_attributes = await select_characters(game, "BjornOak")
    character_attributes["in_map"] = character_attributes.pop("in")
    character = Character(**character_attributes)
    print(character.name)
    await asyncio.sleep(3)
    # Connect Character
    logout_response = await game.logout_everywhere()
    print(logout_response)


asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(main())
