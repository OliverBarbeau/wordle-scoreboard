import discord
# import pytz
from datetime import datetime, timedelta
from discord.ext import commands, tasks
from asyncio import sleep
from os import environ
from os.path import exists
#^ basic imports for other features of discord.py and python
import secret
from get_scoreboard import get_scoreboard
#^ internal project function imports ^

# default_tz = pytz.timezone('US/Central')

# class CustomHelpCommand(commands.HelpCommand):
#   def __init__(self):
#     super().__init__()
#   async def send_bot_help(self, mapping):
#     for cog in mapping:
#       await self.get_destination().send(f'{cog.qualified_name}: {[command.name for command in mapping[cog]]}')
#     # return await super().send_bot_help(mapping)
#   async def send_cog_help(self, cog):
#     await self.get_destination().send(f'{cog.qualified_name}: {[command.name for command in cog.get_commands()]}')
#     # return await super().send_cog_help(cog)
#   async def send_group_help(self, group):
#     await self.get_destination().send(f'{group.name}: {[command.name for index, command in enumerate(group.commands)]}')
#     # return await super().send_group_help(group)
#   async def send_command_help(self, command):
#     await self.get_destination().send(command.name)
#     # return await super().send_command_help(command)
  

client = discord.Client()
# client = commands.Bot(command_prefix = '!', help_command=CustomHelpCommand())
client = commands.Bot(command_prefix = '!')

@client.event
async def on_ready():
  print(f"{client.user} logged in!") # will print "bot online" in the console when the bot is online
  schedule_weekly_messages.start()

@client.command()
async def ping(ctx):
  await ctx.channel.send("pong!")
#print(dir(message))

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
    print('weekly messages scheduled, sleeping for: ' + str(timedelta(seconds=wait_time)))
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
