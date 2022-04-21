from datetime import timedelta
from tabulate import tabulate


def construct_scoreboard_message(text_header, data_headers, data, text_footer):
  scoreboard_message = '>>> `​`​`​​'
  scoreboard_message += text_header
  scoreboard_message = f'{scoreboard_message}\n{tabulate(data, headers=data_headers, tablefmt="fancy_grid")}​\n'
  scoreboard_message += text_footer
  scoreboard_message += '`​`​`​'
  return scoreboard_message