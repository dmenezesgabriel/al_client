import logging

from observer import Observer

logger = logging.getLogger("adventure_land.character")


class Character(Observer):
    def __init__(
        self,
        map,
        in_map,
        name,
        level,
        skin,
        cx,
        online,
        y,
        x,
        type,
        id,
    ) -> None:
        super().__init__()
        self.map = map
        self.in_map = in_map
        self.name = name
        self.level = level
        self.skin = skin
        self.cx = cx
        self.online = online
        self.y = y
        self.x = x
        self.type = type
        self.id = id
