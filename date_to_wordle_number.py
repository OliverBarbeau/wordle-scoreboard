from datetime import date, timedelta

from pandas import Timedelta

def date_to_wordle_number(validate_date : date) :
    first_wordle_date = date(2021, 6, 19)
    days_between = validate_date - first_wordle_date
    #days_between : int = days_between.days
    days_between = int(days_between.days)
    return days_between
# print(date_to_wordle_number(date(year=2022,month=4,day=20)))





    
    
