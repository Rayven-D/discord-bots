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
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

cred = credentials.Certificate({
    "type": os.getenv("FIREBASE_TYPE"),
    "project_id": os.getenv('FIREBASE_PROJECT_ID'),
    "private_key_id": os.getenv('FIREBASE_PRIVATE_KEY_ID'),
    "private_key": os.getenv('FIREBASE_PRIVATE_KEY'),
    "client_email": os.getenv('FIREBASE_CLIENT_EMAIL'),
    "client_id": os.getenv("FIREBASE_CLIENT_ID"),
    "auth_uri": os.getenv("FIREBASE_AUTH_URI"),
    "token_uri": os.getenv("FIREBASE_TOKEN_URI"),
    "auth_provider_x509_cert_url": os.getenv("FIREBASE_AUTH_PROVIDER_CERT_URL"),
    "client_x509_cert_url": os.getenv("FIREBASE_CERT_URL")
})

firebase_admin.initialize_app(cred)

db = firestore.client()

guild_objects = []
collections = db.collection(u'Random_Stuff').document(u'Guilds').collections()
for x in collections:
    guild_objects.append(discord.Object(x.id))


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

    async def on_guild_join(self, guild):
        doc_ref = db.collection(u'Random_Stuff').document(u'Guilds')
        temp_ref = doc_ref.get()
        if(temp_ref.exists):
            doc_ref.collection(f'{guild.id}').document(u'Guild_Info').set({
                'name': guild.name
            })
    async def on_guild_remove(self, guild):
        col_ref = db.collection(u'Random_Stuff').document(u'Guilds').collection(f'{guild.id}')
        docs = col_ref.list_documents()
        for doc in docs:
            doc.delete()


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
    print('testing')
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