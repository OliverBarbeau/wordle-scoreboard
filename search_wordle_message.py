from re import search, compile
# return string search match location of regular expression match, for a wordle score post pattern
def search_wordle_message(message_content):
  #print("search_wordle_message is:", message_content)
  # ex. "Wordle 291 4/6"
  #     "Wordle "+[any string of numerical character]+" "+[a single digit 1-6]+"/6"
  pattern = compile("(Wordle) [0-9]+ [1-6, X]\/[6]")
  #return first location in the message
  match_obj = pattern.search(message_content)
  if match_obj is not None:
    return match_obj.start(0)
  
  return None


# message = "Wordle 283 5/6*"


# print(search_wordle_message(message))




