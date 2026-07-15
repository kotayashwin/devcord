# The simplest program that can run a bot using DevCord.
from devcord import BotUser, ALL_INTENTS

bot = BotUser(
    token = "...",
    intents = ALL_INTENTS
)

bot.run()