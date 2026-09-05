import asyncio
from collections.abc import Coroutine

import httpx

from .consts.intents import STANDARD_INTENTS
from .typehints.typehints import BotToken, BotIntents
from .connectors.gateway_connector import GatewayConnector
from .connectors.http_api_connector import HTTPAPIConnector

class Context:
    def __init__(self, data, token):
        self.channel_id = data["channel_id"]
        self.author = data["author"]
        self.content = data["content"]
        self.token = token

    async def send(self, message):
        async with httpx.AsyncClient() as client:
            await client.post(
                url=f"https://discord.com/api/v10/channels/{self.channel_id}/messages",
                headers={
                    "Authorization": f"Bot {self.token}",
                    "Content-Type": "application/json"
                },
                json={"content": message}
            )

class BotUser():
    """
    Initialises a bot user object with the specified token, intents, and potential prefix.  
    If no intents are specified, `STANDARD_INTENTS` is the default.
    """
    
    def __init__(self, token : BotToken, intents : BotIntents = STANDARD_INTENTS):
        self.TOKEN = token
        self.INTENTS = intents
        self.listener_coros: dict[str, Coroutine] = {}

    def command(self, prefix : str):
        """
        Decorator to create normal message commands with a set prefix, and name
        being the name of the function.    
        Prefix defaults to `\\`.
        """
        self.PREFIX = prefix

        def func(coro: Coroutine):
            self.listener_coros[coro.__name__] = coro
            
        return func

    async def _handle_message(self, data):
        content = data["content"]
        if not content.startswith(self.PREFIX):
            return
        
        command_name = content[len(self.PREFIX):].split()[0]
        
        if command_name not in self.listener_coros:
            return
        
        ctx = Context(data, self.TOKEN)
        await self.listener_coros[command_name](ctx)

    async def dispatch(self, event_name, data):
        if event_name == "MESSAGE_CREATE":
            await self._handle_message(data)

    def slash_command(self):
        """
        Decorator to create slash commands, with name being the name of the function.
        """
        pass

    def run(self):
        """
        Runs the bot with the specified token, intents, and potential prefix.
        Prefix defaults to `\\`.  
        If no intents are specified, `STANDARD_INTENTS` is assumed.
        """

        asyncio.run(
            GatewayConnector(
                token = self.TOKEN,
                intents = self.INTENTS,
                disp = self.dispatch
            ).connect_to_gateway()
        )