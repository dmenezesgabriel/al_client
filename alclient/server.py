class Server:
    """
    Game server class.
    """

    def __init__(
        self,
        name,
        region,
        players,
        key,
        port,
        addr,
    ) -> None:
        self.name = name
        self.region = region
        self.players = players
        self.key = key
        self.port = port
        self.addr = addr

    @property
    def uri(self):
        return f"wss://{self.addr}:{self.port}"
