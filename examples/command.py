# A program that demonstrates syntax to register and use a command: \ping
from devcord import BotUser, ALL_INTENTS

bot = BotUser(
    token = "...",
    intents = ALL_INTENTS
)

@bot.command(prefix = "\\")
async def ping(ctx):       # Creates a command with ping as its calling name,
    await ctx.send("pong!")

bot.run()