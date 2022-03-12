import logging

from alclient.observer import Observer

logger = logging.getLogger("alclient.character")


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
        server=None,
        secret=None,
        session=None,
        user_id=None,
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
        self.server = server
        self.secret = secret
        self._session = session
        self._user_id = user_id

    @property
    def session(self):
        return self._session

    @session.setter
    def session(self, session):
        self._session = session

    @property
    def user_id(self):
        return self._user_id

    @user_id.setter
    def user_id(self, user_id):
        self._user_id = user_id

    async def callbacks(self):
        @self.socket.event
        def connect():
            logger.info("Socket Connected")

        @self.socket.event
        async def disconnect():
            logger.info("Socket connection closed")

        @self.socket.event
        async def welcome(data):
            logger.info("Welcome received")
            await self.socket.emit(
                "loaded",
                {"height": 1080, "width": 1920, "scale": 2, "success": 1},
            )
            await self.socket.emit(
                "auth",
                {
                    "auth": self.session,
                    "character": self.id,
                    "height": 1080,
                    "no_graphics": "True",
                    "no_html": "1",
                    "passphrase": "",
                    "scale": 2,
                    "user": self.user_id,
                    "width": 1920,
                },
            )
            await self.socket.sleep(1.2)

        @self.socket.event
        async def entities(data):
            # logger.debug(f"Entities data: {data}")
            if "players" in data:
                pass

        @self.socket.event
        async def hit(data):
            # logger.debug(f"Hit data: {data}")
            pass

        @self.socket.event
        async def death(data):
            # logger.debug(f"Death data: {data}")
            pass

        @self.socket.event
        async def action(data):
            # logger.debug(f"Action data: {data}")
            pass

    async def connect(self, address):
        await self.callbacks()
        logger.info("Connecting Socket")
        await self.socket.connect(address)
        logger.info(f"SID {self.socket.sid}")
