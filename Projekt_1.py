
import discord
import random
import os
 
client = discord.Client()

@client.event
async def on_ready():
   print('We have logged in as {0.user}'.format(client))
 
@client.event
async def on_message(message):
   if message.author == client.user:
       return
 
   if message.content.startswith('Hej'):
       await message.channel.send('Hallå!')
   elif 'Bye' in message.content:
       await message.channel.send('')

client.run('OTQwMjI2MjY0NTU4NjI0Nzc4.YgET8g.oC9F7tyOmU7dO5aOdOA4CEnOnoQ')