from .consts.intents import STANDARD_INTENTS
from .typehints.typehints import BotToken, BotIntents
from .connectors.gateway_connector import GatewayConnector
from .connectors.http_api_connector import HTTPAPIConnector

import asyncio

class BotUser():
    """
    Initialises a bot user object with the specified token, intents, and potential prefix.  
    If no intents are specified, `STANDARD_INTENTS` is the default.
    """
    
    def __init__(self, token : BotToken, intents : BotIntents = STANDARD_INTENTS):
        self.TOKEN = token
        self.INTENTS = intents

    async def command(self, function : function, prefix : str = "\\"):
        """
        Decorator to create normal message commands with a set prefix, and name
        being the name of the function.    
        Prefix defaults to `\\`.
        """
        pass

    async def slash_command(self, *args, **kwargs):
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
                intents = self.INTENTS
            ).connect_to_gateway()
        )