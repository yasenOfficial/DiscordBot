# IMPORT DISCORD.PY. ALLOWS ACCESS TO DISCORD'S API.
import discord
import datetime
import python_weather
import base64
import os
import requests
import numpy as np
import cv2
import openai
from dotenv import load_dotenv

from dotenv import load_dotenv
from discord.ext.commands import Bot

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
openai.Model.list()    

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

bot = Bot("!", intents=discord.Intents.all())

helpDict = {"hello": "Greets the user and shows the time",
            "temp": "Shows the temperature in Stara Zagora", 
            "help": "Shows this message"}

bot.remove_command('help')

@bot.command("help", pass_context=True)
async def on_help(ctx):
    help_text = "```\n"

    for key, value in helpDict.items():
        help_text += f"Command: {key}, Description: {value}\n"

    help_text += "```"
    
    await ctx.channel.send(help_text)


@bot.command("hello", pass_context = True)
async def on_hello(ctx):

    await ctx.channel.send(f"Hello {ctx.message.author.mention}! The time is: {datetime.datetime.now().strftime('%H:%M:%S')}")

@bot.command("temp", pass_context = True)
async def on_temp(ctx):
  # declare the client. the measuring unit used defaults to the metric system (celcius, km/h, etc.)
    async with python_weather.Client(unit=python_weather.IMPERIAL) as client:
        # fetch a weather forecast from a city
        weather = await client.get('Stara Zagora')
    await ctx.channel.send(f"Hello {ctx.message.author.mention}! The temperature in Stara Zagora is: {int((weather.current.temperature - 32)*5/9)}°C")

@bot.command("chatgpt", pass_context = True)
async def on_temp(ctx, *args):
    messages = [{"role": "system", "content": "You are a kind helpful assistant."}]

    message = ' '.join(args)

    if message:
        messages.append(
            {"role": "user", "content": message},
        )
        chat = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k", messages=messages
        )
    
    reply = chat.choices[0].message.content
    print(f"ChatGPT: {reply}")
    messages.append({"role": "assistant", "content": reply})

    await ctx.send(f"ChatGPT: {reply}")


bot.run(DISCORD_TOKEN)