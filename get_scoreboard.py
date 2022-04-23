from datetime import date, datetime, timedelta, tzinfo
from construct_scoreboard_message import construct_scoreboard_message
from date_to_wordle_number import date_to_wordle_number
from get_user_scores_data import get_user_scores_data
from discord import User, TextChannel
import pytz
default_tz = pytz.timezone('US/Central')

async def get_scoreboard(channel: TextChannel, user: User):
  now_tz = datetime.now(tz=default_tz)
  date_limit_tz = now_tz.replace(hour=0, minute=0, second=0, microsecond=0) - (timedelta(date.today().weekday()) + timedelta(days=1)) #weekly reset on sunday
  now = now_tz.replace(tzinfo=None)
  date_limit = date_limit_tz.replace(tzinfo=None)



  message_count_limit = 1000
  messages = await channel.history(limit=message_count_limit,after=date_limit).flatten()
  data = get_user_scores_data(user, messages) # player wordle submissions as a dataframe
  if len(data) == 0:
    await channel.send("No submissions were made this week!")
    pass
  players = data["player"].value_counts() # get number of unique players this week
  players = [k for (k,v) in players.items()]
  #print(players)
  this_weeks_first_wordle_number = date_to_wordle_number(date_limit.date())
  todays_wordle_number = date_to_wordle_number(now.date())
  completed_days_this_week = todays_wordle_number - this_weeks_first_wordle_number
  player_score_dict_template = {this_weeks_first_wordle_number+i:"-" for i in range(completed_days_this_week)}
  player_score_dict_template.update({this_weeks_first_wordle_number+completed_days_this_week+i:"_" for i in range(7-completed_days_this_week)})
  player_summaries = []
  for player_name in players: #for each player that posted any wordle submission under the message count limit and timeframe specified
    player_score_dict = player_score_dict_template.copy()
    # print(this_weeks_wordle_numbers)
    #print(player)
    player_data = data.loc[data['player'] == player_name]
    #print("player data:\n", player_data)
    #print("player data type:\n", type(player_data), "length: ", len(player_data))
    score_sum = 0
    wins = 0 # count number of wins
    submissions = 0 #  count number of submissions
    for i in range(len(player_data)):
      
      if player_data.iloc[i,3] == True: # check that player won in this submission
        wins += 1
        score = int(player_data.iloc[i,1])
        score_sum += score
        wordle_number = int(player_data.iloc[i, 0])
        player_score_dict[wordle_number] = score

      else:
        player_score_dict[wordle_number] = "X"
      submissions += 1
    avg_score = score_sum/wins #  calculate mean score among winning submissions
    player_record_string = ' '.join([str(v) for k,v  in sorted(player_score_dict.items())])
    player_summaries.append({"player":player_name, "wins":wins, "submissions":submissions, "avg_score":avg_score, "record": player_record_string}) # add player summary data to list
  # print(player_summaries)
  player_summaries.sort(key=lambda x: x["avg_score"])   # sort the players by average score
  #print(player_summaries)
  player_summaries.sort(key=lambda x: x["wins"], reverse=True) # sort the players by wins recorded
  #print(player_summaries)
  placed = 1
  for player_summary in player_summaries:
    player_summary['placed'] = placed
    placed += 1
  #order = ["placed","player","avg_score","wins","submissions"]
  player_summaries = [[player_summary["placed"],player_summary["player"],player_summary["avg_score"], player_summary["wins"], player_summary["submissions"], player_summary["record"]] for player_summary in player_summaries]
  # say what day this scoreboard started on
  # f"{now:%Y-%m-%d}"
  date_limit_string = f'{(date_limit_tz):%m-%d-%Y}'
  week_of_string = 'week of ' + date_limit_string
  player_summary_data_headers = ["placed","player","avg_score","wins","submissions","S M T W T F S"]
  ends_in = (((date_limit) + timedelta(7)) - (now-timedelta(microseconds= now.microsecond)))
  ends_in = ' weekly scoreboard closes in: ' + (str(ends_in))
  scoreboard_message = construct_scoreboard_message(text_header=week_of_string, data_headers=player_summary_data_headers, data=player_summaries, text_footer=ends_in)
  print(scoreboard_message)
  return scoreboard_message