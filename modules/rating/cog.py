from discord.ext import commands
#from googlesheet import get_author_points
import googlesheet
import os

import datetime
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_choice , create_option 
from time_handle import egypt_time_zone, str_day_first_second, str_day_last_second

_SERVER_GUID = int(os.environ['DISCORD_CHANNEL_GUID'])

class AuthorPoints(commands.Cog):
  def __init__(self, bot: commands.Bot):
    self.bot = bot

  @cog_ext.cog_slash(name="points",guild_ids=      
    [_SERVER_GUID],description="Get my points")
  async def points(self,ctx: SlashContext):
    author_name, author_id = str(ctx.author).split('#')
    author = author_name+' #'+author_id
    print(author)
    author_points = googlesheet.get_author_points(author)
    operation = "points"
    if operation == "points":
      await ctx.reply(f"Hello {author}, you have {author_points} points")

def setup(bot: commands.Bot):
  bot.add_cog(AuthorPoints(bot))