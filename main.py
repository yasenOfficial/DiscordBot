# IMPORT DISCORD.PY. ALLOWS ACCESS TO DISCORD'S API.
import discord
from TTS.api import TTS
import datetime
import python_weather
import base64
import os
import requests
import numpy as np
import openai
import re
import random

from dotenv import load_dotenv
from TTS.api import TTS
from discord.ext.commands import Bot, Context


load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
openai.Model.list()    

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

bot = Bot("!", intents=discord.Intents.all())

helpDict = {"hello": "Greets the user and shows the time",
            "temp": "Shows the temperature in Stara Zagora", 
            "help": "Shows this message",
            "roll": "Rolls a dice",
            "chatgpt": "Chat with GPT-3, generates text to speech + image output"}

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

    await ctx.channel.send(f"`Hello {ctx.message.author.mention}! The time is: {datetime.datetime.now().strftime('%H:%M:%S')}`")

@bot.command("temp", pass_context = True)
async def on_temp(ctx):
  # declare the client. the measuring unit used defaults to the metric system (celcius, km/h, etc.)
    async with python_weather.Client(unit=python_weather.IMPERIAL) as client:
        # fetch a weather forecast from a city
        weather = await client.get('Stara Zagora')
    await ctx.channel.send(f"`Hello {ctx.message.author.mention}! The temperature in Stara Zagora is: {int((weather.current.temperature - 32)*5/9)}°C`")

@bot.command(name = "roll", description = "roll a dice!")
async def roll(ctx):
    await ctx.channel.send(f"`Rolled: {random.randint(1, 6)}`")

@bot.command("chatgpt", pass_context = True)
async def on_temp(ctx, *args):

    staticPrompt = "sumarise the following text:\n\n"

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

    print(reply)
    
    messages.append({"role": "assistant", "content": reply})

    sentences = []
    paragraphs = reply.split('\n\n')
    
    for paragraph in paragraphs:
        s = re.split(r'(?<=[.!?]) +', paragraph)
        sentences.append(s)
            
    tts = TTS(model_name='tts_models/en/vctk/vits', progress_bar=False, gpu=False)

    male_voice = "p273"
    female_voice = "p230"

    output_dir = "output"
    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)

    
    for p in paragraphs:
        tts.tts_to_file(text=p, speaker=male_voice , file_path="output/output.wav")

        sumarisedprompt = staticPrompt + p

        messages = [{"role": "system", "content": "You are a kind helpful assistant."}]

        message = sumarisedprompt

        if message:
            messages.append(
                {"role": "user", "content": message},
            )
            chat = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-16k", messages=messages
            )

        
        sumarisedReply = chat.choices[0].message.content

        print(sumarisedReply)
        
        messages.append({"role": "assistant", "content": reply})

        response = openai.Image.create(prompt=p,n=1,size="512x512")
        sumarisedResponse = openai.Image.create(prompt=sumarisedReply,n=1,size="512x512")


        await ctx.send(f"`{p}`")
        await ctx.send(file = discord.File("output/output.wav", "output.wav"))

        await ctx.send(f"`Whole paragraph to image:`")
        await ctx.send(response["data"][0]["url"])


        await ctx.send(f"`Sumarised prompt to image:`")
        await ctx.send(sumarisedResponse["data"][0]["url"])
    
bot.run(DISCORD_TOKEN)