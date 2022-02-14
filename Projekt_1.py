
import discord
import os
import urllib.request
import json
 
client = discord.Client()

@client.event
async def on_ready():
   print('We have logged in as {0.user}'.format(client))
 
@client.event
async def on_message(message):
   if message.author == client.user:
       return
 
   if message.content.startswith('Hur blir vädret?'):
       await message.channel.send('Var och när menar du?')
   elif 'Bye' in message.content:
       await message.channel.send('')


       #översätta svensk tid till coordinated universal time
       #hitta rätt koordinater utifrån vilken plats som väljs
       #leta i API

client.run('')

