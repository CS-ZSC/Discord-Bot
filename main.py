import os
from discord.ext import commands
from discord import Intents
from discord_slash import SlashCommand

import utils

TOKEN = os.getenv('DISCORD_TOKEN')

client = commands.Bot(command_prefix="/")
slash = SlashCommand(client,sync_commands=True)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(msg):
  if (str(msg.channel).endswith('-done')):
    if (msg.content.lower().startswith("done")):
      await utils.done_task(msg, announce)
      await msg.add_reaction('👏')
  elif (not str(msg.channel).startswith('bot')):      
  # this is dumb. but easier to handle for future use like giving user more points when he shares in core-cs or some science-related channel
    await utils.msg_add_point(msg, announce)
    

async def announce(msg):
  channel = client.get_channel(946152947631403058)
  await channel.send(msg)
  

utils.load_cogs(client)
client.run(TOKEN)
