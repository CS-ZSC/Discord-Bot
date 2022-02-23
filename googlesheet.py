import gspread

gc = gspread.service_account(filename='./creds.json')
sh = gc.open("Copy of CS 22")

def user_cell_of_sheet(sheet, discord_name):
  cell = sheet.find(discord_name)
  return (cell.row, cell.col)

def insert_task_done(track, author, task_number, created_at):
  sheet = sh.worksheet(track)
  user_row, user_col = user_cell_of_sheet(sheet, author)
  if (user_row == 1 and user_col == 1): #Not found
    print("Failed to add done task, probably the author doesn't exist in the sheet")
    return
  task_col = user_col + int(task_number)
  sheet.update_cell(user_row, task_col, "Done " + created_at)
  add_points_to(author, 20)
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
  print(f"Added {number_of_points} to {author}")

def add_deadline(track, task_number, starting_time, ending_time):
  sheet = sh.worksheet(track+'_DL')
  task_row = task_number+1
  task_col = 1
  sheet.update_cell(task_row, task_col, str(task_number))
  sheet.update_cell(task_row, task_col+1, starting_time)
  sheet.update_cell(task_row, task_col+2, ending_time)
  response = f"added {task_number} in {track} from {starting_time} to {ending_time}"
  print(response)
  return response
