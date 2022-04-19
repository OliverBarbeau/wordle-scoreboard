import pd

def get_user_scores_data(user_wordle_messages = [None], limit = 10000):
  print("get_user_scores_data called!")
  data = pd.DataFrame(columns=['wordle_number', 'score', 'player', 'win'])
  # among the messages in the channel
  for msg in user_wordle_messages: 
    # making sure we aren't reading our own (bot) messages
    if msg.author != client.user:
      print("message is from this bot!")
      break
    # determine if message content is a wordle score post.
    # search_wordle_message()
    if ((location := search_wordle_message(message_content)) is not None):
      print("message is from this bot!")
      # parse the message content for the the wordle number and the score
      # (wordle_number, score)
      wordle_submission_data = parse_wordle_post()
      wordle_number = wordle_submission_data[0]
      score = wordle_submission_data[1]
      win = True
      if score == "X":
        score = 0
        win = False
      data = data.append({'wordle_number': wordle_number,
                          'score': score,
                          'player': msg.author.name,
                          'win': win}, ignore_index=True)

        