import discord
from discord.ext import commands
from discord import app_commands
import random

from typing import Dict

team_captains = {}
last_embed: discord.Embed = None

async def create_teams(interaction: discord.Interaction, teams: int, rename_teams: bool = False, in_call: discord.VoiceChannel = None):
    
    global team_captains
    global last_embed

    team_captains.clear()
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
        await interaction.response.send_message( embed=discord.Embed(
            title="You have more teams than the number of people.",
            color= discord.Colour.dark_green().__hash__()
        ))
    else:
        random.shuffle(member_list)
        sorted_teams = []
        for index, x in enumerate(member_list):
            if(index < teams and not x._user.bot):
                sorted_teams.append([x])
                if rename_teams:
                    team_captains.update({x._user.id : x})
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
        last_embed = embed
        await interaction.response.send_message(embed=embed)
        captain_string = ""
        for index, x in enumerate(team_captains):
            if index + 1 == len(team_captains):
                captain_string += " and "
            captain_string += f"<@{x}>"
            if index + 1 < len(team_captains):
                captain_string += ","
            
        await interaction.channel.send(f"Teams have been set! Team captains {captain_string}, please use `/renameteams` to rename your team.")
    
async def rename_teams(interaction: discord.Interaction):
    if not (interaction.user.id in team_captains.keys()):
        await interaction.response.send_message("Sorry, you're not a team captain. Team captains are the only ones to rename their team.", ephemeral=True)
        return
    rename_teams_modal = RenameTeamsModal()
    rename_teams_modal.last_embed = last_embed
    await interaction.response.send_modal(rename_teams_modal)

class RenameTeamsModal(discord.ui.Modal):
    last_embed: discord.Embed = None
    global team_captains
    def __init__(self):
        super().__init__(title="New Team Name")
        self.add_item(discord.ui.TextInput(label="New Team Name (you can only do this once!)"))

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message("Thanks! Waiting for other responses, then I'll post!", ephemeral=True)
        new_name = interaction.data.get("components")[0].get("components")[0].get("value")

        index = list(team_captains.keys()).index(interaction.user.id)

        values = self.last_embed.fields[index].value
        self.last_embed.remove_field(index)
        self.last_embed.add_field(
            name= f"Team {new_name}",
            value= values,
            inline= False
        )

        team_captains.pop(interaction.user.id)

        if len(team_captains) == 0:
            await interaction.channel.send(embed=self.last_embed)

            


