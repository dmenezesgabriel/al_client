import logging

from alclient.domain.user import User
from alclient.login.login import Login

logger = logging.getLogger("alclient.login_facade")


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
