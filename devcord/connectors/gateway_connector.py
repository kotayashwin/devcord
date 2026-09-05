"""
Discord Gateway / WebSocket API Connector

Discord has two (mutually exclusive) APIs accessible to bot applications
for interacting with a guild it is in. This program connects it to the Gateway.

It is meant for receiving real-time changes (and sometimes sending information), called events,
in the guilds the bot is listening to.

For a comprehensive explanation of how the Gateway operates, see https://docs.discord.com/developers/events/gateway.
"""

import asyncio
import json
import random
import sys

import httpx
from websockets.asyncio import client as Client

from ..typehints.typehints import *
from ..consts.opcodes import *
from ..events import *

class GatewayConnector():
    """
    Establishes a WebSockets connection to the Gateway.

    Requires the bot user's token and intents, as specified by
    the user. Intents defaults to the standard intents but will not be enforced here,
    but rather in the `BotUser` class in file `bot.py`.

    Default version is v10.
    """

    # The version number must be hardcoded. 
    # There is no HTTP endpoint to determine the latest stable version.

    def __init__(self, token : BotToken, intents : BotIntents, disp) -> None:
        self.TOKEN = token
        self.INTENTS = intents
        self.API_VERSION = 10
        self.disp = disp
        self.d = None

    def _fetch_url(self) -> JSON:
        """
        Fetches the WSS URL and metadata required to start the WebSocket connection.

        This is recommended by Discord themselves, so that the case of any
        future changes to the URL can be handled, and to also fetch recommended sharding details.
        """
        # TODO: sharding implementation in devcord

        with httpx.Client() as client:
            response = client.get(
                url = f"https://discord.com/api/v{self.API_VERSION}/gateway/bot",
                headers = {
                        "Authorization" : f"Bot {self.TOKEN}"
                    }
                )
            
        return response.json()

    async def _send_identify(self, client : Client.ClientConnection) -> None:
        """
        Sends an `IDENTIFY` packet with the bot information.
        This is the part that requires the token and intents for authentication.
        """
        
        await client.send(
            message = json.dumps(
                {
                    "op" : 2,
                    "d" : {
                        "token" : self.TOKEN,
                        "properties" : {
                            "os" : f"{sys.platform}",
                            "browser" : "DevCord",
                            "device" : "DevCord"
                        },
                        "compress" : False,
                        "presence" : {
                                "since" : None,
                                "activities" : [],
                                "status" : "online",
                                "afk" : False
                            },
                        "intents" : self.INTENTS
                        }
                }
            )
        )

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

    async def _send_presence(self, client : Client.ClientConnection):
        await client.send(
            message = json.dumps(
                {
                    "op": 3,
                    "d": {
                        "since": None,
                        "activities": [],
                        "status": "online",
                        "afk": False
                    }
                }
            )
        )

    async def _handler(self, event: str, client: Client.ClientConnection):
        """
        The universal helper function that handles events coming in from the Gateway.
        
        Some critical processes like """
        opcode = event["op"]

        if opcode == DISPATCH:
            # This is a received heartbeat, it's different from a sent one:
            # https://docs.discord.com/developers/events/gateway#heartbeat-requests
            # httpx.post(
            #     url = f"https://discord.com/api/v10/channels/{int(event["d"]["channel_id"])}/messages",
            #     json = {
            #         "content": "pong!"
            #     },
            #     headers = {
            #         "Authorization" : f"Bot {self.TOKEN}",
            #         "User-Agent" : f"devcord@{sys.platform} (https://github.com/kotayashwin/devcord, 1.0)", # add devcord version here
            #         "Content-Type" : "application/json"
            #     }
            # )
            await self.disp(event["t"], event["d"])
        elif opcode == HEARTBEAT:
            ...
        elif opcode == IDENTIFY:
            ...
        elif opcode == PRESENCE_UPDATE:
            ...
        elif opcode == VOICE_STATE_UPDATE:
            ...
        elif opcode == RESUME:
            ...
        elif opcode == RECONNECT:
            ...
        elif opcode == REQUEST_GUILD_MEMBERS:
            ...
        elif opcode == INVALID_SESSION:
            ...
        elif opcode == HELLO:
            ...
        elif opcode == HEARTBEAT_ACK:
            ...
        elif opcode == REQUEST_SOUNDBOARD_SOUNDS:
            ...
        elif opcode == REQUEST_CHANNEL_INFO:
            ...
        else:
            raise Exception("Unknown or unsupported opcode received from Discord.")

    async def _listener(self, client : Client.ClientConnection):
        """
        The helper function which listens to incoming event information.

        While it's meant to solely be a listener, it also caches the value of s at every event, and passes it as the
        value of d on the next heartbeat. It is also essential for resuming broken connections. There's no point
        in separating this implementation into another helper function.
        
        """
        
        async for event in client:
            event = json.loads(event)

            # Caches the value of s in self.d
            if (event["s"] != None):
                self.d = event["s"]

            asyncio.create_task(
                self._handler(event, client)
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
                self._listener(
                    client = client
                ),
                self._send_presence(
                    client = client
                )
            )