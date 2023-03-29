import discord
from discord.ext import commands
from discord import app_commands
import os
from typing import Tuple
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import personal_ext
import randomizer_ext


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
        super().__init__(intents=discord.Intents.all())
        
        self.synced = False

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            for x in guild_objects:
                await tree.sync(guild=x)
            self.synced = True
        print(f'Logged in as {self.user}')
        
        # users = ["Rayven", "Jessi", "Owen","Alyssa"]
        # user_ids = [290294208634290179, 963157243786825768, 494265123217735686, 399372400279683096]
        # user_obj = [(await self.fetch_user(x)) for x in user_ids]
        # print(user_obj)
        # selection = random.sample(range(4), 4)
        # while(selection[0] == 0 or selection[1] == 1 or selection[2] == 2 or selection[3] == 3):
        #     print("Someone got themselves. Retrying...")
        #     selection = random.sample(range(4), 4)
        # print('Everyone got someone different!')
        # for x in range(4):
        #     await user_obj[x].send(f"It's time to reroll due to some circumstances.\nThe above rules still apply.\nHere's your new person: ***{users[selection[x]]}***")

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
    guilds=guild_objects[0:2]

)
async def time_to_tswizzle(interaction: discord.Interaction):
    await personal_ext.time_to_tswizzle(interaction)

#------------------------------- Randomizer Ext -------------------------------

@tree.command(
    name="createteams",
    description="Randomize people in server into equal (enough) teams",
    guilds= guild_objects
)
async def createteams(interaction: discord.Interaction, number_of_teams: int, in_call: discord.VoiceChannel = None):
    await randomizer_ext.createteams(interaction, number_of_teams, in_call)


client.run(TOKEN)