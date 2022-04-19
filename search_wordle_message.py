from re import search
# return string search match location of regular expression match, for a wordle score post pattern
def search_wordle_message(message_content):
  # ex. "Wordle 291 4/6"
  #     "Wordle "+[any string of numerical character]+" "+[a single digit 1-6]+"/6"
  pattern = "(Wordle) [1-9]+ [1-6, X]\/[6]"
  #return first location in the message
  return search(message_content, pattern)




