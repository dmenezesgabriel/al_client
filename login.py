import logging

from user import User

logger = logging.getLogger("alclient.login")


class LoginFacade:
    @classmethod
    async def loginApi(cls, user: User):
        """
        Login Api.
        """
        logger.info(f"Login In with {user.email}")
        await user.update_session()
        await user.update_servers_and_characters()
