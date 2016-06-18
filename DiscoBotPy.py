### Imports
import discord
import LoLapi
import Login
import random
from cleverbot import Cleverbot

client = discord.Client()
cb = Cleverbot()


### Functions
@client.event
def on_ready():
    print "bot online"

@client.event
def on_message(message):
    author = message.author
    if message.content.startswith("!hello"):
        hello_func(author, message)
    if message.content.startswith("!kill"):
        logout_func(author, message)
    if message.content.startswith("!rank"):
        rank_func(author, message)
    if message.content.startswith("!roll"):
        roll_func(author, message)
    if message.content.startswith("!cleverbot"):
        cleverbot_func(author, message)
    if message.content.startswith("!opgg"):
        opgg_func(author, message)
    if message.content.startswith("!commands"):
        commands_func(author, message)
    if message.content.startswith("!help"):
        help_func(author, message)
        
def hello_func(author, message):
    client.send_message(message.channel, "Hello %s! :D" % author)
    print "hello_func"

def logout_func(author, message):
    if str(author) != "Monster":
        client.send_message(message.channel, "Unauthorized")
        return
    client.send_message(message.channel, "Logging out, cya!")
    client.logout()
    print "logout_func"

def rank_func(author, message):
    args = message.content.split()
    size = len(args)
    if size < 3:
        msg = "Too few arguments. example: \n ```!rank wildturtle na```"
        client.send_message(message.channel, msg)
        return
    region = args[size-1].lower()
    summoner = ""
    for i in range(1,size-1):
        summoner += args[i]
    result = LoLapi.getRank(region, summoner)
    client.send_message(message.channel, result)
    print "rank_func"

def roll_func(author, message):
    result = random.randint(0,100)
    msg = str(author) + " rolled " + str(result)
    client.send_message(message.channel, msg)
    print "roll_func"

def cleverbot_func(author, message):
    msg = message.content[11:]
    result = cb.ask(msg)
    client.send_message(message.channel, result)
    print "cleverbot_func"

def opgg_func(author, message):
    args = message.content.split()
    size = len(args)
    if size < 3:
        msg = "Too few arguments. example: \n ```!opgg wildturtle na```"
        client.send_message(message.channel, msg)
        return
    region = args[size-1].lower()
    summoner = ""
    for i in range(1,size-1):
        summoner += args[i]
    result = "http://" + region + ".op.gg/summoner/userName=" + summoner
    client.send_message(message.channel, result)
    print "opgg_func"

def commands_func(author, message):
    msg = "```"
    msg += "!hello \n!kill \n!rank \n!roll \n!cleverbot \n!opgg \n!commands"
    msg += "```"
    client.send_message(message.channel, msg)
    print "commands_func"

def help_func(author, message):
    msg = "Hello, I am a bot working for Monster. He is a good master :) \n"
    msg += "To see my commands, type:"
    msg += "\n`!commands`"
    client.send_message(message.channel, msg)
    print "help_func"

    
### Main   
mail = Login.mail
password = Login.password
client.login(mail, password)
client.run()

