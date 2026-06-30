"""
Discord Gateway / WebSocket API Connector

Discord has two (mutually exclusive) APIs accessible to bot applications
for interacting with a guild it is in. This program connects it to the Gateway.

It is meant for receiving real-time changes (and sometimes sending information), called events,
in the guilds the bot is listening to.

For a comprehensive explanation of how the Gateway operates, see https://docs.discord.com/developers/events/gateway.
"""

import asyncio
import httpx
import json
import random
from typehints.typehints import *
from websockets.asyncio import client as Client

class GatewayConnector():
    """
    Establishes a WebSockets connection to the Gateway.

    Requires the bot user's token and intents, as specified by
    the user. Intents defaults to the standard intents but will not be enforced here,
    but rather in the `BotUser` class in file `bot.py`.

    Default version is v10.
    """
    # The version number is hardcoded. (Maybe check if this can be changed by fetching
    # the latest version's number somehow; I couldn't find it on the website.)

    def __init__(self, token : BotToken, intents : BotIntents):
       self.TOKEN = token
       self.INTENTS = intents

    def _fetch_url(self) -> JSON:
        """
        Fetches the WSS URL and metadata required to start the WebSocket connection.

        This is recommended by Discord themselves, so that the case of any
        future changes to the URL can be handled, and to also fetch recommended sharding details.
        """

        with httpx.Client() as client:
            response = client.get(
                url = "https://discord.com/api/v10/gateway/bot",
                headers = {
                    "Authorization" : f"Bot {self.TOKEN}"
                    }
                )
            
            data = response.json()

        return data

    async def _send_identify(self):
        """
        Sends an `IDENTIFY` packet with the bot information.
        This is the part that requires the token and intents for authentication.
        """

        ...

    async def _maintain_heartbeat(self, client : Client.ClientConnection, heartbeat_interval : int) -> None:
        """
        Maintains a heartbeat to tell the Gateway the bot is still online and wishes to
        send and receive interactions.
        Heartbeat is fetched from the `HELLO` packet received at the beginning.
        """

        first_heartbeat : bool = True

        while client.state == 0 or 1: # I'm a little confused here, let this be as it is temporarily
            if first_heartbeat == True:
                jitter = random.random()
                
                await asyncio.sleep(heartbeat_interval * jitter)
                await client.send(message = json.dumps({"op" : "1", "d": "null"}))
                # "d" should NOT say null always, do not be lazy - this should be fixed ASAP

                first_heartbeat = False
            else:
                await asyncio.sleep(heartbeat_interval)
                await client.send(message = json.dumps({"op" : "1", "d": "null"}))
                # GET Line80

    async def _gateway_listener(self, client : Client.ClientConnection, info : dict) -> None:
        """
        Listens to the Gateway for all events.
        Of these, the `HELLO`, `READY`, and disconnection events are specially handled.
        """

        hello_packet = json.loads(await client.recv(decode = True))

        await self._maintain_heartbeat(
                client = client,
                heartbeat_interval = int(hello_packet["d"]["heartbeat_interval"]) # Safety type conversion
            )
        
    async def connect_to_gateway(self):
        """
        Fetches the connection URL and connects the bot to the Gateway.
        """

        info = self._fetch_url()

        async with Client.connect(uri = info["url"] + "?v=10&encoding=json") as client:
            pass

        # aS you can see, this is for future me