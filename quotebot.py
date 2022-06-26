import random
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
@lightbulb.command('zznewquote', 'Stores the given quote.')
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
    await contextObject.respond(contextObject.options.num1 + contextObject.options.num2)
    
    
    
    
# actual stuff starts here

# quote data file
databaseFile = "./quotedata.txt"

# stores all quotes during runtime
# refreshed on every readToArray() call
database = open(databaseFile)
quotearray = database.readlines()
database.close

# read all quote data lines to quotearray
# does a full refresh of the quotearray
def readToArray():
    database = open(databaseFile)
    quotearray = database.readlines()
    database.close
    
#initial read
readToArray()

# writes to file and appends to end of quotearray
# does not do a full refresh of quotearray
def writeNewQuote(quotetext):
    database = open(databaseFile, "a") # open for append
    database.write(quotetext + "\n")
    quotearray.append(quotetext)
    database.close

#grab a random quote
def getQuote():
    quoteArrayLen = len(quotearray)
    return quotearray[random.randrange(0, (quoteArrayLen), 1)]

# Command: Get quote.
# Option - Amount: Returns this many random quotes.
@bot.command
@lightbulb.option('amount', 'Number of quotes to spit out.', type=int)
@lightbulb.command('quote', 'Random quotes.')
@lightbulb.implements(lightbulb.SlashCommand)
async def quote(context):
    quotestring = ""
    for x in range(context.options.amount):
        quotestring += getQuote() + "\n"    
    await context.respond(quotestring)
    
@bot.command
@lightbulb.command('quote')
@lightbulb.implements(lightbulb.SlashCommand)
async def quote(context):
    await context.respond(getQuote() + "\n")
        
# Command: Add new quote to database.
@bot.command
@lightbulb.option('quote', 'Quote to be added.', type=str)
@lightbulb.command('newquote', 'Adds new quote.')
@lightbulb.implements(lightbulb.SlashCommand)
async def newquote(context):
    writeNewQuote(context.options.quote)
    await context.respond('Quote added.')
    
@bot.command
@lightbulb.option('quote', 'Quote to be added.', type=str)
@lightbulb.command('addquote', 'Adds new quote.')
@lightbulb.implements(lightbulb.SlashCommand)
async def addquote(context):
    writeNewQuote(context.options.quote)
    await context.respond('Quote added.')
    


# finally, run the bot
bot.run()
