from googlesheet import insertRow

def get_task_number(msgContent):
  return msgContent.split("-")[-1].split(" ")[-1]

def get_year(date):
 return date.strftime("%Y")+ "/"+ date.strftime("%m") +"/"+ date.strftime("%d")

def get_time(date):
  return date.strftime("%X")


def done_task(msg):
  task = str(get_task_number(msg.content))
  author = str(msg.author.name+" #" + msg.author.discriminator)
  created_at =  str(get_year(msg.created_at)+" " + get_time(msg.created_at))
  track = str(msg.channel.category.name).tolower()
  if (track == "science tasks"):
    if (str(msg.channel) == 'science-tasks-done'):
      track = 'science-tasks'
    elif (str(msg.channel) == 'competitor-done'):
      track = 'competitor-tasks'
    else:
      return
  insertRow(track, author, task, created_at)
