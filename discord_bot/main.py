import os
import json
import requests
from datetime import datetime

import discord
from table2ascii import table2ascii as t2a, PresetStyle

BOT_TOKEN = os.environ['BOT_TOKEN']
QUOTE_API = os.environ['QUOTE_API']
WEATHER_API = os.environ['WEATHER_API']
WEATHER_API_KEY = os.environ['WEATHER_API_KEY']

CMD_TOKEN = '.'
DAY_LIMIT = 7

WEEKDAY_MAP = {
  0: "Monday",
  1: "Tuesday",
  2: "Wednesday",
  3: "Thursday",
  4: "Friday",
  5: "Saturday",
  6: "Sunday"
}

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
client = discord.Client(intents=intents)

def get_quote():
  response = requests.get(QUOTE_API)
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + '\n' + "— " + json_data[0]['a']
  return quote

def get_weather(location, num):
  response = requests.get(WEATHER_API + location + WEATHER_API_KEY)
  if response:
    json_data = json.loads(response.text)
    address_data = json_data["resolvedAddress"]
    days_data = json_data["days"]

  else:
    return f"I can't find any location with {location} ..."

  days = []
  weekday = datetime.today().weekday()
    
  for count, day in enumerate(days_data):
    if count == num:
      break

    days.append([])
    days[count].append(day["datetime"])
    days[count].append(WEEKDAY_MAP[weekday])
    days[count].append("YES" if day["preciptype"] else "NO")
    days[count].append(day["tempmax"])
    days[count].append(day["tempmin"])

    weekday = (weekday + 1) % 7

  output = t2a(
    header=["Date", "Weekday", "Rain", "High Temp", "Low Temp"],
    body=days,
    style=PresetStyle.thin_compact
  )

  address = "Weather forecast at " + address_data + "\n"
  return address + f"```\n{output}\n```"

@client.event
async def on_ready():
  print(f"Logged in as {client.user}")

@client.event
async def on_message(message):
  
  if message.author == client.user:
    return

  elif message.content.startswith(CMD_TOKEN + "hello"):
    name = message.content.split(CMD_TOKEN + "hello", 1)[1].strip()
    
    if not name:
      await message.channel.send(f"Hello {message.author}!")

    else:
      await message.channel.send(f"Hello {name}!")

  elif message.content == CMD_TOKEN + "quote":
    quote = get_quote()
    await message.channel.send(quote)

  elif message.content.startswith(CMD_TOKEN + "weather"):
    split = message.content.split(" ", 2)
    if len(split) < 2:
      await message.channel.send("Please enter the location or postal code you want to query.")

    location = split[1]
    
    if len(split) == 3:
      num = split[2]
      
      try:
        num = int(num)
      except ValueError:
        await message.channel.send(f"{num} is not a valid day limit, try 1 - 15")
        return

      if num > 15 or num < 1:
        await message.channel.send(f"{num} is not a valid day limit, try 1 - 15")
        return

      await message.channel.send(get_weather(location, num))

    else:
      await message.channel.send(get_weather(location, DAY_LIMIT))

client.run(BOT_TOKEN)
