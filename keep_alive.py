# This file is used to keep the bot alive on repl.it
# repl.it will shut down the bot if it doesn't receive any requests for 5 minutes
# so we will use this file to keep the bot alive

# dont worry if you don't understand this code. This is just to keep the bot alive

from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "I'm alive"

def run():
    app.run(host='0.0.0.0',port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()