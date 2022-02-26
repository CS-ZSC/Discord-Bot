import gspread
gc = gspread.service_account(filename='./creds.json')
sh = gc.open("Copy of CS 22")
announce_author_points = 50

def user_cell_of_sheet(sheet, discord_name):
  cell = sheet.find(discord_name)
  if (cell):
    return (cell.row, cell.col)
  return 1, 1
  

def insert_task_done(track, author, task_number, created_at):
  sheet = sh.worksheet(track)
  user_row, user_col = user_cell_of_sheet(sheet, author)
  if (user_row == 0 and user_col == 0): #Not found
    print("Failed to add done task, probably the author doesn't exist in the sheet")
    return
  task_col = user_col + int(task_number)
  sheet.update_cell(user_row, task_col, "Done " + created_at)
  print(f"row inserted for {author}, task {task_number}, track {track}")

def add_points_to(author, number_of_points):
  sheet = sh.worksheet("points")
  user_row, user_col = user_cell_of_sheet(sheet, author)
  if (user_row == 1 and user_col == 1): #Not found
    print("Failed to add point, probably the author doesn't exist in the sheet")
    return
  points_col = user_col + 1
  old_points = int(sheet.cell(user_row, points_col).value)
  new_points = old_points + number_of_points    
  sheet.update_cell(user_row, points_col, str(new_points))
  print(f"Added {number_of_points} points to {author}")
  return old_points, new_points
  
def get_author_points(author):
  sheet = sh.worksheet("points")
  user_row, user_col = user_cell_of_sheet(sheet, author)
  if (user_row == 1 and user_col == 1): #Not found
    print("Failed to get author point, probably the author doesn't exist in the sheet")
    return
  points_col = user_col + 1
  points = sheet.cell(user_row, points_col).value
  if (points):
    return points
  else:
    print("Failed to get author point, probably cell is clear (doesn't contain 0)")
  return None
  
def add_deadline(track, task_number, starting_time, ending_time):
  try:
    sheet = sh.worksheet(track+'_DL')
    task_row = task_number+1
    task_col = 1
    sheet.update_cell(task_row, task_col, str(task_number))
    sheet.update_cell(task_row, task_col+1, starting_time)
    sheet.update_cell(task_row, task_col+2, ending_time)
  except:
    return False
  return True

def get_task_start_end_date_str(track, task_number):
  #try:
    sheet = sh.worksheet(track+'_DL')
    task_row = int(task_number)+1
    task_col = 1
    start_date_str = str(sheet.cell(task_row, task_col+1).value)
    end_date_str = str(sheet.cell(task_row, task_col+2).value)
    if (end_date_str == None or start_date_str == None):
      print("Task Deadline doesn't exist in the spreadsheet")
      return '', ''
    return start_date_str, end_date_str
  #except:
  #  return '', ''