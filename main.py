import asyncio
import os

import socketio

from game import Game

sio = socketio.AsyncClient(logger=True)


@sio.event
def connect():
    print("Connected")


@sio.event
async def disconnect():
    print("connection closed")


@sio.event
async def welcome(data):
    await sio.emit(
        "loaded", {"height": 1080, "width": 1920, "scale": 2, "success": 1}
    )
    await sio.sleep(1.2)
    await sio.disconnect()


async def select_server(game, key):
    return [server for server in game.servers if server.get("key") == key][0]


async def build_server_uri(game, key):
    server = await select_server(game, key)
    return f"wss://{server['addr']}:{server['port']}"


async def select_characters(game, name):
    return [
        character
        for character in game.characters
        if character.get("name") == name
    ][0]


async def get_character_id(game, name):
    character = await select_characters(game, name)
    return character["id"]


async def main():
    # await sio.connect("wss://eud1.adventure.land:2053")
    # await sio.wait()
    game = Game()
    email = os.environ["EMAIL"]
    password = os.environ["PASSWORD"]
    print(email)
    session_data = await game.get_session(email, password)
    print(session_data)
    await game.set_servers_and_characters()
    server_uri = await build_server_uri(game, "EUI")
    print(server_uri)
    character_id = await get_character_id(game, "BjornOak")
    print(character_id)
    await asyncio.sleep(3)
    logout_response = await game.logout_everywhere()
    print(logout_response)


asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(main())
