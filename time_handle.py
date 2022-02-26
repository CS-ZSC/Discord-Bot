import datetime

def get_date(date):
  return date.strftime("%d/%m/%Y")

def get_time(date):
  return date.strftime("%X")

def egypt_time_zone(date):
  return date+datetime.timedelta(hours=2)    # Egypt timezone is UTC+2

def str_day_first_second(date):
  # adding 2 hours margin so the task could be pusblished before midnight with 2 hours
  date = date+datetime.timedelta(hours=2)  
  return str(get_date(date)+" 00:00:00")

def str_day_last_second(date, duration):
  # same goes here but minus 2 hours and adding the duration
  date = date-datetime.timedelta(hours=2)+datetime.timedelta(days=duration)
  return str(get_date(date)+" 23:59:59")


def date_from_str(date_str):
  date = False
  try:
    date = datetime.datetime.strptime(date_str, "%d/%m/%Y %X")
  except:
    print(f"Failed to parse date from {date_str}")
  return date
