import discord
from discord.ext import commands
from discord import app_commands
import os
from typing import List
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import helper_functions.google_sheets as google_sheets
import helper_functions.personal_ext as personal_ext
import helper_functions.team_makers as team_makers



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
personal_guilds = []
collections = db.collection(u'Random_Stuff').document(u'Guilds').collections()
for x in collections:
    guild_objects.append(discord.Object(x.id))
    if(x.id == "1026665499309908009" or x.id == "955312528123113482"):
        personal_guilds.append(discord.Object(x.id))


class random_stuff(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.all())
        
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

#------------------------------ Personal Stuff -------------------------------

@tree.command(
    name="timetotswizzle", 
    description="How much longer until we see the Goddess herself", 
    guilds=personal_guilds

)
async def time_to_tswizzle(interaction: discord.Interaction):
    await personal_ext.time_to_tswizzle(interaction)

#------------------------------- Randomizer Ext -------------------------------

@tree.command(
    name="createteams",
    description="Randomize people in server into equal (enough) teams",
    guilds= guild_objects
)
async def create_teams(interaction: discord.Interaction, number_of_teams: int, rename_teams: bool = None, in_call: discord.VoiceChannel = None):
    await team_makers.create_teams(interaction, number_of_teams, rename_teams, in_call)

@tree.command(
    name="renameteams",
    description="Team captain privilages! Rename your team :)",
    guilds=guild_objects
)
async def rename_teams(interaction: discord.Interaction):
    await team_makers.rename_teams(interaction)

@tree.command(
    name="customgameselect",
    description="Get custom rulesets!",
    guilds=guild_objects
)
@app_commands.choices(gametype=[
    app_commands.Choice(name="Valorant", value="valo")
])
@app_commands.describe(
    repeat="Repeat gamemodes, meaning you can get the same gamemode multiple times possibly.",
    refresh="Refresh list of game modes removed from no repeating. If repeat is turned on, this is not needed."
)
async def valo_custom_game_selection(interaction: discord.Integration, gametype: app_commands.Choice[str], repeat: bool = False, refresh: bool = False):
    if gametype.value == "valo":
        await google_sheets.valo_custom_game_selection(interaction, repeat, refresh)




client.run(TOKEN)