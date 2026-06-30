import devcord

BOT_TOKEN = "..."

bot = devcord.BotUser(
    token = BOT_TOKEN,
    intents = ...
)

@bot.slash_command
async def ping(): # Creates a slash command with ping as its calling name,
                  # this is to be dealt with later
    bot.send("pong!")

bot.run()