"""
Discord HTTP API Connector (v10)

Discord bots need to use two APIs in order to send and receive all interactions.
The HTTP API is a REST API that lets you interact and modify
core Discord resources like channels, servers (or guilds), users, and messages.

For a comprehensive documentation of the HTTP API's workings, see https://docs.discord.com/developers/reference#http-api.
"""

import httpx

BASE_URL = "https://discord.com/api/v10"

class HTTPAPIConnector():
    """
    Creates, sends, and receives requests to and from the Discord HTTP API. Interactions are in
    the form of JSON packets.
    """

    def __init__(self, token):
        self.TOKEN = token

    async def _send_get(self):
        """
        Method to send a `GET` request with the specified params.
        (Doing this because of redundancy)
        """
        async with httpx.AsyncClient() as client:
            client.get
        ...

    async def _send_post(self, url, content_type, json):
        """
        Method to send a `POST` request with the specified params.
        (Doing this because of redundancy)
        """

        async with httpx.AsyncClient() as client:
            response = await client.post(
                url = BASE_URL + url,
                headers = {
                    "Authorization" : f"Bot {self.TOKEN}",
                    "User-Agent" : "DiscordBot (https://github.com, 1.0)",
                    "Content-Type" : content_type
                },
                json = json
            )

            response.raise_for_status()

    async def create_message(self, message: str, channel_id: int):
        """
        Sends messages in a channel using a `POST` request.
        """

        await self._send_post(
                url = f"/channels/{channel_id}/messages",
                content_type = "application/json",
                json = {
                    "content" : message
                }
            )