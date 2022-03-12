import logging

from alclient.domain.user import User
from alclient.login.facade import LoginFacade

logger = logging.getLogger("alclient.login_controller")


class LoginController:
    def __init__(self) -> None:
        self.login_facade = LoginFacade()

    async def run(self, user: User):
        await self.login_facade.login_api(user)
