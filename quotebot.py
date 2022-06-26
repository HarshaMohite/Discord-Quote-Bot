import hikari
import lightbulb

text_file = open("./token.txt")
new_token = text_file.read()
text_file.close()
print(new_token)

bot = lightbulb.BotApp(token=new_token, default_enabled_guilds=())

@bot.listen(hikari.GuildMessageCreateEvent)
async def print_message(event):
    print(event.content)

@bot.listen(hikari.StartedEvent)
async def bot_started(event):
    print('Bot has started!')
    
@bot.command
@lightbulb.command('newquote', 'Stores the given quote.')
@lightbulb.implements(lightbulb.SlashCommand)
async def ping(contextObject):
    await contextObject.respond('Pong!')
    
@bot.command
@lightbulb.command('group', 'This is a group')
@lightbulb.implements(lightbulb.SlashCommandGroup)
async def my_group(contextObject):
    pass

@my_group.child
@lightbulb.command('subcommand', 'This is a subcommand')
@lightbulb.implements(lightbulb.SlashSubCommand)
async def subcommand(contextObject):
    await contextObject.respond('I am a subcommand!')
    
@bot.command
@lightbulb.option('num1', 'The first number', type=int)
@lightbulb.option('num2', 'The second number', type=int)
@lightbulb.command('add', 'Add two numbers together')
@lightbulb.implements(lightbulb.SlashCommand)
async def add(contextObject):
    await contextObject.respond(ctx.options.num1 + ctx.options.num2)
    

bot.run()
