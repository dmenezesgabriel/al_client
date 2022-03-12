import logging

import socketio

logger = logging.getLogger("alclient.observer")


class Observer:
    """
    Connect to websocket and listen/emit to events.
    """

    socket = socketio.AsyncClient(logger=False)

    def __init__(self) -> None:
        pass

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
            await self.socket.sleep(1.2)

    async def connect(self, address):
        await self.callbacks()
        logger.info("Connecting Socket")
        await self.socket.connect(address)
        logger.info(f"SID {self.socket.sid}")

    async def stop(self):
        logger.info("Disconnecting Socket")
        await self.socket.disconnect()
