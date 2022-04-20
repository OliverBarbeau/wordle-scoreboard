import discord
import os
from datetime import date, datetime, timedelta
from discord.ext import commands
from tabulate import tabulate
# from table2ascii import table2ascii
#^ basic imports for other features of discord.py and python
from get_user_scores_data import get_user_scores_data
import secret
#^ internal project function imports ^

client = discord.Client()

client = commands.Bot(command_prefix = '!') #put your own prefix here

@client.event
async def on_ready():
  print(f"{client.user} logged in!") #will print "bot online" in the console when the bot is online


@client.command()
async def ping(ctx):
  await ctx.channel.send("pong!")
#print(dir(message))
@client.command()
async def scoreboard(ctx):
  #defaulting to get messages after the most recent sunday at midnight.
  # date_limit = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) daily
  date_limit = (datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)) - timedelta(date.today().weekday()) #weekly reset on sunday
  message_count_limit = 1000
  messages = await ctx.channel.history(limit=message_count_limit,after=date_limit).flatten()
  #print(type())
  data = get_user_scores_data(client.user, messages)
  if len(data) == 0:
    await ctx.channel.send("No submissions were made this week!")
    pass
  players = data["player"].value_counts()
  print(players.head())
  print(type(players))


  players = [i for (i,j) in players.items()]
  print(players)
  #for each user that posted any wordle submission in the limit and timeframe prespecified:
  player_summaries = []
  for player in players:
    #print(player)
    player_data = data.loc[data['player'] == player]
    print("player data:\n", player_data)
    print("player data type:\n", type(player_data), "length: ", len(player_data))
    score_sum = 0
    wins = 0
    submissions = 0
    for i in range(len(player_data)):
      if player_data.iloc[i,3] == True:
        wins += 1
        score_sum += int(player_data.iloc[i,1])
      submissions += 1
    avg_score = score_sum/wins
    player_summaries.append({"player":player, "wins":wins, "submissions":submissions, "avg_score":avg_score})
  
    #  calculate number of submissions
    #  calculate average score among submissions
    #  add user summary data to ranked list
  # sort the players by average score
  print(player_summaries)
  player_summaries.sort(key=lambda x: x["avg_score"])
  # sort the players by wins recorded
  print(player_summaries)
  player_summaries.sort(key=lambda x: x["wins"], reverse=True)
  print(player_summaries)
  # column_titles = [{"player":'player', "avg_score":'avg_score', "wins":'wins', "submissions":'submissions'}]
  # print(column_titles)
  placed = 1
  for player_summary in player_summaries:
    player_summary['placed'] = placed
    placed += 1


  #order = ["placed","player","avg_score","wins","submissions"]
  player_summaries = [[player_summary["placed"],player_summary["player"],player_summary["avg_score"], player_summary["wins"], player_summary["submissions"]] for player_summary in player_summaries]
  scoreboard_message = f'>>> `​`​`​\n{tabulate(player_summaries, headers=("placed","player","avg_score","wins","submissions"), tablefmt="fancy_grid")}\n`​`​`​' # sorted_stocks is a dict

  #send message
  await ctx.channel.send(scoreboard_message)
  
  

client.run(secret.TOKEN) 



# 