from typing import List
import pandas as pd
from search_wordle_message import search_wordle_message
from parse_wordle_post import parse_wordle_post
from discord import ClientUser
from discord.message import Message
from datetime import date, datetime, timedelta # dont confuse this library with the date column or variables.
from date_to_wordle_number import date_to_wordle_number

def get_user_scores_data(user : ClientUser , user_messages : List[Message] = [], limit : int = 1000): #take a discord channel, and retrieves valid wordle submissions as a dataframe
  #print("get_user_scores_data called!")
  data = pd.DataFrame(columns=['wordle_number', 'score', 'player', 'win', 'date'])
  # among the messages in the channel
  for msg in user_messages: 
    #print("\nevaluating a new message")
    #print("message content:", msg.content)
    # making sure we aren't reading our own (bot) messages
    if msg.author == user:
      #print("message is from this bot!")
      continue
    #print("message is from a real user!")
    # determine if message content is a wordle score post.
    # search_wordle_message()
    location = search_wordle_message(str(msg.content))
    #print("location:", location)
    if (location is not None):
      print("found a wordle submission!")
      # print(msg.content)
      # parse the message content for the the wordle number and the score
      # (wordle_number, score)
      wordle_submission_data = parse_wordle_post(msg.content, location)
      print("wordle_submission_data:",wordle_submission_data)
      wordle_number = wordle_submission_data[0]
      print("wordle_number:",wordle_number)
      score = wordle_submission_data[1]
      print("score:",score)
      win = True
      if score == "X":
        score = 0
        win = False

      msg_created_at = (msg.created_at - timedelta(hours= 5)) # changing to my timezone 
      print("msg.created_at:", msg_created_at)
      msg_date = msg_created_at.date().strftime("%m-%d-%Y")
      player_submission_dict = {'wordle_number': int(wordle_number),'score': int(score),'player': msg.author.name, 'win': win, 'date': msg_date}
      
      print("player_submission_data['player']: '" + str(player_submission_dict['player'])+"'")
      print("player_submission_data['date']: '" + str(player_submission_dict['date'])+"'")
      print("player_submission_data['win']: '" + str(player_submission_dict['win'])+"'")
      print("player_submission_data['wordle_number']: '" + str(player_submission_dict['wordle_number'])+"'")
      print("player_submission_data['score']: '" + str(player_submission_dict['score'])+"'")

      submission_date = datetime.strptime(player_submission_dict['date'], '%m-%d-%Y').date()
      wordle_number_should_be =  date_to_wordle_number(submission_date)
      date_does_not_match_wordle_number = bool( wordle_number_should_be != player_submission_dict['wordle_number']) # dont add the data if the date and the wordle number dont align to the known wordle number
      print("date_does_not_match_wordle_number: ", date_does_not_match_wordle_number)
      sub_data = data.loc[data['player'] == player_submission_dict['player']] # retrieve submissions from this player
      sub_data = sub_data.loc[sub_data['wordle_number'] == player_submission_dict['wordle_number']] # retrieve submissions from this player with this wordle number
      entry_already_exists = bool(len(sub_data) != 0)
      print("entry_already_exist: ", entry_already_exists)
      if not (date_does_not_match_wordle_number or  (entry_already_exists)): # none of of these conditions should be True to include data
        player_submission_data = pd.DataFrame({'wordle_number': [int(wordle_number)],'score': [int(score)],'player': [msg.author.name], 'win': [win], 'date': [msg_date]})
        # player_submission_data = pd.DataFrame(player_submission_dict, index=None)
        print('Recording data')
        data = pd.concat([data, player_submission_data], ignore_index=True, axis=0)
      else:
        print('NOT Recording data')
      # dont add the data if an entry exists with a matching 'player' and 'wordle_number'
      # ((df['A'] == 2) & (df['B'] == 3)).any()
  return data

        