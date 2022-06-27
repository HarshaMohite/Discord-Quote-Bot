from contextlib import nullcontext
import math
import random
import hikari
import lightbulb

# load token
text_file = open("./token.txt")
new_token = text_file.read()
text_file.close()
print(new_token)

bot = lightbulb.BotApp(token=new_token, prefix=".")

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
    if ".quote" in quotetext.lower():
        return False
    if ".addquote" in quotetext.lower():
        return False
    if ".newquote" in quotetext.lower():
        return False
    if "!quote" in quotetext.lower():
        return False
    if "!addquote" in quotetext.lower():
        return False
    if "!newquote" in quotetext.lower():
        return False
    quotetext_appended = quotetext + "\n" # Need to check for duplicates with newline char at end
    if quotetext_appended in quotearray:
        return False
    database = open(databaseFile, "a") # open for append
    database.write(quotetext_appended)
    quotearray.append(quotetext_appended)
    database.close
    return True

#grab a random quote
def getQuote():
    quoteArrayLen = len(quotearray)
    if len == 0: # todo: these checks currently do not work, but no crashes occur
        return "No quotes."
    if len == -1:
        return "No quotes."
    else:
        return quotearray[random.randrange(0, (quoteArrayLen), 1)]

# Get multiple quotes.
# Option - Amount: Print this many random quotes. Max 10.
def getQuotes(amount):
    quotestring = ""
    for x in range(min(10, max(1, amount))):
        quotestring += getQuote()
    return quotestring
    

# COMMAND #
# quote
@bot.command
@lightbulb.option('amount', 'Number of quotes to print.', type=int, required=False)
@lightbulb.command('quote', 'Print a random quote.')
@lightbulb.implements(lightbulb.SlashCommand)
async def quote(context):
    if context.options.amount == None:
        await context.respond(getQuote())
    else:
        await context.respond(getQuotes(context.options.amount))
        
@bot.command
@lightbulb.option('amount', 'Number of quotes to print.', type=int, required=False)
@lightbulb.command('quote', 'Print a random quote.')
@lightbulb.implements(lightbulb.PrefixCommand)
async def quote(context):
    if context.options.amount == None:
        await bot.rest.create_message(context.get_channel().id, getQuote())
    else:
        await bot.rest.create_message(context.get_channel().id, getQuotes(context.options.amount))
        
        
# COMMAND #
# newquote / addquote
@bot.command
@lightbulb.option('quote', 'Quote to be added.', type=str)
@lightbulb.command('newquote', 'Adds new quote.', aliases=["addquote"])
@lightbulb.implements(lightbulb.SlashCommand)
async def newquote(context):        
    if writeNewQuote(context.options.quote):
        await context.respond("Quote added: " + context.options.quote)
        print("Quote added: " + context.options.quote)
    else:
        await context.respond("Quote invalid.")
    
@bot.command
@lightbulb.option('quote', 'Quote to be added.', type=str, modifier=lightbulb.OptionModifier.CONSUME_REST, required=False)
@lightbulb.command('newquote', 'Adds new quote.', aliases=["addquote"])
@lightbulb.implements(lightbulb.PrefixCommand)
async def newquote(context):        
    newQuoteWritten = False # outcome of writeNewQuote
    newQuoteText = ""
    if context.event.message.referenced_message != None: # see if quote is from a replied message
        newQuoteText = context.event.message.referenced_message.content
        newQuoteWritten = writeNewQuote(newQuoteText)
    else: # otherwise, take text like normal
        if context.options.quote == None:
            return
        else:
            newQuoteText = context.options.quote
            newQuoteWritten = writeNewQuote(newQuoteText)
        
    if newQuoteWritten:
        await bot.rest.create_message(context.get_channel().id, "Quote added: " + newQuoteText)
        print("Quote added: " + context.options.quote)
    else:
        await bot.rest.create_message(context.get_channel().id, "Quote invalid. Already in database or includes a bot command.")
    


@bot.command
@lightbulb.command('echoreply', 'Echo the reply')
@lightbulb.implements(lightbulb.PrefixCommand)
async def echoreply(context):
    if context.event.message.referenced_message != None:
        print(context.event.message.referenced_message.content)
    else:
        print("No reply found")
    #message = await context.channel.fetch_message(context.message.reference.message_id)
    #await context.send(message.content)

celebQuoteFile = "./QuoteStore/famousquotes.txt"
celebdatabase = open(celebQuoteFile)
celebquotearray = celebdatabase.readlines()
celebdatabase.close

def getCelebQuote():
    quoteArrayLen = len(celebquotearray)
    randIndex = random.randrange(0, (quoteArrayLen), 2)
    quoteText = celebquotearray[randIndex]
    quoteAuthor = celebquotearray[randIndex + 1]
    finalQuote = "> " + quoteText + "        - *" + quoteAuthor.strip() + "*"
    return finalQuote
    

@bot.command
@lightbulb.command('celebquote', 'Print a famous quote.', aliases=["famousquote"])
@lightbulb.implements(lightbulb.PrefixCommand)
async def celebquote(context):
    # await bot.rest.create_message(context.get_channel().id, "> " + getCelebQuote())
    await bot.rest.create_message(context.get_channel().id, getCelebQuote())

# if valid event, give a reply to "quote"
# @bot.listen(hikari.GuildMessageCreateEvent)
# async def print_message(event):
#     if event != None:
#         if "quote" in event.message.content.lower():
#             #await bot.rest.create_message(event.channel_id, "Found the magic words!")
#             pass



# finally, run the bot
bot.run()
