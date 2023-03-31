from __future__ import print_function
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import discord
import random

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

creds = None
used = []

async def setup_sheets_creds():
    global creds

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

async def valo_custom_game_selection(interaction: discord.Interaction, repeat: bool = False, refresh: bool = False):
    global creds
    global used

    await setup_sheets_creds()

    SAMPLE_SPREADSHEET_ID = '1-u3cpXsr2Hp4OBL7IepN0OXkELhB0K_GPMXp1WtMgTs'
    SAMPLE_RANGE_NAME = 'Options!A:F'

    try:
        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range=SAMPLE_RANGE_NAME).execute()
        values = result.get('values', [])

        if (len(used) + 1) == len(values):
            interaction.response.send_message(embed=discord.Embed(
                title="You have no more gamemodes!",
                color=discord.Colour.dark_green().__hash__()
            ))

        if refresh:
            used = []
        
        index = random.randrange(1, len(values))

        if not repeat:
            while index in used:
                index = random.randrange(len(values))
            used.append(index)

        row = values[index]
        column_names = values[0]
        
        embed = discord.Embed(
            title="Valorant Custom Game:",
            color=discord.Colour.dark_green().__hash__()
        )

        for x in range(len(row)):
            embed.add_field(
                name=column_names[x],
                value=row[x],
                inline=False
            )
        await interaction.response.send_message(embed=embed)         
            
    except HttpError as err:
        print(err)
