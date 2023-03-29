import discord
from discord.ext import commands
from discord import app_commands
import random

async def createteams(interaction: discord.Interaction, teams: int, in_call: discord.VoiceChannel = None):
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
        embed = discord.Embed(
            title="Here are your teams!",
            color= discord.Colour.dark_green().__hash__()
        )
        for x in range(teams):
            row = sorted_teams[x]
            team_list = ""
            for y in row:
                team_list += f'• {y.name}\n'
            embed.add_field(
                name=f"Team {x + 1}", # add <#{ voice chat id}> if you want to specify a voice channel
                value=team_list,
                inline=False
            )
        await interaction.channel.send(embed=embed)

