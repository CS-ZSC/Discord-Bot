import datetime

def get_day(date):
  return date.strftime("%Y/%m/%d")

def egypt_time_zone(date):
  return date+datetime.timedelta(hours=2)    # Egypt timezone is UTC+2

def get_hour(date):
  return date.strftime("%X")

def str_day_first_second(date):
  # adding 2 hours margin so the task could be pusblished before midnight with 2 hours
  date = date +datetime.timedelta(hours=2)  
  return str(get_day(date)+" 00:00:00")

def str_day_last_second(date, duration):
  # same goes here but minus 2 hours and adding the duration
  date = date-datetime.timedelta(hours=2)+datetime.timedelta(days=duration)
  return str(get_day(date)+" 23:59:59")
