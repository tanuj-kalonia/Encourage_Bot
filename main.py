import discord
import os
import requests # to make a request to the API
import json # to parse the response
import random # to generate a random number
from replit import db # to store data in the database
from keep_alive import keep_alive

client = discord.Client()
# bot always listens to events triggerd by user 

sad_words = ["sad", "depressed", "unhappy", "angry", "miserable"]
starter_encouragements = [
    "Cheer up!",
    "Hang in there.",
    "You are a great person / bot!"
    "This too will pass."
]
if "responding" not in db.keys():
    db["responding"] = True

def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)

    # json_data is a list of dictionaries
    # json_data[0] is a dictionary and it has two keys 'q' and 'a'
    # json_data[0]['q'] is the quote and json_data[0]['a'] is the author
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return(quote)

# if the user wants to add an encouragement
def update_encouragements(encouraging_message):
    if "encouragements" in db.keys():
        encouragements = db["encouragements"]
        encouragements.append(encouraging_message)
        db["encouragements"] = encouragements
    else:
        db["encouragements"] = [encouraging_message]

# if the user wants to delete an encouragement
def delete_encouragement(index):
    encouragements = db["encouragements"]
    if len(encouragements) > index:
        del encouragements[index]
        db["encouragements"] = encouragements


# on_ready fun will be triggerd whenever the bot is ready
@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

# on_message fun will be triggerd whenever the bot receives a message
@client.event
async def on_message(message):  
    # if the message is sent by the bot itself, then it will return
    if message.author == client.user:
        return
    
    msg = message.content
    # if the message starts with $inspire, then it will send a quote
    if msg.startswoth('$inspire'):
        quote = get_quote()
        await message.channel.send(quote)
    
    # if the message starts with $responding, then it will change the value of responding in the database
    if db["responding"]:
        options = starter_encouragements
        if "encouragements" in db.keys():
            options = options + db["encouragements"]

        # if the message contains any of the sad words, then it will send a random encouragement
        if any(word in msg for word in sad_words):
            await message.channel.send(random.choice(starter_encouragements))
    
    # if the message starts with $new, then it will add the message to the database
    if msg.startswith("$new"):
        encouraging_message = msg.split("$new ",1)[1]
        update_encouragements(encouraging_message)
        await message.channel.send("New encouraging message added.")

    # if the message starts with $del, then it will delete the message from the database
    if msg.startswith("$del"):
        encouragements = []
        if "encouragements" in db.keys():
            index = int(msg.split("$del",1)[1])
            delete_encouragement(index)
            encouragements = db["encouragements"]
        await message.channel.send(encouragements)
    
    # if the message starts with $list, then it will list all the encouragements
    if msg.startswith("$list"):
        encouragements = []
        if "encouragements" in db.keys():
            encouragements = db["encouragements"]
        await message.channel.send(encouragements)
    
    # if the message starts with $responding, then it will change the value of responding in the database
    if msg.startswith("$responding"):
        value = msg.split("$responding ",1)[1]

        if value.lower() == "true":
            db["responding"] = True
            await message.channel.send("Responding is on.")
        else:
            db["responding"] = False
            await message.channel.send("Responding is off.")

keep_alive()
client.run(os.getenv('TOKEN'))
