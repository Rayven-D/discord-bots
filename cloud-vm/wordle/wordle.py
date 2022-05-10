import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_choice, create_option
import os
import re
from quickchart import QuickChart
from dotenv import load_dotenv
import http.client
import json
import urllib.parse



load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

cred = credentials.Certificate('wordle-bot-discord-firebase-adminsdk-pcdbv-c5915e6837.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

bot = commands.Bot(command_prefix='!')
bot.remove_command('help')
slash = SlashCommand(bot, sync_commands=True)

guild_ids = [955312528123113482,928141122943987753]

@slash.slash(
    name='getuserstats',
    description='Get a user\'s Wordle stats',
    guild_ids=guild_ids,
    options=[
        create_option(
            name='users',
            description='Choose a user',
            required=True,
            option_type=6
        )
    ]
)
async def get_wordle_stats(ctx: SlashContext, users):
    user_id = users.id
    doc_ref = db.collection(u'Users').document(f'{user_id}').get()
    doc = doc_ref.to_dict()
    qc = QuickChart()
    qc.config = {
        'type': 'horizontalBar',
        'data':{
            'labels':['1', '2', '3', '4','5','6','X'],
            'datasets':[{
                'label': 'Tries',
                'data': doc.get('tries'),
            }]
        },
        'options':{
            'plugins': {
                'datalabels': {
                    'anchor': 'center',
                    'align': 'center',
                    'color': 'white',
                    'font': {
                        'weight': 'normal',
                    },
                },     
            } 
        }
    }
    qc.background_color ='white'
    embed = discord.Embed(title=f'{doc.get("username")} stats', color=discord.Colour.green().__hash__())
    embed.set_image(url=qc.get_url())
    await ctx.send(embed=embed)

@slash.slash(
    name='getmystats',
    description='Get your Wordle stats',
    guild_ids=guild_ids,
)
async def get_my_wordle_stats(ctx):
    user_id = ctx.author.id
    doc_ref = db.collection(u'Users').document(f'{user_id}').get()
    doc = doc_ref.to_dict()
    qc = QuickChart()
    qc.config = {
        'type': 'horizontalBar',
        'data':{
            'labels':['1', '2', '3', '4','5','6','X'],
            'datasets':[{
                'label': 'Tries',
                'data': doc.get('tries'),
            }]
        },
        'options':{
            'plugins': {
                'datalabels': {
                    'anchor': 'center',
                    'align': 'center',
                    'color': 'white',
                    'font': {
                        'weight': 'normal',
                    },
                },     
            } 
        }
    }
    qc.background_color ='white'
    embed = discord.Embed(title=f'{doc.get("username")} stats', color=discord.Colour.green().__hash__())
    embed.set_image(url=qc.get_url())
    await ctx.send(embed=embed)

@slash.slash(
    name='getmycount',
    description='Get the number of Wordles you have completed',
    guild_ids=guild_ids,
)
async def get_my_streak(ctx):
    user_id = ctx.author.id
    doc_ref = db.collection(u'Users').document(f'{user_id}').get()
    doc = doc_ref.to_dict()
    tries = doc.get('tries')
    count = 0
    for t in tries:
        count += t
    response = f'You have a streak of: `{count}`'
    await ctx.send('> {}'.format(response))

@slash.slash(
    name='getusercount',
    description='Get the number of Wordles a user has completed',
    guild_ids=guild_ids,
    options=[
        create_option(
            name='users',
            description='Choose a user',
            required=True,
            option_type=6
        )
    ]
)
async def get_streak(ctx, users):
    user_id = users.id
    doc_ref = db.collection(u'Users').document(f'{user_id}').get()
    doc = doc_ref.to_dict()
    tries = doc.get('tries')
    count = 0
    for t in tries:
        count += t
    response = f'{doc.get("username")} has a streak of: `{count}`'
    await ctx.send('> {}'.format(response))

@slash.slash(
    name='8ball',
    description='Ask the all knowing 8 ball a question',
    guild_ids=guild_ids,
    options=[
        create_option(
            name='question',
            description='Give the 8 ball a yes/no question (no slashes plz)',
            required=True,
            option_type=3
        )
    ]
)
async def magic_8_ball(ctx, question):
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
    await ctx.send(embed=embed)


@bot.event
async def on_message(message):
    wordle_regex = re.compile(r"Wordle [0-9]+ [1-6X]/6")
    if(wordle_regex.search(message.content)):
        doc_ref = db.collection(u'Users').document(f'{message.author.id}')
        temp_ref = doc_ref.get()
        if(temp_ref.exists):
            doc = temp_ref.to_dict()
            tries = doc.get('tries')
            tries_index = message.content.find('/') - 1
            num_tries = message.content[tries_index]
            index = 6
            if(num_tries.isnumeric()):
                index = int(num_tries) - 1
            tries[index] += 1
            doc_ref.update({
                u'tries': tries
            })
            await message.channel.send(f'Thanks {doc.get("username")}! uWu <3. It is saved!')
        else:
            tries = [0,0,0,0,0,0,0]
            tries_index = message.content.find('/') - 1
            num_tries = message.content[tries_index]
            index = 6

            if(num_tries.isnumeric()):
                index = int(num_tries) - 1
            tries[index] += 1
            data = {
                u'id': message.author.id,
                u'tries': tries,
                u'username': message.author.ursername
            }
            doc_ref.set(data)
            await message.channel.send(f'Thanks {doc.get("username")}, and welcome to the Daily Wordle! I will keep track of all of your tries and guesses.')
    await bot.process_commands(message=message)


bot.run(TOKEN)