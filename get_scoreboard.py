from datetime import date, datetime, timedelta
from construct_scoreboard_message import construct_scoreboard_message
from get_user_scores_data import get_user_scores_data
from discord import User, TextChannel

async def get_scoreboard(channel: TextChannel, user: User):
  now = datetime.now()
  # defaulting to get messages after the most recent week-start on sunday.
  # date_limit = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) daily
  date_limit = now.replace(hour=0, minute=0, second=0, microsecond=0) - (timedelta(date.today().weekday()) + timedelta(days=1)) #weekly reset on sunday
  date_limit_string = f'{(date_limit):%m-%d-%Y}'
  # date_limit = date_limit - timedelta(hours=1) # matching new york time zone from central.
  message_count_limit = 1000
  messages = await channel.history(limit=message_count_limit,after=date_limit).flatten()
  #print(type())
  data = get_user_scores_data(user, messages)
  if len(data) == 0:
    await channel.send("No submissions were made this week!")
    pass
  players = data["player"].value_counts() # get number of unique players this week


  #print(players.head())
  #print(type(players))


  players = [i for (i,j) in players.items()]
  #print(players)
  #for each user that posted any wordle submission in the limit and timeframe prespecified:
  player_summaries = []
  for player in players:
    #print(player)
    player_data = data.loc[data['player'] == player]
    #print("player data:\n", player_data)
    #print("player data type:\n", type(player_data), "length: ", len(player_data))

    # drop invalid entries i.e. the right wordle number for that date, duplicate entries
    # player_data = player_data.drop_duplicates(subset=['wordle_number'], keep='first', inplace=False, ignore_index=False) # remove duplicate entries of a wordle number
    # player_data = 
    score_sum = 0
    wins = 0
    submissions = 0
    for i in range(len(player_data)):
      
      if player_data.iloc[i,3] == True: #check that player won in this submission
        wins += 1
        score_sum += int(player_data.iloc[i,1])
      submissions += 1
    avg_score = score_sum/wins
    player_summaries.append({"player":player, "wins":wins, "submissions":submissions, "avg_score":avg_score})
  
    #  calculate number of submissions
    #  calculate average score among submissions
    #  add user summary data to ranked list
  # sort the players by average score
  #print(player_summaries)
  player_summaries.sort(key=lambda x: x["avg_score"])
  # sort the players by wins recorded
  #print(player_summaries)
  player_summaries.sort(key=lambda x: x["wins"], reverse=True)
  #print(player_summaries)
  placed = 1
  for player_summary in player_summaries:
    player_summary['placed'] = placed
    placed += 1
  #order = ["placed","player","avg_score","wins","submissions"]
  player_summaries = [[player_summary["placed"],player_summary["player"],player_summary["avg_score"], player_summary["wins"], player_summary["submissions"]] for player_summary in player_summaries]
  # say what day this scoreboard started on
  # f"{now:%Y-%m-%d}"
  week_of_string = 'week of ' + date_limit_string
  player_summary_data_headers = ["placed","player","avg_score","wins","submissions"]
  ends_in = (((date_limit) + timedelta(7)) - (now-timedelta(microseconds= now.microsecond)))
  ends_in = ' weekly scoreboard closes in: ' + (str(ends_in))
  scoreboard_message = construct_scoreboard_message(text_header=week_of_string, data_headers=player_summary_data_headers, data=player_summaries, text_footer=ends_in)
  #send message
  print(scoreboard_message)
  return scoreboard_message