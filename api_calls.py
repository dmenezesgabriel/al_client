import asyncio
import json
import os
import re

import aiohttp


async def login(email, password):
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
            print(response.status)
            text_response = await response.text()
            messages = [
                data for data in json.loads(text_response) if "message" in data
            ]
            has_logged_in = any(
                message["message"] == "Logged In!" for message in messages
            )
            if has_logged_in:
                match = re.match(
                    r"^auth=(.+?);", response.headers["Set-Cookie"]
                )
                if match:
                    auth = match.group(0)
                    return dict(
                        user_auth=auth.split("-")[0],
                        user_id=auth.split("-")[1],
                    )


async def main():
    email = os.environ["EMAIL"]
    password = os.environ["PASSWORD"]
    print(email)
    login_data = await login(email, password)
    print(login_data)


asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(main())
