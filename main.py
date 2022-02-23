import os
import discord
from utils import done_task, msg_add_point, bot_command


TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(msg):
  if (str(msg.channel).endswith('-done')):
    if (msg.content.lower().startswith("done")):
      done_task(msg)
      await msg.add_reaction('👏')
  elif (str(msg.channel) == 'bot-commands'):
    response = bot_command(msg)
    await msg.add_reaction('👍')
    await client.get_channel(msg.channel.id).send(response)
  else:
    msg_add_point(msg, 1)
      
client.run(TOKEN)
