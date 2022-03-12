import json
import logging

import aiohttp

logger = logging.getLogger("alclient.user")


class User:
    """
    User class.
    """

    def __init__(
        self,
        email,
        password,
        session=None,
        id=None,
        characters=None,
        servers=None,
        code_list=None,
        mail=None,
        rewards=None,
        tutorial=None,
    ):
        self.email = email
        self.password = password
        self._session = session
        self._id = id
        self._characters = characters
        self._servers = servers
        self._code_list = code_list
        self._mail = mail
        self._rewards = rewards
        self._tutorial = tutorial

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, email):
        self._email = email

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self._password = password

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    @property
    def session(self):
        return self._session

    @session.setter
    def session(self, session):
        self._session = session

    @property
    def characters(self):
        return self._characters

    @characters.setter
    def characters(self, characters):
        self._characters = characters

    @property
    def servers(self):
        return self._servers

    @servers.setter
    def servers(self, servers):
        self._servers = servers

    @property
    def code_list(self):
        return self._code_list

    @code_list.setter
    def code_list(self, code_list):
        self._code_list = code_list

    @property
    def mail(self):
        return self._mail

    @mail.setter
    def mail(self, mail):
        self._mail = mail

    @property
    def rewards(self):
        return self._rewards

    @rewards.setter
    def rewards(self, rewards):
        self._rewards = rewards

    @property
    def tutorial(self):
        return self._tutorial

    @tutorial.setter
    def tutorial(self, tutorial):
        self._tutorial = tutorial

    async def post_code(self, file_path, slot_number, save_name):
        print("Posting code")
        with open(file_path, "r") as code_file:
            code_file_content = code_file.read()
        args = dict(
            code=code_file_content,
            slot=str(slot_number),
            name=save_name,
            log="1",
        )
        arguments = json.dumps(args)
        data = {
            "method": "save_code",
            "arguments": arguments,
        }
        headers = dict(cookie=f"auth={self.id}-{self.session}")
        headers.update({"Content-Type": "application/x-www-form-urlencoded"})
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.post(
                "https://adventure.land/api/save_code",
                data=data,
            ) as response:
                if response.status == 200:
                    text_response = await response.text()
                    try:
                        json_response = json.loads(text_response)
                        return json_response
                    except Exception as error:
                        logger.error(error)

    async def logout_everywhere(self):
        """
        Logout from everywhere.
        """
        logger.info("Login Out")
        data = {
            "method": "logout_everywhere",
            "arguments": "{}",
        }
        headers = dict(cookie=f"auth={self._id}-{self.session}")
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
