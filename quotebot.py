import hikari

bot = hikari.GatewayBot(token='OTkwNDM0MDI1MDExMjkwMTMy.GnTV_n.L_nnVBVVH0u3k7aiDD3huup9RHwkcC9obBV5oQ')

@bot.listen(hikari.GuildMessageCreateEvent)
async def print_message(event):
    print(event.content)
    
@bot.listen(hikari.StartedEvent)
async def bot_started(event):
    print('Bot has started!')



bot.run()
