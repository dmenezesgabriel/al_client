import logging

from alclient.login.login import Login
from alclient.user.user import User

logger = logging.getLogger("adventure_land.login_facade")


class LoginFacade:
    def __init__(self):
        self.login = Login()

    async def login_api(self, user: User):
        """
        Login Api.
        """
        logger.info(f"Login In with {user.email}")
        await self.login.update_session(user)
        await self.login.update_servers_and_characters(user)
