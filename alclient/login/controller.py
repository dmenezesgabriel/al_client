import logging

from alclient.login.facade import LoginFacade
from alclient.user.user import User

logger = logging.getLogger("adventure_land.login_controller")


class LoginController:
    def __init__(self) -> None:
        self.login_facade = LoginFacade()

    async def run(self, user: User):
        await self.login_facade.login_api(user)
