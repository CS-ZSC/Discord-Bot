import gspread

gc = gspread.service_account(filename='./creds.json')
sh = gc.open("Testing Bot")


def get_cell_of_sheet(sheet, discord_name, task_number):
  cell = sheet.find(discord_name)
  return (cell.row, cell.col+2+int(task_number))

def insertRow(track, author, task_number, created_at):
  sheet = sh.worksheet(track.lower())
  user_row, task_col = get_cell_of_sheet(sheet, author, task_number)
  sheet.update_cell(user_row, task_col, "Done " + created_at)
  print(f"row inserted for {author}, task {task_number}")
