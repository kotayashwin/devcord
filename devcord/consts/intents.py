"""
Discord Intents

Defines constants with commonly used intent values, pre-calculated for convenience. It also houses the helper
class `Intents`, for manually enabling or disabling intents for your bot.
For more information on how to calculate your intent values, see: https://docs.discord.com/developers/events/gateway#gateway-intents
"""

STANDARD_INTENTS = 53575421
ALL_INTENTS      = 53608447

INTENTS_HASHMAP = {
    "GUILDS"                        : (1 << 0),
    "GUILD_MEMBERS"                 : (1 << 1),
    "GUILD_BANS"                    : (1 << 2),
    "GUILD_EMOJIS_AND_STICKERS"     : (1 << 3),
    "GUILD_INTEGRATIONS"            : (1 << 4),
    "GUILD_WEBHOOKS"                : (1 << 5),
    "GUILD_INVITES"                 : (1 << 6),
    "GUILD_VOICE_STATES"            : (1 << 7),
    "GUILD_PRESENCES"               : (1 << 8),
    "GUILD_MESSAGES"                : (1 << 9),
    "GUILD_MESSAGE_REACTIONS "      : (1 << 10),
    "GUILD_MESSAGE_TYPING"          : (1 << 11),
    "DIRECT_MESSAGES"               : (1 << 12),
    "DIRECT_MESSAGE_REACTIONS"      : (1 << 13),
    "DIRECT_MESSAGE_TYPING"         : (1 << 14),
    "MESSAGE_CONTENT"               : (1 << 15),
    "GUILD_SCHEDULED_EVENTS"        : (1 << 16),
    "AUTO_MODERATION_CONFIGURATION" : (1 << 20),
    "AUTO_MODERATION_EXECUTION"     : (1 << 21),
    "GUILD_MESSAGE_POLLS"           : (1 << 24),
    "DIRECT_MESSAGE_POLLS"          : (1 << 25)
}

class Intents():
    """
    Helper class to calculate intents manually.
    """

    def __init__(self):
        print("We recommend you use STANDARD_INTENTS or ALL_INTENTS.\n")
        print("For more information on the names of intents, see: https://docs.discord.com/developers/events/gateway#gateway-intents\n")
        self.intent_value = STANDARD_INTENTS

    def include(self, opt_info : list[str]) -> int:
        """
        A helper function to include the intent value of only the provided intents, starting from STANDARD_INTENTS.
        """

        for intent in opt_info:
            if intent.upper() in INTENTS_HASHMAP.keys():
                self.intent_value += INTENTS_HASHMAP[intent]
            else:
                raise Exception("Invalid intent name(s) provided in Intents.include([\"...\"])")

    def exclude(self, opt_info : list[str]) -> int:
        """
        A helper function to exclude the intent value of only the provided intents, starting from STANDARD_INTENTS.
        """

        for intent in opt_info:
            if intent.upper() in INTENTS_HASHMAP.keys():
                self.intent_value -= INTENTS_HASHMAP[intent]
            else:
                raise Exception("Invalid intent name(s) provided in Intents.exclude([\"...\"])")