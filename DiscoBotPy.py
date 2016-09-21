### Imports
import discord
import LoLapi
import Login
import random
import requests
import time, datetime
from cleverbot import Cleverbot
import TwitterScanner
import urllib2

client = discord.Client()
cb = Cleverbot()

# Starttime of bot. Used by !uptime
startTime = datetime.datetime.now()

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
    if message.content.startswith("!twitch"):
        twitch_func(author, message)
    if message.content.startswith("!uptime"):
        uptime_func(author, message)
    if message.content.startswith("!pogo"):
        pogo_func(author, message)
    if message.content.startswith("!imdb"):
        imdb_func(author, message)
    if message.content.startswith("!yt"):
        youtube_func(author, message)
    if message.content.startswith("!youtube"):
        youtube_func(author, message)
    if message.content.startswith("!code"):
        code_func(author, message)
    if message.content.startswith("!dick"):
        dick_func(author, message)
        
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
    msg += "!hello \n!kill \n!rank \n!roll \n!cleverbot \n!opgg"
    msg += "\n!twitch \n!uptime \n!pogo \n!commands"
    msg += "```"
    client.send_message(message.channel, msg)
    print "commands_func"

def help_func(author, message):
    msg = "Hello, I am a bot working for Monster. He is a good master :) \n"
    msg += "To see my commands, type:"
    msg += "\n`!commands`"
    client.send_message(message.channel, msg)
    print "help_func"

def twitch_func(author, message):
    m = message.content.split()
    if len(m) <= 1:
        print "twitch_func: no argument"
        msg = "Needs 1 argument. ex: `!twitch Dekar173`"
        client.send_message(message.channel, msg)
        return
    streamer = m[1]
    url = "https://api.twitch.tv/kraken/streams/" + streamer
    response = requests.get(url)
    json = response.json()
    try:
        if json["stream"] == None:
            msg = "twitch.tv/" + streamer + " is **offline**"
        else:
            msg = "twitch.tv/" + streamer + " is **online**"
        print "twitch_func"
    except:
        msg = "twitch.tv/" + streamer + " doesn't exist"
        print "twitch_func json (try) error"
    client.send_message(message.channel, msg)

def uptime_func(author, message):
    now = datetime.datetime.now()
    hour = now.hour - startTime.hour
    if hour < 0:
        hour += 24
    minute = now.minute - startTime.minute
    if minute < 0:
        minute += 60
        hour -= 1
    second = now.second - startTime.second
    if second < 0:
        second += 60
        minute -= 1
    msg = "uptime: " + str(hour) + "h" + str(minute) + "m" + str(second) + "s"
    client.send_message(message.channel, msg)
    print "uptime_func"

def imdb_func(author, message):
    movieTitle = message.content[6:]
    url = "http://www.omdbapi.com/?t=" + movieTitle + "&y=&plot=short&r=json"
    r = requests.get(url)
    json = r.json()
    if json["Response"] == "True":
        title = json["Title"]
        year = json["Year"]
        rating = json["imdbRating"]
        # ghetto fix ascii character problem when printing
        if len(year) == 9:
            year = year[:4] + "-" + year[5:]
        elif len(year) == 5:
            year = year[:4] + "-"
        msg = title + "\n" + year + "\n" + rating
        decoded_string = msg.decode('string_escape')
        client.send_message(message.channel, msg)
    else:
        print "imdb response false (" + movieTitle + ")"
        client.send_message(message.channel, json["Error"])

def pogo_func(author, message):
    url = "https://twitter.com/PokemonGBG"
    tweets = TwitterScanner.url2tweets(url)
    msg = ""
    for tweet in tweets:
        if tweet not in cachedTweets:
            if "all" in pokemonsToScan:
                cachedTweets.append(tweet)
                msg += tweet + "\n"
            else:
                for pokemon in pokemonsToScan:
                    if tweet.startswith(str(pokemon)):
                        cachedTweets.append(tweet)
                        msg += tweet + "\n"               
    if msg != "":
        client.send_message(message.channel, msg)
        print "pogo_func"
    else:
        print "pogo_func (empty)"

cachedTweets = []
pokemonsToScan = ["all", "Dragonite", "Porygon"]

def youtube_func(author, message):
    m = message.content.split()
    if len(m) <= 1:
        client.send_message(message.channel, "No arguments")
        print "yt_func (no arguments)"
        return
    keywords = m[1:]
    searchString = ""
    for word in keywords:
        searchString += str(word) + "+"
    searchString = searchString[:-1]
    url = "https://www.youtube.com/results?search_query=" + searchString
    tag = 'data-context-item-id="'
    response = urllib2.urlopen(url)
    html = response.read()
    pos_start = html.find(tag) + len(tag)
    pos_end = html.find('"', pos_start)
    video_id = html[pos_start:pos_end]
    video_url = "http://www.youtube.com/watch?v=" + video_id
    client.send_message(message.channel, video_url)
    print "yt func"

def dick_func(author, message):
    r = random.randint(0, 10)
    d = "8" + r * "=" + "D"
    client.send_message(message.channel, d)

def code_func(author, message):
    msg = "https://github.com/MonsterMannen/discordbot"
    client.send_message(message.channel, msg)

### Main   
mail = Login.mail
password = Login.password
client.login(mail, password)
client.run()

