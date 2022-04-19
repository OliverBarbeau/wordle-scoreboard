import discord
import os
from datetime import date, datetime, timedelta
from discord.ext import commands
#^ basic imports for other features of discord.py and python
import get_user_scores_data
#^ internal project function imports ^

client = discord.Client()

client = commands.Bot(command_prefix = '!') #put your own prefix here

@client.event
async def on_ready():
  print(f"{client.user} logged in!") #will print "bot online" in the console when the bot is online
  
#print(dir(message))
@client.command()
async def scoreboard(ctx):
  #defaulting to get messages after the most recent sunday at midnight.
  date_limit = (datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)) - timedelta(date.today().weekday())
  message_count_limit = 10000
  messages = ctx.channel.history(limit=message_count_limit,after=date_limit)
  data = get_user_scores_data(messages)
  players = [i for (i, j) in data["player"].value_counts()]
  #for each user that posted any wordle submission in the limit and timeframe prespecified:
  player_sumarries = []
  for player in players:
    player_data = data[data['player'] == player]
    sum = 0
    wins = 0
    submissions = 0
    for row in player_data:
      if row['win'] == True:
        wins += 1
        sum += row['score']
      submissions += 1

    
    player_sumarries.append((player, wins, submissions, sum/wins))
    
    
    
    #  calculate number of submissions
    #  calculate average score among submissions
    #  add user summary data to ranked list
  await ctx.channel.send(player_sumarries)
  
  

client.run(os.getenv("TOKEN")) 



# 