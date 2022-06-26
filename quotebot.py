import hikari

text_file = open("./token.txt")
new_token = text_file.read()
text_file.close()
print(new_token)

bot = hikari.GatewayBot(token=new_token)

@bot.listen(hikari.GuildMessageCreateEvent)
async def print_message(event):
    print(event.content)
    
@bot.listen(hikari.StartedEvent)
async def bot_started(event):
    print('Bot has started!')



bot.run()
