import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import discord
from discord.ext import commands
import os
import re
from quickchart import QuickChart
from dotenv import load_dotenv



load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

cred = credentials.Certificate('wordle-bot-discord-firebase-adminsdk-pcdbv-c5915e6837.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

bot = commands.Bot(command_prefix='!')
bot.remove_command('help')


@bot.command(name='getstats')
async def get_wordle_stats(ctx, arg):
    user_id = re.sub(r'[^0-9]','', arg)
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

@bot.command(name='getmystats')
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

@bot.command(name='getmystreak')
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

@bot.command(name='getstreak')
async def get_streak(ctx, arg):
    user_id = re.sub(r'[^0-9]','', arg)
    doc_ref = db.collection(u'Users').document(f'{user_id}').get()
    doc = doc_ref.to_dict()
    tries = doc.get('tries')
    count = 0
    for t in tries:
        count += t
    response = f'{doc.get("username")} has a streak of: `{count}`'
    await ctx.send('> {}'.format(response))

@bot.command(name="help")
async def wordle_bot_help(ctx):
    header = '**Help is on the way!** \n__Here are some commands for me:__\n'
    streaks = '`!getmystreak` -> get your current Wordle streak\n`!getstreak @<user>` -> get Wordle streak of tagged user\n'
    stats = '`!getmystats` -> get your current Wordle stats\n`!getstats @<user>` -> get Wordle stats of tagged user\n'
    help = '`!help` -> pull up help menu for all commands available\n'

    response = header + streaks + stats + help
    await ctx.send('>>> {}'.format(response))
@bot.event
async def on_command_error(ctx, error):
    failed = '**Not a known command...**\n__Here are some commands for me:__\n'
    streaks = '`!getmystreak` -> get your current Wordle streak\n`!getstreak @<user>` -> get Wordle streak of tagged user\n'
    stats = '`!getmystats` -> get your current Wordle stats\n`!getstats @<user>` -> get Wordle stats of tagged user\n'
    help = '`!help` -> pull up help menu for all commands available\n'

    response = failed + streaks + stats + help
    await ctx.send('>>> {}'.format(response))


bot.run(TOKEN)