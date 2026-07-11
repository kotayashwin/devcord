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

    # The version number must be hardcoded. 
    # There is no endpoint to determine the latest stable version.

    def __init__(self, token : BotToken, intents : BotIntents):
       self.TOKEN = token
       self.INTENTS = intents
       self.d = None

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
            
        return response.json()

    async def _send_identify(self, client : Client.ClientConnection):
        """
        Sends an `IDENTIFY` packet with the bot information.
        This is the part that requires the token and intents for authentication.
        """
        
        await client.send(message = json.dumps(
            {
                "op" : 2,
                "d" : {
                    "token" : self.TOKEN,
                    "properties" : {
                        "os" : "win11",
                        "browser" : "chrome",
                        "device" : "chrome"
                    },
                    "compress" : False,
                    "presence" : {
                            "since" : None,
                            "activities" : [{
                                "name" : "yashbot",
                                "type" : 3
                            }],
                            "status" : "online",
                            "afk" : False
                        },
                    "intents" : 53608447
                    }
            }
        ))

    async def _maintain_heartbeat(self, client : Client.ClientConnection, heartbeat_interval : int) -> None:
        """
        Maintains a heartbeat to tell the Gateway the bot is still online and wishes to
        send and receive interactions.
        Heartbeat is fetched from the `HELLO` packet received at the beginning.
        """

        first_heartbeat : bool = True

        while True:
            if first_heartbeat == True:
                jitter = random.random()
                
                await asyncio.sleep(heartbeat_interval * jitter / 1000)
                await client.send(message = json.dumps({"op" : 1, "d": self.d}))
                
                first_heartbeat = False
            else:
                await asyncio.sleep(heartbeat_interval / 1000)
                await client.send(message = json.dumps({"op" : 1, "d": self.d}))  
    
    async def _d_cacher(self, client : Client.ClientConnection):
        """
        For caching the value of s every time an event comes.
        This is essential for resuming a broken connection.
        """
        async for message in client:
            print(self.d)
            self.d = (json.loads(message))["s"]

    async def _send_presence(self, client : Client.ClientConnection):
        await client.send(
            message = json.dumps(
                {
                    "op": 3,
                    "d": {
                        "since": None,
                        "activities": [{
                            "name": "yashbot",
                            "type": 3
                            }],
                        "status": "online",
                        "afk": False
                    }
                }
            )
        )

    async def connect_to_gateway(self):
        """
        Fetches the connection URL and connects the bot to the Gateway.
        """

        data = self._fetch_url()

        async with Client.connect(uri = data["url"] + "?v=10&encoding=json") as client:
            hello_packet = json.loads(await client.recv(decode = True))

            await asyncio.gather(
                self._maintain_heartbeat(
                    client = client,
                    heartbeat_interval = int(hello_packet["d"]["heartbeat_interval"])
                ),
                self._send_identify(
                    client = client
                ),
                self._d_cacher(
                    client = client
                ),
                self._send_presence(
                    client = client
                )
            )