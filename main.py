import os
import discord
from utils import done_task


TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(msg):
  if (str(msg.channel) == 'tasks-done'):
    if (msg.content.lower().startswith("done")):
      done_task(msg)
      await msg.add_reaction('👏')

client.run(TOKEN)