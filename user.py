import json
import logging
import re

import aiohttp

logger = logging.getLogger("adventure_land.user")


class User:
    """
    User class.
    """

    def __init__(self, email, password, id=None):
        self._email = email
        self._password = password
        self._id = id

    @property
    def email(self):
        return self._email

    @property
    def password(self):
        return self._password

    @property
    def id(self):
        return self._id

    async def update_session(self):
        """
        Update user session.
        """
        logger.info(f"Getting session for {self._email}")
        data = {
            "method": "signup_or_login",
            "arguments": (
                '{ "email": "'
                + self._email
                + '", "password": "'
                + self._password
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
                            self._id = user_id
                            self.session_cookie = session_cookie

                            return dict(
                                user_id=user_id,
                                session_cookie=session_cookie,
                            )

    async def _get_servers_and_characters(self):
        """
        Get servers and characters data.
        """
        logger.info(f"Getting servers and characters for {self._email}")
        data = {
            "method": "servers_and_characters",
            "arguments": "{}",
        }
        headers = dict(cookie=f"auth={self._id}-{self.session_cookie}")
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

    async def update_servers_and_characters(self):
        """
        Update servers and characters.
        """
        logger.info(f"Updating servers and characters for {self._email}")
        servers_and_characters = await self._get_servers_and_characters()
        self.characters = servers_and_characters[0].get("characters")
        self.servers = servers_and_characters[0].get("servers")
        self.code_list = servers_and_characters[0].get("code_list")
        self.mail = servers_and_characters[0].get("mail")
        self.rewards = servers_and_characters[0].get("rewards")
        self.tutorial = servers_and_characters[0].get("tutorial")

    async def logout_everywhere(self):
        """
        Logout from everywhere.
        """
        logger.info(f"Login Out {self.email}")
        data = {
            "method": "logout_everywhere",
            "arguments": "{}",
        }
        headers = dict(cookie=f"auth={self._id}-{self.session_cookie}")
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.post(
                "https://adventure.land/api/logout_everywhere",
                data=data,
            ) as response:
                if response.status == 200:
                    text_response = await response.text()
                    try:
                        json_response = json.loads(text_response)
                        return json_response
                    except Exception as error:
                        logger.error(error)
