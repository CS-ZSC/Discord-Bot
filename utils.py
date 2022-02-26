import os
#from googlesheet import insert_task_done, add_points_to, add_deadline, get_task_start_end_date_str
import googlesheet
from time_handle import egypt_time_zone, get_date, get_time, str_day_first_second, str_day_last_second, date_from_str

#Constants
_ANNOUNCE_WHEN = 50
_MSG_POINT = 1
_SCIENCE_MSG_POINT = 5
_TASK_POINT_INITAL = 100
_TASK_BONUS_RATIO = 0.5
_TRACK_SICIENCE_CHANNELS = ['math', 'machine-learnig', 'android', 'flutter', 'main-concepts', 'front-end', 'back-end', 'blogs-and-podcasts']


def load_cogs(client):
  print("Loading cogs...")
  for dir in os.listdir("modules"):
    if os.path.exists(os.path.join("modules", dir, "cog.py")):
      client.load_extension(f'modules.{dir}.cog')
      print(f'Loaded {dir} cog!')
  print("Done loading all cogs.")

def get_task_number(msgContent):
  return msgContent.split("-")[-1].split(" ")[-1]


def test_if_announce(old_points, new_points):
  if (new_points // _ANNOUNCE_WHEN > old_points // _ANNOUNCE_WHEN):
    return True
  return False
  
def calculate_task_points(start_date, end_date, submit_date, initial, bonus):
  '''
    Task points: initial*(1-bonus) <= points <= initial*(1+bonus)
  '''
  seconds_from_start = (submit_date - start_date).total_seconds()
  seconds_from_end = (end_date - submit_date).total_seconds()    # Would be negative if he submitted after end_date
  
  duration = (end_date - start_date).total_seconds()
  points = initial * (1 + seconds_from_end/(duration/2) * bonus)
  points = min(points, initial*(1+bonus))
  points = max(points, initial*(1-bonus))
  points = int(points)

  return points

  
async def done_task(msg, announce):
  task_number = str(get_task_number(msg.content))
  author = str(msg.author.name+ " #" + msg.author.discriminator)
  time_zoned_date = egypt_time_zone(msg.created_at)
  created_at =  str(get_date(time_zoned_date) + " " + get_time(time_zoned_date))
  track = str(msg.channel.category.name).lower()
  if (track == "science tasks"):
    if (str(msg.channel) == 'science-tasks-done'):
      track = 'science-tasks'
    elif (str(msg.channel) == 'competitor-done'):
      track = 'competitor-tasks'
    else:
      print("Unrocognized channel")
      return
  
  task_start_date, task_end_date = get_task_start_end_date(track, task_number)
  if (task_end_date and task_start_date):
    task_points = calculate_task_points(task_start_date, task_end_date, time_zoned_date, _TASK_POINT_INITAL, _TASK_BONUS_RATIO)
    old_points, new_points = googlesheet.add_points_to(author, task_points)
    if (test_if_announce(old_points, new_points)):
      await announce(f"{msg.author.mention} you have {new_points} points now, yay") 
  else:
    print("Can't get start date or end date, done_task aborted")
    return
  
  googlesheet.insert_task_done(track, author, task_number, created_at)


def get_task_start_end_date(track, task_number):
  start_date_str, end_date_str = googlesheet.get_task_start_end_date_str(track, task_number)
  end_date = date_from_str(end_date_str)
  start_date = date_from_str(start_date_str)
  return start_date, end_date


async def msg_add_point(msg, announce):
  '''
    Ok that is a stupid approach, I agree. Having the function announce in every call to add points and checking if he exceeded some limit isn't the best idea. but it kinda works (also I tried to implement it other ways but it resulted in circular imports and it kinda didn't work as I wanted so so this is a temperary solution)
  '''
  author = str(msg.author.name+" #" + msg.author.discriminator)
  category = str(msg.channel.category.name).lower()
  channel = str(msg.channel.name).lower()
  if (category == 'core cs' or category == 'cs media' or channel in _TRACK_SICIENCE_CHANNELS):
    old_points, new_points = googlesheet.add_points_to(author, _SCIENCE_MSG_POINT)
  else:
    old_points, new_points = googlesheet.add_points_to(author, _MSG_POINT)
    
  if (test_if_announce(old_points, new_points)):
    await announce(f"{msg.author.mention} you have {new_points} points now, yay") 
  
def bot_command(msg):
  command = str(msg.content)
  print(command)
  track, _, task_number, _,  duration = command.split(" ")
  duration = int(duration)
  task_number = int(task_number)
  time_zoned_date = egypt_time_zone(msg.created_at)
  starting_time = str_day_first_second(time_zoned_date)
  ending_time = str_day_last_second(time_zoned_date, duration)
  track = track.lower()
  return googlesheet.add_deadline(track, task_number, starting_time, ending_time)
