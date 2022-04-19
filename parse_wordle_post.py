from re import match
def parse_wordle_post(message_content):
  #assumes location in message content is the start of wordle post.
  location = 7
  wordle_number = ""
  while match(message_content[location], "[1-9]"):
    wordle_number += message_content[location]
    location += 1
    print(wordle_number)
  location += 1
  score = message_content[location]
  return [wordle_number, score]
