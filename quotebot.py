import random
import hikari
import lightbulb

# load token
text_file = open("./token.txt")
new_token = text_file.read()
text_file.close()
print(new_token)

bot = lightbulb.BotApp(token=new_token)

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
@lightbulb.command('quotes', 'Print multiple random quotes.')
@lightbulb.implements(lightbulb.SlashCommand)
async def quote(context):
    quotestring = ""
    for x in range(context.options.amount):
        quotestring += getQuote() + "\n"    
    await context.respond(quotestring)
    
@bot.command
@lightbulb.command('quote', 'Print a random quote.')
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
