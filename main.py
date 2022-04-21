import discord
from datetime import datetime, timedelta
from discord.ext import commands, tasks
from asyncio import sleep
from get_scoreboard import get_scoreboard
from os import environ
from os.path import exists

# from table2ascii import table2ascii
#^ basic imports for other features of discord.py and python
import secret
#^ internal project function imports ^

client = discord.Client()

client = commands.Bot(command_prefix = '!') #put your own prefix here

@client.event
async def on_ready():
  print(f"{client.user} logged in!") # will print "bot online" in the console when the bot is online
  schedule_weekly_messages.start()

@client.command()
async def ping(ctx):
  await ctx.channel.send("pong!")
#print(dir(message))

@client.command()
async def d(ctx):
  await ctx.msg.delete()

@client.command()
async def scoreboard(ctx): # primary user command
  scoreboard_message = await get_scoreboard(ctx.channel, client.user) 
  await ctx.channel.send(scoreboard_message)

@tasks.loop(hours=7*24)
async def schedule_weekly_messages():
  while True:
    now = datetime.now()
    then = now + timedelta(days=7)
    then = then.replace(hour=0, minute=0, second=0, microsecond=0)
    #then = now.replace(hour=5, minute=29, second=0, microsecond=0)
    wait_time = (then-now).total_seconds()
    print('weekly messages scheduled, sleeping for: ' + str(wait_time))
    channel = client.get_channel(965658295715115123)
    await sleep(wait_time)
    scoreboard_message = await get_scoreboard(channel, client.user) 
    sent_message = await channel.send(scoreboard_message)
    print(sent_message)


my_secret = ""
if exists('secret.py'):
  environ['TOKEN'] = secret.TOKEN  # local enviroment secret key access
try:
  my_secret = environ['TOKEN'] # replit secret key access
except KeyError:
  pass

if my_secret != "":
  client.run(my_secret) 
else:
  print("no secret key found!")
# 