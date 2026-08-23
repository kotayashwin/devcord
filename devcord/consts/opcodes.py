"""
Gateway Opcodes

All numerical opcodes used in the Gateway connection.
Refer: https://docs.discord.com/developers/topics/opcodes-and-status-codes#gateway
"""

DISPATCH                  = 0
HEARTBEAT                 = 1
IDENTIFY                  = 2
PRESENCE_UPDATE           = 3
VOICE_STATE_UPDATE        = 4
RESUME                    = 6
RECONNECT                 = 7
REQUEST_GUILD_MEMBERS     = 8
INVALID_SESSION           = 9
HELLO                     = 10
HEARTBEAT_ACK             = 11
REQUEST_SOUNDBOARD_SOUNDS = 31
REQUEST_CHANNEL_INFO      = 43