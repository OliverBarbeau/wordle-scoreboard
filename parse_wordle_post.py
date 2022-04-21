from re import compile
def parse_wordle_post(message_content, loc):
  #print("parse_wordle_post message content:",message_content)
  #assumes location in message content is the start of wordle post.
  location = loc + 7
  wordle_number = ""
  while (compile("[0-9]").match(message_content[location]) is not None):
    wordle_number += message_content[location]
    location += 1
    #print(wordle_number)
  location += 1
  score = message_content[location]
  return [wordle_number, score]
