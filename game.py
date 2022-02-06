import json
import re

import aiohttp


class Game:
    async def get_session(self, email, password):
        data = {
            "method": "signup_or_login",
            "arguments": (
                '{ "email": "'
                + email
                + '", "password": "'
                + password
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
                            self.user_id = auth.split("-")[0]
                            self.session_cookie = auth.split("-")[1]

                            return dict(
                                user_id=auth.split("-")[0],
                                session_cookie=auth.split("-")[1],
                            )

    async def get_servers_and_characters(self):
        data = {
            "method": "servers_and_characters",
            "arguments": "{}",
        }
        headers = dict(cookie=f"auth={self.user_id}-{self.session_cookie}")
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
                        print(error)

    async def set_servers_and_characters(self):
        servers_and_characters = await self.get_servers_and_characters()
        self.characters = servers_and_characters[0].get("characters")
        self.servers = servers_and_characters[0].get("servers")
        self.code_list = servers_and_characters[0].get("code_list")
        self.mail = servers_and_characters[0].get("mail")
        self.rewards = servers_and_characters[0].get("rewards")
        self.tutorial = servers_and_characters[0].get("tutorial")

    async def logout_everywhere(self):
        data = {
            "method": "logout_everywhere",
            "arguments": "{}",
        }
        headers = dict(cookie=f"auth={self.user_id}-{self.session_cookie}")
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
                        print(error)
