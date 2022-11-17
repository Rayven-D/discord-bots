import discord
from discord.ext import commands
from discord import app_commands
import os
import re
from dotenv import load_dotenv
import random
from datetime import datetime, timezone
import pytz
import http.client
import urllib.parse
import json


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
guild_ids = [955312528123113482, 1026665499309908009]
guild_objects = [discord.Object(x) for x in guild_ids]

class random_stuff(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.synced = False

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            for x in guild_objects:
                await tree.sync(guild=x)
            self.synced = True
        print(f'Logged in as {self.user}')

client = random_stuff()
tree = app_commands.CommandTree(client)

@tree.command(
    name="timetotswizzle", 
    description="How much longer until we see the Goddess herself", 
    guilds=guild_objects
)
async def time_to_tswizzle(interaction: discord.Interaction):
    concert_time = datetime(2023, 7, 15, 18, 30, tzinfo= pytz.timezone("US/Mountain"))
    concert_time_utc = concert_time.astimezone(pytz.UTC)
    current_time_utc = interaction.created_at.astimezone(pytz.UTC)
    delta = concert_time_utc - current_time_utc
    await interaction.response.send_message(f"{delta.days} days, {delta.seconds // 3600} hours, {(delta.seconds // 60) % 60} minutes, {delta.seconds % 60} seconds")

@tree.command(
    name="8ball", 
    description="Ask the all knowing 8 ball a question", 
    guilds=guild_objects
)
async def magic_8_ball(interaction: discord.Interaction, question: str):
    conn = http.client.HTTPSConnection("8ball.delegator.com")
    question_param = urllib.parse.quote(question)
    conn.request('GET', '/magic/JSON/' + question_param)
    response = conn.getresponse()
    response_object = json.loads(response.read())
    type = response_object.get('magic').get('type')
    color = discord.Colour.light_grey().__hash__()
    if(type == 'Contrary'):
        color = discord.Colour.red().__hash__()
    elif(type == 'Affirmative'):
        color = discord.Colour.green().__hash__()
    embed = discord.Embed(
        title= response_object.get('magic').get('answer'),
        description='Magic 8 ball knows all',
        color=color
    )
    embed.set_author(name=response_object.get('magic').get('question'))
    await interaction.response.send_message(embed=embed)

client.run(TOKEN)