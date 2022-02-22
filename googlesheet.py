import gspread

gc = gspread.service_account(filename='./creds.json')
sh = gc.open("CS 22")


def get_cell_of_sheet(sheet, discord_name, task_number):
  cell = sheet.find(discord_name)
  return (cell.row, cell.col+int(task_number))

def insertRow(track, author, task_number, created_at):
  sheet = sh.worksheet(track)
  user_row, task_col = get_cell_of_sheet(sheet, author, task_number)
  if (user_row == 1 and task_col == 1): #Not found
    print("Failed to updated row, probably the author doesn't exist in the sheet")
    return
  sheet.update_cell(user_row, task_col, "Done " + created_at)
  print(f"row inserted for {author}, task {task_number}, track {track}")
