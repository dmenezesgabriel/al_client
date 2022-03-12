import json
import logging
import re

import aiohttp
from alclient.user.user import User

logger = logging.getLogger("adventure_land.login")


class Login:
    async def update_session(self, user: User) -> dict:
        """
        Update user session.
        """
        logger.info(f"Getting session for {user.email}")
        data = {
            "method": "signup_or_login",
            "arguments": (
                '{ "email": "'
                + user.email
                + '", "password": "'
                + user.password
                + '", "only_login": "true"}'
            ),
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://adventure.land/api/signup_or_login", data=data
            ) as response:
                if response.status == 200:
                    text_response = await response.text()
                    messages = [
                        data
                        for data in json.loads(text_response)
                        if "message" in data
                    ]
                    has_logged_in = any(
                        message["message"] == "Logged In!"
                        for message in messages
                    )
                    if has_logged_in:
                        match = re.match(
                            r"^auth=(.+?);", response.headers["Set-Cookie"]
                        )
                        if match:
                            auth = match.group(1)
                            user_id = auth.split("-")[0]
                            session_cookie = auth.split("-")[1]
                            user.id = user_id
                            user.session = session_cookie

                            return dict(
                                user_id=user_id,
                                session_cookie=session_cookie,
                            )

    async def _get_servers_and_characters(self, user: User) -> None:
        """
        Get servers and characters data.
        """
        logger.info(f"Getting servers and characters for {user.email}")
        data = {
            "method": "servers_and_characters",
            "arguments": "{}",
        }
        headers = dict(cookie=f"auth={user.id}-{user.session}")
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.post(
                "https://adventure.land/api/servers_and_characters",
                data=data,
            ) as response:
                if response.status == 200:
                    text_response = await response.text()
                    try:
                        json_response = json.loads(text_response)
                        return json_response
                    except Exception as error:
                        logger.error(error)

    async def update_servers_and_characters(self, user: User):
        """
        Update servers and characters.
        """
        logger.info(f"Updating servers and characters for {user.email}")
        servers_and_characters = await self._get_servers_and_characters(user)
        user.characters = servers_and_characters[0].get("characters")
        user.servers = servers_and_characters[0].get("servers")
        user.code_list = servers_and_characters[0].get("code_list")
        user.mail = servers_and_characters[0].get("mail")
        user.rewards = servers_and_characters[0].get("rewards")
        user.tutorial = servers_and_characters[0].get("tutorial")
