import logging

from alclient.character import Character
from alclient.server import Server
from alclient.user.user import User

logger = logging.getLogger("adventure_land.game")


class Game:
    def __init__(self, user: User):
        self.user = user

    def select_server(self, key: str) -> Server:
        """
        Server factory.
        """
        logger.info(f"Selecting server {key}")
        server_attributes = [
            server for server in self.user.servers if server.get("key") == key
        ]
        if server_attributes:
            return Server(**server_attributes[0])

    def select_characters(self, name: str) -> Character:
        """
        Character factory.
        """
        logger.info(f"Selecting character {name}")
        character_attributes = [
            character
            for character in self.user.characters
            if character.get("name") == name
        ]
        if character_attributes:
            character_attributes[0]["in_map"] = character_attributes[0].pop(
                "in"
            )
            return Character(**character_attributes[0])
