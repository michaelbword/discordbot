# bot.py
import os
import discord
import dnd5e
from dotenv import load_dotenv


load_dotenv('venv/.env')  # Loads secret key from .env file

TOKEN = os.getenv("DISCORD_TOKEN")  # Gets secret key for Bot
GUILD = os.getenv("DISCORD_GUILD")  # Gets name of Discord Server

intents = discord.Intents.all()  # Sets intent to allow bot to interact with discord
client = discord.Client(intents=intents, case_insensitive=True)


no_result_message = 'Sorry, the princess is in another castle...'  # Error message declaration


@client.event
async def on_member_join(member):
    channel = client.get_channel(958511278933016589)
    embed = discord.Embed(title="Welcome!", description=f"{member.mention} has arrived and promised to bring all the booze. Where's it at, {member.mention}?")
    await channel.send(embed=embed)

# Instantiate DnD5e class from dnd5e.py
dnd_5e = dnd5e.DnD5e()


@client.event  # Spits out online status when Bot successfully initializes
async def on_ready():
    print(f'{client.user} is now online!')


@client.event
async def on_message(message):  # Stops bot from replying to itself
    if message.author == client.user:
        return
        # lower case message
    message_content = message.content.lower()

    if 'joke' in message.content.lower():  # Checks for this user input then responds
        await message.channel.send('Your life')

    if f'$search' in message_content:  # Sets $search as command to initiate web scrape

        key_words, search_words = dnd_5e.key_words_search_words(message_content)  # Looks for keywords to search with in message_content
        result_links = dnd_5e.search(key_words)
        links = dnd_5e.send_link(result_links, search_words)

        if len(links) > 0:
            for link in links:
                await message.channel.send(link)
        else:
            await message.channel.send(no_result_message)

client.run(TOKEN)
