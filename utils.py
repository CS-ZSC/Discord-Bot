from googlesheet import insert_task_done, add_points_to, add_deadline
from time_handle import egypt_time_zone, get_day, get_hour, str_day_first_second, str_day_last_second

def done_task(msg):
  task = str(get_task_number(msg.content))
  author = str(msg.author.name+" #" + msg.author.discriminator)
  time_zoned_date = egypt_time_zone(msg.created_at)
  created_at =  str(get_year(time_zoned_date)+" " + get_time(time_zoned_date))
  track = str(msg.channel.category.name).lower()
  if (track == "science tasks"):
    if (str(msg.channel) == 'science-tasks-done'):
      track = 'science-tasks'
    elif (str(msg.channel) == 'competitor-done'):
      track = 'competitor-tasks'
    else:
      return
  insert_task_done(track, author, task, created_at)

def msg_add_point(msg, number_of_points):
  author = str(msg.author.name+" #" + msg.author.discriminator)
  add_points_to(author, number_of_points)


def bot_command(msg):
  command = str(msg.content)
  print(command)
  track, _, task_number, _, duration = command.split(" ")
  duration = int(duration)
  task_number = int(task_number)
  time_zoned_date = egypt_time_zone(msg.created_at)
  starting_time = str_day_first_second(time_zoned_date)
  ending_time = str_day_last_second(time_zoned_date, duration)
  track = track.lower()
  return add_deadline(track, task_number, starting_time, ending_time)
