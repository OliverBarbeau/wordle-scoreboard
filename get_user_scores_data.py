import pandas as pd
from search_wordle_message import search_wordle_message
from parse_wordle_post import parse_wordle_post
def get_user_scores_data(user, user_messages = [None], limit = 10000):
  print("get_user_scores_data called!")
  data = pd.DataFrame(columns=['wordle_number', 'score', 'player', 'win'])
  # among the messages in the channel
  for msg in user_messages: 
    print("\nevaluating a new message")
    print("message content:", msg.content)
    # making sure we aren't reading our own (bot) messages
    if msg.author == user:
      print("message is from this bot!")
      continue
    print("message is from a real user!")
    # determine if message content is a wordle score post.
    # search_wordle_message()
    location = search_wordle_message(str(msg.content))
    print("location:", location)
    if (location is not None):
      print("found a wordle submission!")
      print(msg.content)
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
      data = data.append({'wordle_number': int(wordle_number),
                          'score': int(score),
                          'player': msg.author.name,
                          'win': win}, ignore_index=True)
  return data

        