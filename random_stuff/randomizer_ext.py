import discord
from discord.ext import commands
from discord import app_commands
import random

async def randomize_teams(interaction: discord.Interaction, teams: int, in_call: discord.VoiceChannel = None):
    guild = interaction.guild
    member_list = []
    if in_call != None:
        for x in in_call.members:
            member_list.append(x)
    else:
        for x in guild.members:
            if x._user.bot:
                continue
            member_list.append(x)
    if(teams > len(member_list)):
        await interaction.channel.send(f"You have more teams than the number of people.")
    else:
    
        random.shuffle(member_list)
        sorted_teams = []
        for index, x in enumerate(member_list):
            if(index < teams and not x._user.bot):
                sorted_teams.append([x])
            else:
                sorted_teams[index % teams].append(x)
        message = ""
        for x in range(teams):
            row = sorted_teams[x]
            message += f'Team {x + 1}:\n'
            for y in row:
                message += f'• {y.name}\n'
            message += "\n"
        await interaction.channel.send(message)

