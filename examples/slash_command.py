# A program that demonstrates syntax to register and use a slash command: /ping
from devcord import BotUser, ALL_INTENTS

bot = BotUser(
    token = "...",
    intents = ALL_INTENTS
)

@bot.slash_command
async def ping():       # Creates a slash command with ping as its calling name,
    bot.send("pong!")   # this is to be dealt with later

bot.run()