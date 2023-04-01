
from datetime import datetime
import discord
import pytz


async def time_to_tswizzle(interaction: discord.Interaction):
    concert_time = datetime(2023, 7, 15, 18, 30, tzinfo= pytz.timezone("US/Mountain"))
    concert_time_utc = concert_time.astimezone(pytz.UTC)
    current_time_utc = interaction.created_at.astimezone(pytz.UTC)
    delta = concert_time_utc - current_time_utc
    await interaction.response.send_message(f"{delta.days} days, {delta.seconds // 3600} hours, {(delta.seconds // 60) % 60} minutes, {delta.seconds % 60} seconds")