from discord.ext import commands
import googlesheet
import os

import datetime
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_choice , create_option 
from time_handle import egypt_time_zone, str_day_first_second, str_day_last_second


_SERVER_GUID = int(os.environ['DISCORD_CHANNEL_GUID'])

class Deadline(commands.Cog):

  def __init__(self, bot: commands.Bot):
    self.bot = bot

  
  @cog_ext.cog_slash(name="deadline",guild_ids=      
    [_SERVER_GUID],description="Set a deadline for a task",
                    options=[
                      create_option(name="track", description="Please choose the track", option_type=3, required=True, choices=[
                        create_choice(value="web", name="Web"),
                        create_choice(value="mobile", name="Mobile"),
                        create_choice(value="ai", name="AI")
                      ]),
                               create_option(name="duration", description="Enter a duration in days [recommended is 7 days]", option_type=4, required=True),
                               create_option(name="task_number", description="Enter The task number", option_type=4, required=True)
                    ])
  @commands.has_role("Trackhead")
  async def deadline(self,ctx: SlashContext, track, task_number, duration):
    print(ctx)
    operation = "add"
    if operation == "add":
      time_zoned_date = egypt_time_zone(datetime.datetime.now())
      starting_time = str_day_first_second(time_zoned_date)
      ending_time = str_day_last_second(time_zoned_date, int(duration))
      if googlesheet.add_deadline(track, int(task_number), starting_time, ending_time):
        await ctx.reply(f"added {task_number} in {track} from {starting_time} to {ending_time}")

  @deadline.error
  async def kick_error(self,ctx, error):
    if isinstance(error, commands.MissingRole):
      if isinstance(error , commands.MissingRole):
        message = "You are not allowed to use this command please check your role!"
        await ctx.send(message, delete_after=5)
        await ctx.message.delete(delay=5)


def setup(bot: commands.Bot):
  bot.add_cog(Deadline(bot))